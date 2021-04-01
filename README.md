Build docker image : $ docker build --tag similarity-check .

Run in detached mode : $ docker run -d -p 5000:5000 similarity-check

The first time to compute VisualSimilarity would take time to download model weights. In current version, I am using ResNet50 to extract image features.

There are three metric of similarity I am using: Cosine similarity, Pearson Coefficient, Euclidean distance.
