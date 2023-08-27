import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
  
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
  
ratings = pd.read_csv("rating.csv")
ratings.head()
  
anime = pd.read_csv("anime.csv")
anime.head()

n_ratings =len(ratings)
n_anime = len(ratings['anime_id'].unique())
n_users = len(ratings['user_id'].unique())

#print(f"num of ratings: {n_ratings}")
#print(f"num of anime: {n_anime}")
#print(f"num of users: {n_users}")

user_freq =ratings[['user_id', 'anime_id']].groupby('user_id').count().reset_index()
user_freq.columns = ['user_id','n_ratings']
#print(user_freq.head())

mean_rating = ratings.groupby('anime_id')[['rating']].mean()

lowest_rated = mean_rating['rating'].idxmin()
anime.loc[anime['anime_id'] == lowest_rated]

highest_rated = mean_rating['rating'].idxmax()
anime.loc[anime['anime_id'] == highest_rated]

ratings[ratings['anime_id'] == highest_rated]
ratings[ratings['anime_id'] == lowest_rated]

anime_stats = ratings.groupby('anime_id')[['rating']].agg(['count', 'mean'])
anime_stats.columns = anime_stats.columns.droplevel()

from scipy.sparse import csr_matrix

def create_matrix(df):
    N = len(df['user_id'].unique())
    M = len(df['anime_id'].unique())

    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    anime_mapper = dict(zip(np.unique(df["anime_id"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    anime_inv_mapper = dict(zip(list(range(M)), np.unique(df["anime_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    anime_index = [anime_mapper[i] for i in df['anime_id']]

    X = csr_matrix((df["rating"],(anime_index, user_index)), shape=(M,N))

    return X, user_mapper, anime_mapper, user_inv_mapper, anime_inv_mapper

X, user_mapper, anime_mapper, user_inv_mapper, anime_inv_mapper = create_matrix(ratings)

from sklearn.neighbors import NearestNeighbors

def find_similar(anime_id, X, k, metric='cosine', show_distance=False):

    neighbours_id = []

    anime_ind = anime_mapper[anime_id]
    anime_vec = X[anime_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    anime_vec = anime_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(anime_vec, return_distance=show_distance)

    for i in range(0,k):
        n = neighbour.item(i)
        neighbours_id.append(anime_inv_mapper[n])
    neighbours_id.pop(0)
    return neighbours_id

anime_names = dict(zip(anime['anime_id'], anime['name']))

#change so we can enter anime naem instead of the id 
anime_id = 32

similar_ids = find_similar(anime_id, X, k= 10)

anime_name = anime_names[anime_id]

print(f"Since you watched {anime_name}")
for i in similar_ids:
    print(anime_names[i])







