# Data Stream Algorithms
Algorithms to process streams of data

## Part 1

## Part 2
This part handles the calculation of the 2nd moment of a set of words (a.k.a. *surprise number*). The dataset used is the Peter Norvig's Sherlock Holmes books in text format, available at Professor Laber's [Homepage](http://www-di.inf.puc-rio.br/~laber/ExpandedNrvg.zip).

The program first checks if the dataset is present in the required folder (./datasets), if not, the dataset is downloaded from the website and the processing can begin.

The 2nd moment is calculated in two ways: First, the exact moment is calculated by counting the number of ocurrences of each word, squaring them and summing the results. This approach yields the exact second moment for the dataset, at the cost of being impractical for extremely large or infinite streams of data. The second approach uses the Alon-Matias-Szegedy algorithm for estimating the second moment of the dataset. This algorithm computes a number of variables **X**, where **X.element** is the stream element that this variable refers to. and **X.value** is the number of times that the stream element occurs in the stream after **X**'s position is calculated. Both algorithms are explained in [1].

The variable selection is made using the *reservoir selection* technique, which consists in adding a new token to a sample array **S** of fixed size, with a chance of **s/n**, where **s = |S|**, is the number of variables in **S** and **n** is the number of tokens seen so far. When a variable is selected to be included in **S**, another variable must be removed. The choice of which variable is to be removed is done uniformly at random. A better explanation and the necessary proofs are presented in [1].

## Part 3

# References

[1] Leskovec, J. and Rajaraman, A. and Ullman, J.; **Mining of Massive Datasets**; 2nd ed., chapter 4, page 145;
URL: [http://infolab.stanford.edu/~ullman/mmds/ch4.pdf](http://infolab.stanford.edu/~ullman/mmds/ch4.pdf)
