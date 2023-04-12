import pandas

# Dataset obtained from here: https://www.kaggle.com/datasets/ulrikthygepedersen/rotten-tomatoes-reviews
PATH_TO_DATA_FILE = "./data/rt_reviews.csv"

def main():

    # Read CSV file
    df = pandas.read_csv(PATH_TO_DATA_FILE, encoding_errors="ignore")

    # Replicate certain rows as the plagiarized data set
    df['replicated'] = False
    df.loc[df['Review'].str.contains("yet"), 'replicated'] = True 
    df = df.append([df[df['replicated'] == True]],ignore_index=True)

    # Save as new CSV file
    df.to_csv("./data/rt_reviews_plagiarized.csv")

if __name__ == "__main__":
    main()
