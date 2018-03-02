Here we have python files to compute the similarity.

py_hw_1_similarity.py computes cosine, edit-distance and jaccard similarity over all the tuples of the final dataset.
The implementations to compute the similarity are similar to those from tika-similarity but have been modified to find 
similarity within rows of same file instead of similarity between files.

Cosine similarity is computed on continuous features. We do column wise min-max normalization of the features before we 
compute cosine similarity. 

We discretize the features to compute edit-distance and jaccard similarity.

We get a smaller sample of the dataset. We compute similarity on this sample and test the same.  
