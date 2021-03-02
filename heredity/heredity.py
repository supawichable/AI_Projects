import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]
   
   
def gene_copies(person, one_gene, two_genes):
    """
    Return number of GJB2 genes a person has
    """
    if person in two_genes:
        return 2
    elif person in one_gene:
        return 1
    else:
        return 0


def trait(person, have_trait):
    """
    Return True if a person has trait, False if doesn't
    """
    if person in have_trait:
        return True
    else:
        return False


def prob_gene_transmitted(person, one_gene, two_genes):
    """
    Return probability of a person transimiting GJB2 gene
    """
    if person in two_genes:
        return 1 - PROBS["mutation"]
    elif person in one_gene:
        return 0.5
    else:
        return PROBS["mutation"]


def prob_gene_not_transmitted(person, one_gene, two_genes):
    """
    Return probability of a person NOT transimiting GJB2 gene
    """
    if person in two_genes:
        return PROBS["mutation"]
    elif person in one_gene:
        return 0.5
    else:
        return 1 - PROBS["mutation"]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    roots = set()  # set of root nodes (i.e. people with no parents specified)
    children = set()  # set of child nodes (i.e. people with parents specified)
    prob = {}  # dictionary containing probability of each node
    ret_val = 1  # return value
    # adding root and child nodes to "roots" and "children"
    for person in people.keys():
        if people[person]['mother'] == None:
            roots.add(person)
        else:
            children.add(person)
    # evaluate probability of root nodes
    for person in roots:
        person_gene_copies = gene_copies(person, one_gene, two_genes)
        person_trait = trait(person, have_trait)
        prob[person] = PROBS["gene"][person_gene_copies] * PROBS["trait"][person_gene_copies][person_trait]
        ret_val *= prob[person]
    # evaluate probability of children node
    for person in children:
        mother = people[person]['mother']
        father = people[person]['father']
        person_gene_copies = gene_copies(person, one_gene, two_genes)
        person_trait = trait(person, have_trait)
        if person in two_genes:
            prob[person] = prob_gene_transmitted(mother, one_gene, two_genes) * prob_gene_transmitted(father, one_gene, two_genes) 
        elif person in one_gene:
            prob[person] = prob_gene_transmitted(mother, one_gene, two_genes) * prob_gene_not_transmitted(
                father, one_gene, two_genes) + prob_gene_not_transmitted(mother, one_gene, two_genes) * prob_gene_transmitted(father, one_gene, two_genes)
        else:
            prob[person] = prob_gene_not_transmitted(mother, one_gene, two_genes) *\
                prob_gene_not_transmitted(father, one_gene, two_genes)
        ret_val *= (prob[person] * PROBS["trait"][person_gene_copies][person_trait])
    return ret_val


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        person_gene_copies = gene_copies(person, one_gene, two_genes)  # number of genes a person has
        person_trait = trait(person, have_trait)  # trait a person has (TRUE or FALSE)
        probabilities[person]["gene"][person_gene_copies] += p  # update gene values in probabilities
        probabilities[person]["trait"][person_trait] += p *\
            PROBS['trait'][person_gene_copies][person_trait]  # update trait values in probabilities


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        g = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        t = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0]/g
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1]/g
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2]/g
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False]/t
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True]/t


if __name__ == "__main__":
    main()
