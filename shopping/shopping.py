import csv
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # loading data from csv
    data = pd.read_csv("shopping.csv")
    df = pd.DataFrame(data, dtype=object)
    # breaking imported data into evidence and labels
    evidence_df = df.iloc[:, :17]
    labels = df["Revenue"]
    # lists for Month, VisitorType, Weekend, Revenue columns (to be stored as int)
    Month = []
    VisitorType = []
    Weekend = []
    Revenue = []

    # month-to-number switcher
    def months_to_numbers(month):
        switcher = {
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "Apr": 3,
            "May": 4,
            "Jun": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11
        }
        return switcher.get(month, 12)

    # visitor-to-number switcher
    def visitors_to_numbers(visitor):
        switcher = {
            "Returning_Visitor": 1,
            "New_Visitor": 0
        }
        return switcher.get(visitor, 0)

    # boolean-to-number switcher
    def booleans_to_numbers(bool):
        switcher = {
            False: 0,
            True: 1
        }
        return switcher.get(bool)
    # adding corresponding numeric value of Month, VisitorType and Weekend to lists
    for i in range(len(evidence_df)):
        Month.append(months_to_numbers(evidence_df["Month"][i]))
        VisitorType.append(visitors_to_numbers(evidence_df["VisitorType"][i]))
        Weekend.append(booleans_to_numbers(evidence_df["Weekend"][i]))
        Revenue.append(booleans_to_numbers(labels[i]))
    evidence_df["Month"] = Month
    evidence_df["VisitorType"] = VisitorType
    evidence_df["Weekend"] = Weekend
    labels = Revenue
    evidence = evidence_df.values.tolist()
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    count_positive = 0  # total number of positive labels
    count_negative = 0  # total number of negative labels
    count_sensitivity = 0  # total number of positive labels that were accurately identified
    count_specificity = 0  # total number of negative labels that were accurately identified
    for i in range(len(labels)):
        if labels[i] == 1:
            count_positive += 1
            if predictions[i] == 1:
                count_sensitivity += 1
        else:
            count_negative += 1
            if predictions[i] == 0:
                count_specificity += 1
    sensitivity = count_sensitivity/count_positive
    specificity = count_specificity/count_negative
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
