# Data Stream Algorithms
Algorithms to process streams of data

## Part 1

## Part 2
This part handles the calculation of the 2nd moment of a set of words (a.k.a. *surprise number*). The dataset used is the NY times bag of words, available at the [UCI Machine Learning datasets repository](https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/). A [README](https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/readme.txt) file is available at the repository to explain the dataset's file format.

The program first checks if the dataset is present in the required folder (./datasets/nytimes.txt.gz), if not, the dataset is downloaded from the website and then processing can begin.

The 2nd moment is calculated in two ways: First, the exact moment is calculated by iterating line-by-line through the dataset, squaring the word counts and summing them. This approach yields the exact second moment for the dataset, at the cost of being a slower approach. The second approach uses the Alon-Matias-Szegedy algorithm for estimating the second moment of the dataset.

## Part 3
