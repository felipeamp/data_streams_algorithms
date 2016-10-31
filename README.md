# Data Stream Algorithms
Algorithms to process streams of data

## Part 1

## Part 2
This part handles the calculation of the 2nd moment of a set of words (a.k.a. *surprise number*). The dataset used is the NY times bag of words, available at the [UCI Machine Learning datasets repository](https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/). A [README](https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/readme.txt) file is available at the repository to explain the dataset's file format.

The program first checks if the dataset is present in the required folder (./datasets/nytimes.txt.gz), if not, the dataset is downloaded from the website and the processing can begin.

The 2nd moment is calculated in two ways: First, the exact moment is calculated by iterating line-by-line through the dataset, squaring the word counts and summing them. This approach yields the exact second moment for the dataset, at the cost of being a slower approach. The second approach uses the Alon-Matias-Szegedy algorithm for estimating the second moment of the dataset. This algorithm computes a number of variables **X**, where **X.element** is the stream element that this variable refers to. and **X.value** is the number of times that the stream element occurs in the stream after **X**'s position is calculated. Both algorithms are explained in [1].

## Part 3

# References

[1] Leskovec, J. and Rajaraman, A. and Ullman, J.; **Mining of Massive Datasets**; 2nd ed., chapter 4, page 145;
URL: [http://infolab.stanford.edu/~ullman/mmds/ch4.pdf](http://infolab.stanford.edu/~ullman/mmds/ch4.pdf)
