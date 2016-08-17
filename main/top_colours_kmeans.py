from sklearn.cluster import KMeans

def k_means(num_clusters, array):
    print("starting top colours kmeans")
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(array)

    labels = kmeans.predict(array)

    return labels