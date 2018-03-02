Here we have python files to compute the similarity.

py_hw_1_similarity.py computes cosine, edit-distance and jaccard similarity over all the tuples of the final dataset.
The implementations to compute the similarity are similar to those from tika-similarity but have been modified to find
similarity within rows of same file instead of similarity between files.

Cosine similarity is computed on continuous features. We do column wise min-max normalization of the features before we
compute cosine similarity.

We discretize the features to compute edit-distance and jaccard similarity.

We get a smaller sample of the dataset. We compute similarity on this sample and test the same.  

Order of running.

1) Run py_build_features.py first

2) Run py_hw1_similarity.py second.

3) This would generate 3 csv files, namely - "cosine_similarity.csv", "edit_distance_similarity.csv", "jaccard_similarity.csv"
