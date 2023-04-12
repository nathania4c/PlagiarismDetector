import matplotlib.pyplot as plt
import numpy as np
import pandas
import re
import time

# Dataset obtained from here: https://www.kaggle.com/datasets/ulrikthygepedersen/rotten-tomatoes-reviews
PATH_TO_DATA_FILE = "./data/rt_reviews.csv"

def data_setup():

    # Read CSV file
    df = pandas.read_csv(PATH_TO_DATA_FILE, encoding_errors="ignore")

    # Replicate certain rows as the plagiarized data set
    df['replicated'] = False
    df.loc[df['Review'].str.contains("yet"), 'replicated'] = True 
    df = df.append([df[df['replicated'] == True]],ignore_index=True)

    # Shuffle row orders
    df = df.sample(frac=1).reset_index(drop=True)

    # Return plagiarized dataset as list
    return list(df['Review'].loc[0:1000])

def KMP_Plagiarism_Detector(dataset):

    def compute_match_table(lines, x):
        match_table = [[0]]*x
        for i in range(x):
            patterns = lines[i].strip(" ").split(" ")
            m = len(patterns)
            match_table[i] = computePrefix(patterns, m)
        return match_table
    
    def computePrefix(patterns, m):
        pi = [0] * m # array of longest prefix suffix
        k = 1           
        l = pi[0]
        while k < m:
            if patterns[k].lower() == patterns[l].lower():
                l += 1
                pi[k] = l
                k += 1
            else:
                if l == 0:
                    pi[k] = l
                    k += 1
                else:
                    l = pi[l-1]
        return pi

    def KMP_Matcher(dataset, patterns, pi):
        n = len(dataset)
        m = len(patterns)
        i = 0
        j = 0
        p = 0 # count how many words match

        while i < n:
            if dataset[i].lower() == patterns[j].lower():
                i += 1
                if j+1 == m:
                    j = pi[j]
                    p += m
                else:
                    j += 1
            else:
                if j == 0:
                    i += 1
                else:
                    j = pi[j-1]
        return p

    match_counter = 0 # words matched
    total_words_in_sample_text = 0

    # preprocessing
    x = len(dataset)
    match_table = compute_match_table(dataset, x)

    # KMP search
    start_time = time.time()
    for i in range(x):
        text = dataset[i].strip(" ").split(" ")

        for j in range(x):
            if (i == j):
                continue
            pattern = dataset[j].strip(" ").split(" ")
            match_counter += KMP_Matcher(text, pattern, match_table[j])

        total_words_in_sample_text += len(text)
        
    # Get total processing time
    processing_time = (time.time() - start_time)

    # print(f"KMP Percentage plagiarised: {match_counter / total_words_in_sample_text * 100}%")

    return [total_words_in_sample_text, processing_time]

def LCSS_Plagiarism_Detector(dataset):

    def lcss_length(X, Y):
        m = len(X)
        n = len(Y)
        LCS = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if X[i-1] == Y[j-1]:
                    LCS[i][j] = LCS[i-1][j-1] + 1
                else:
                    LCS[i][j] = max(LCS[i-1][j], LCS[i][j-1])
        return LCS[m][n]

    sum_lcss = 0
    total_words_in_sample_text = 0
    x = len(dataset)

    start_time = time.time()
    # LCSS_length
    for i in range(x):
        text = dataset[i].strip(" ").split(" ")
        for j in range(x):
            if (i == j):
                continue
            s = dataset[j].strip(" ").split(" ")
            sum_lcss += lcss_length(text, s)

        total_words_in_sample_text += len(text)

    # Get total processing time
    processing_time = (time.time() - start_time)

    # print(f"LCSS Percentage plagiarised: {sum_lcss / total_words_in_sample_text * 100}%")

    return [total_words_in_sample_text, processing_time]

class rolling_hash():
    def __init__(self, text, patternSize):
        self.text = text
        self.patternSize = patternSize
        self.base = 26
        self.window_start = 0
        self.window_end = 0
        self.mod = 5807
        self.hash = self.get_hash(text, patternSize)

    def get_hash(self, text, patternSize):
        hash_value = 0
        for i in range(0, patternSize):
            hash_value += (ord(self.text[i]) - 96)*(self.base**(patternSize - i -1)) % self.mod

        self.window_start = 0
        self.window_end =  patternSize

        return hash_value

    def next_window(self):
        if self.window_end <= len(self.text) - 1:
            self.hash -= (ord(self.text[self.window_start]) - 96)*self.base**(self.patternSize-1)
            self.hash *= self.base
            self.hash += ord(self.text[self.window_end])- 96
            self.hash %= self.mod
            self.window_start += 1
            self.window_end += 1
            return True
        return False

    def current_window_text(self):
        return self.text[self.window_start:self.window_end]

def Rabin_Karp_Plagiarism_Detector(dataset):
    # calaculate hash value of the file content
    # and add it to the document type hash table 
    def calculate_hash(text, doc_type):
        text = rolling_hash(text, k_gram)
        for _ in range(len(dataset) - k_gram + 1):
            hash_table[doc_type].append(text.hash)
            if text.next_window() == False:
                break

    def get_rate():
        return calaculate_plagiarism_rate(hash_table)
        
    # calculate the plagiarism rate using the plagiarism rate formula
    def calaculate_plagiarism_rate(hash_table):
        th_a = len(hash_table["a"])
        th_b = len(hash_table["b"])
        a = hash_table["a"]
        b = hash_table["b"]
        sh = len(np.intersect1d(a, b))

        # Formular for plagiarism rate
        # P = (2 * SH / THA * THB ) 100%
        p = (float(2 * sh)/(th_a + th_b)) * 100
        return p

    hash_table = {"a": [], "b": []}
    k_gram = 5
    x = len(dataset)
    
    total_words_in_sample_text = 0

    start_time = time.time()
    
    for i in range(x):
        content_a = dataset[i]
        content_b = ""
        for j in range(x):
            if i == j:
                continue
            content_b = content_b + dataset[j]

        calculate_hash(content_a, "a")
        calculate_hash(content_b, "b")

        total_words_in_sample_text += len(content_a.split())

        # print('The percentage of plagiarism held by both documents is  {0}%'.format(get_rate()))

    # Get total processing time
    processing_time = (time.time() - start_time)

    return [total_words_in_sample_text, processing_time]

def main():

    reviews = data_setup()

    size = len(reviews)

    #################
    # KMP Algorithm #
    #################

    # Recording the processing time for each 250 row increments
    kmp_processing_time = {}
    nrows = 250
    while nrows < size:
        result = KMP_Plagiarism_Detector(reviews[0:nrows])
        kmp_processing_time[result[0]] = result[1] 
        if nrows + 250 < size:
            nrows = nrows + 250
        elif nrows == size - 1:
            break
        else:
            nrows = size - 1

    ##################
    # LCSS Algorithm #
    ##################

    # Recording the processing time for each 250 row increments
    lcss_processing_time = {}
    nrows = 250
    while nrows < size:
        result = LCSS_Plagiarism_Detector(reviews[0:nrows])
        lcss_processing_time[result[0]] = result[1] 
        if nrows + 250 < size:
            nrows = nrows + 250
        elif nrows == size - 1:
            break
        else:
            nrows = size - 1
    
    ########################
    # Rabin Karp Algorithm #
    ########################

    # Recording the processing time for each 250 row increments
    rk_processing_time = {}
    nrows = 250
    while nrows < size:
        result = Rabin_Karp_Plagiarism_Detector(reviews[0:nrows])
        rk_processing_time[result[0]] = result[1] 
        if nrows + 250 < size:
            nrows = nrows + 250
        elif nrows == size - 1:
            break
        else:
            nrows = size - 1

    # Plot all processing time
    plt.plot(
        list(kmp_processing_time.keys()),
        list(kmp_processing_time.values()),
        marker='o',
        label='KMP'
    )

    plt.plot(
        list(lcss_processing_time.keys()),
        list(lcss_processing_time.values()),
        marker='o',
        label='LCSS'
    )

    plt.plot(
        list(rk_processing_time.keys()),
        list(rk_processing_time.values()),
        marker='o',
        label='Rabin Karp'
    )

    plt.title('Processing Time in Seconds X Number of Words')
    plt.xlabel('number of words')
    plt.ylabel('processing time (sec)')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
