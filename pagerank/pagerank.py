import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
CONVERGE_THRESHOLD = 0.001


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    len_page = len(corpus[page])
    len_corpus = len(corpus)
    pd = {}
    for key in corpus.keys():
        pd[key] = (1-damping_factor)/len_corpus  # every page gets (1-d)/N
    if len_page != 0:
        for linked_page in corpus[page]:
            pd[linked_page] += damping_factor/len_page  # every page that is linked from current page gets additional probability
    else:
        for key in corpus.keys():  # if there's no page linked, every page gets equal probability
            pd[key] = pd[key]/(1-damping_factor)
    return pd


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    len_corpus = len(corpus)
    times_visited = {}  # dictionary storing number of times each page is visited
    PR = {}  # dictionary storing PR value of each page
    # initialize number of visiting of every page to zero 
    for page in corpus.keys():
        times_visited[page] = 0
    # random number of first page visited
    first_page_number = random.randint(0, len_corpus-1)
    current_page = list(corpus.keys())[first_page_number]
    times_visited[current_page] += 1
    # iterate n times to get n samples, adding to times_visited every time any page is visited
    for i in range(n):
        transition_dp = transition_model(corpus, current_page, damping_factor)
        pages = list(transition_dp.keys())
        weights = list(transition_dp.values())
        current_page = random.choices(pages, weights=weights)[0]
        times_visited[current_page] += 1
    # calculating PR values for each page 
    for page in times_visited.keys():
        PR[page] = times_visited[page]/n
    return PR

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PR = {}
    new_PR = {}
    steps = {}  # stroing difference of PR values between each iteration 
    linking_pages = {}  # dictionary storing pages linking to the key page
    corpus_len = len(corpus)
    # initializing PR value of every page to 1/N
    for page in corpus.keys():
        PR[page] = 1/corpus_len
    # setting values of linking_pages to a set for every key page
    for page in corpus.keys():
        linking_pages[page] = set()
    # setting linking_pages (stores pages linking to the key page) from corpus
    for page in corpus.keys():
        for linked_page in corpus[page]:
            linking_pages[linked_page].add(page)
    while True:
        check = True  # for threashold checking
        # initializing first condition (1-d)/N
        for page in corpus.keys():
            steps[page] = False
            linked_pages = linking_pages[page]
            new_PR[page] = (1-damping_factor)/corpus_len
            # looping through all linking pages
            for linked_page in linked_pages:
                linked_pages_len = len(corpus[linked_page])
                new_PR[page] += damping_factor * PR[linked_page]/linked_pages_len
        # check if threashold is met
        for page in corpus.keys():
            if new_PR[page] - PR[page] < CONVERGE_THRESHOLD:
                steps[page] = True
            check = check and steps[page]
            if check == False:
                break
        # if the threashould is not crossed by any page's PR value, break out of loop
        PR = new_PR.copy()
        if check == True:
            break
    return PR


if __name__ == "__main__":
    main()
