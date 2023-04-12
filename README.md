# Plagiarism Detector

- Nihad Alakbarzade
- Nathania Hendradjaja

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
    - [Install Python3](#install-python3)
    - [Install Python Libraries](#install-python-libraries)
- [How to Run](#how-to-run)
    - [Run main.py](#run-mainpy)

## Requirements

### Install Python3
If you don't already have Python3 installed, please visit this link for instructions: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Install Python Libraries
After you have Python3 installed, run the following command in your Terminal or Console to install the required libraries, including Pandas, Numpy, and Matplotlib

```bash
python3 -m pip install pandas numpy matplotlib
```

## How to Run

### Run main.py
The `main.py` file shoould:

1. Setup the dataset: Read the public Rotten Tomatoes Reviews dataset and duplicate arbitrary rows and then shuffle the row orders to create the plagiarized dataset
2. Run KMP plagiarism detector
3. Run the LCSS plagiarism detector
4. Run the Rabin Karp plagiarism detector
5. Plot all processing time against the number of words

Run the `main.py` Python by executing the following command:

```python
python3 main.py
```
