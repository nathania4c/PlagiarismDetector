import pandas
import time
import re
import matplotlib.pyplot as plt

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

def KMP_Plagiarism_detector(dataset):

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

    # Recording the processing time for each 100 row increments
    kmp_processing_time = {}

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

        # For every 100 row increment record the processing time
        if i % 100 == 0:
            kmp_processing_time[i] = (time.time() - start_time)
        
    # Get total processing time
    kmp_processing_time[x] = (time.time() - start_time)

    print(f"Percentage plagiarised: {match_counter / total_words_in_sample_text * 100}%")

    return kmp_processing_time

def main():

    reviews = data_setup()

    # Recording the processing time for each 100 row increments
    kmp_processing_time = KMP_Plagiarism_detector(reviews)

    plt.plot(
        list(kmp_processing_time.keys()),
        list(kmp_processing_time.values()),
        marker='o'
    )
    plt.title('KMP')
    plt.xlabel('nrows')
    plt.ylabel('processing time (sec)')
    plt.show()

    exit()
    lcss_processing_time = []
    rabin_karp_processing_time = []


if __name__ == "__main__":
    main()
