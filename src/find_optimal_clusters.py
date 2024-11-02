import pandas as ps
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.metrics import silhouette_score


def find_optimal_clusters_kmeans(df, max_k, random_state=False):
    """
    Funkcja znajduje optymalna ilosc klastrów dla algorytmu KMeans.
    Input : df - dane, max_k - maksymalna ilosc klastrów, random_state - int do powtarzalności wyników
    Output : int - optymalna ilosc klastrów
    """
    scores = []
    for i in range(10):
        temp_scores = []
        for i in range(2, max_k):
            kmeans = KMeans(n_clusters=i, random_state=random_state).fit(df)
            sil_score = silhouette_score(df, kmeans.labels_)
            temp_scores.append(sil_score)
        scores.append(sum(temp_scores)/len(temp_scores))
    return scores.index(max(scores)) + 2


def find_optimal_clusters_SpectralClustering(df, max_k, random_state=False):
    """
    Funkcja znajduje optymalna ilosc klastrów dla algorytmu SpectralClustering.
    Input : df - dane, max_k - maksymalna ilosc klastrów, random_state - int do powtarzalności wyników
    Output : int - optymalna ilosc klastrów    """
    scores = []
    for i in range(10):
        temp_scores = []
        for i in range(2, max_k):
            spectral = SpectralClustering(n_clusters=i, random_state=random_state).fit(df)
            sil_score = silhouette_score(df, spectral.labels_)
            temp_scores.append(sil_score)
        scores.append(sum(temp_scores)/len(temp_scores))
    return scores.index(max(scores)) + 2
