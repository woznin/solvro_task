import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import src.find_optimal_clusters as foc

def plot_1(plot_type, ingredient_counts, category_counts, glass_counts):
    """
    Funckja do rysowania wykresów
    Input : rodzaj wykresu zczytany z dropdown menu
    Output : wykres
    """
    plt.figure(figsize=(10, 6))
    
    if plot_type == 'Ilość składników w drinkach':
        plt.bar(ingredient_counts.index, ingredient_counts.values, color='skyblue')
        plt.title('Rozkład ilości składników w drinkach')
        plt.xlabel('Ilość składników')
        plt.ylabel('Ilość Drinków')
        
    elif plot_type ==  'Ilość drinków w kategoriach':
        plt.bar(category_counts.index, category_counts.values, color='salmon')
        plt.title('Rozkład kategorii drinków')
        plt.xlabel('Kategoria')
        plt.ylabel('Ilość Drinków')
        
    elif plot_type == 'Ilość drinków w rodzajach szklanek':
        plt.bar(glass_counts.index, glass_counts.values, color='lightgreen')
        plt.title('Rozkład szklanek')
        plt.xlabel('Rodzaj szklanki')
        plt.ylabel('Ilość Drinków')
        plt.xticks(rotation=45)
        
    plt.grid(axis='y', linestyle='--')
    plt.show()


def plot_2(n_clusters, algorithm, scaler, df):
    """
    Funkcja do interaktywnych wykresów klastrowania
    Wejścia: wartości pobrane z widgetów (liczba klastrów, wybrany algorytm, czy standaryzować dane)
    Wyjścia: wykres algorytmu klastrowania
    """
    if algorithm == 'KMeans':
        model = KMeans(n_clusters=n_clusters, random_state=1)
    elif algorithm == 'Spectral Clustering':
        model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', random_state=0)
    
    # an option to disable the standarization (we only have 1 feature scalable to points higher than 1 so one may not find it necessary)
    if scaler:
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df)
        pca = PCA(n_components=10) 
        df_pca = pca.fit_transform(df_scaled)

    # Dimensionality reduction (otherwise we have 100+ columns)
    else:
        pca = PCA(n_components=10) 
        df_pca = pca.fit_transform(df)

    labels = model.fit_predict(df_pca)
    sil_score = silhouette_score(df_pca, labels)
    dbi_score = davies_bouldin_score(df_pca, labels)
    ch_score = calinski_harabasz_score(df_pca, labels)

    print(f"Dla {n_clusters} klastrów, wyniki: \nSilhouette : {sil_score}\nDavies Bouldin : {dbi_score}\nCalinski Harabasz : {ch_score}")
    plt.figure(figsize=(10, 10))
    plt.scatter(df_pca[:, 0], df_pca[:, 1], c=labels, cmap='viridis')
    plt.xlabel('Kompnent główny 1')
    plt.ylabel('Komponent główny 2')
    plt.title(f'{algorithm} z {n_clusters} klastrami')
    plt.show()


def plot_3(df):

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    pca = PCA(n_components=10)
    df_pca = pca.fit_transform(df_scaled)

    best_k = foc.find_optimal_clusters_kmeans(df_pca, 10, 1)
    kmeans = KMeans(n_clusters=best_k)
    labels = kmeans.fit_predict(df_pca)
    sil_score = silhouette_score(df_pca, labels)
    dbi_score = davies_bouldin_score(df_pca, labels)
    ch_score = calinski_harabasz_score(df_pca, labels)
    print(f"Dla najlepszej ilości klastrów - {best_k}, wyniki: \nSilhouette : {sil_score}\nDavies Bouldin : {dbi_score}\nCalinski Harabasz : {ch_score}")
    df['cluster'] = labels
    plt.figure(figsize=(10, 10))
    plt.scatter(df_pca[:, 0], df_pca[:, 1], c=labels, cmap='viridis')
    plt.xlabel('Kompnent główny 1')
    plt.ylabel('Komponent główny 2')
    plt.title('Optymalne KMeans Clustering')
    plt.show()

def plot_4(plot_type, df, df_loaded):
    """
    Funckja do rysowania wykresów
    Input : rodzaj wykresu zczytany z dropdown menu
    Output : wykres
    """
    
    if plot_type == 'Rozkład koktajli w klastrach':
        category_columns = df.columns[df.columns.isin(df_loaded['category'])]
        cluster_category_counts = df.groupby('cluster')[category_columns].sum()
        cluster_category_counts.plot(kind='bar', stacked=True, colormap='tab20', edgecolor='black', figsize=(12, 10))
        plt.title('Liczba drinków z każdej kategorii w poszczególnych klastrach')
        plt.xlabel('Klaster')
        plt.ylabel('Liczba drinków')
        plt.legend(title='Kategoria koktajlu',loc='upper right')

        
    elif plot_type ==  'Rozkład szklanek w klastrach':
        glass_columns = df.columns[df.columns.isin(df_loaded['glass'])]
        cluster_glass_counts = df.groupby('cluster')[glass_columns].sum()
        cluster_glass_counts.plot(kind='bar', stacked=True, colormap='tab20', edgecolor='black', figsize=(12, 10))
        plt.title('Liczba szklanek z każdej kategorii w poszczególnych klastrach')
        plt.xlabel('Klaster')
        plt.ylabel('Liczba szklanek')
        plt.legend(title='Rodzaj szklanki',loc='upper right')
        
    elif plot_type == 'Rozkład grup składników w klastrach':
        ingredient_counts = df.groupby(['cluster', 'ingredient_count']).size().unstack(fill_value=0)
        ingredient_counts.plot(kind='bar', stacked=True, colormap='tab20', edgecolor='black', figsize=(12, 10))
        plt.title('Liczba koktajli podzielona na ilość składników w klastrach')
        plt.xlabel('Klaster')
        plt.ylabel('Liczba koktajli')
        plt.legend(title='N-składnikowe koktajle',loc='upper right')


    plt.grid(axis='y', linestyle='--')
    plt.show()