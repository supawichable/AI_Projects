import nltk
import os
import sys
import string
import math
import operator

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    ret_dict = {}
    for textfile in os.listdir(directory):
        f = open(os.path.join(directory, textfile))
        text = f.read()
        ret_dict[textfile] = text
    return ret_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document)  # tokenize
    words = [word.lower() for word in words]  # make lowercase
    words = [word.translate(str.maketrans('', '', string.punctuation)) for word in words]  # remove punctuations
    words = [word for word in words if not word in nltk.corpus.stopwords.words("english")]  # remove stop words
    words = [word for word in words if word != '']
    return words
    

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    ret_dict = {}
    word_set = set()
    num_doc = len(documents)
    # add all words in every document to a set 'word_set'
    for document in documents.keys():
        word_set |= set(documents[document])
    # compute idf for each word and put in dictionary 'ret_dict'
    for word in word_set:
        count = 0
        for document in documents.keys():
            if word in documents[document]:  # count number of documents that contain word
                count += 1
        ret_dict[word] = math.log(num_doc/count)
    return ret_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = {document: 0 for document in files.keys()}
    # calculate sum of tf-idf for each file (document) 
    for word in query:
        for document in files.keys():
            tf = files[document].count(word)
            idf = idfs[word]
            tf_idf[document] += tf * idf
    # sort and return the n top files that match the query
    ret_dict = dict(sorted(tf_idf.items(), key=operator.itemgetter(1), reverse=True)[:n])
    return ret_dict.keys()


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_value = {sentence: 0 for sentence in sentences.keys()}  # dictionary to store idf value for each sentence
    qtd_value = {sentence: 0 for sentence in sentences.keys()}  # dictionary to store qtd value for each sentence
    idf_qtd = []  # list to store tuple of (sentence, idf, qtd)
    # calculate sum of idf value of each word for each sentence 
    for word in query:
        for sentence in sentences.keys():
            if word in sentences[sentence]:
                idf_value[sentence] += idfs[word]
            sentence_len = len(sentence)
            count_word = 0
            # count how many words in sentence exist in query
            for word_sen in sentences[sentence]:
                if word_sen in query:
                    count_word += 1
            qtd_value[sentence] = count_word/sentence_len
    # append values of idf_value and qtd_value to idf_qtd
    for sentence in sentences.keys():
        idf_qtd.append((sentence, idf_value[sentence], qtd_value[sentence]))
    # sort using idf as primary key and qtd as secondary key
    top_idf_qtd = sorted(idf_qtd, key=operator.itemgetter(1, 2), reverse=True)[:n]
    sen_top_idf_qtd = [tuple_top[0] for tuple_top in top_idf_qtd]  # take only sentence from the tuple
    return sen_top_idf_qtd


if __name__ == "__main__":
    main()
