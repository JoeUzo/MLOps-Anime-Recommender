import pandas as pd
import numpy as np
import joblib
from config.path_config import *


##### 1. Get Anime Frame #####
def get_anime(path_df, anime):
    df = pd.read_csv(path_df)
    if isinstance(anime,int):
        return df[df.anime_id == anime]
    elif isinstance(anime, str):
        return df[df.eng_version.str.lower() == anime.lower()]
    

##### 2. Get Synopsis #####
def get_synopsis(path_synopsis_df, anime):
    df = pd.read_csv(path_synopsis_df)
    try:
        if isinstance(anime,int):
            return df[df["MAL_ID"] == anime]["sypnopsis"].values[0]
        elif isinstance(anime, str):
            return df[df["Name"].str.lower() == anime.lower()]["sypnopsis"].values[0]
    except IndexError:
        return 'N/A'
    

##### 3. Content Recommendation #####
def find_similar_animes(name, path_df, path_synopsis_df, 
                        path_anime_weights, 
                        path_anime2anime_encoded, path_anime2anime_decoded, n=10,
                        return_dist=False, neg=False):

    anime_weights = joblib.load(path_anime_weights)
    anime2anime_encoded = joblib.load(path_anime2anime_encoded)
    anime2anime_decoded = joblib.load(path_anime2anime_decoded)
    df = pd.read_csv(path_df)
    synopsis_df = pd.read_csv(path_synopsis_df)

    try:
        index = get_anime(path_df, name).anime_id.values[0] #to get the natural index example >>> np.int64(2029)
        encoded_index = anime2anime_encoded.get(index)
        weights = anime_weights
        dists = np.dot(weights, weights[encoded_index]) # find the similarity between all the anime weights and the current anime weight
        sorted_dist = np.argsort(dists) # returns an array of indices that would sort `dists` in ascending order. In other words
        n = n+1
        if neg:
            closest = sorted_dist[:n]
        else:
            closest = sorted_dist[-n:]
        
        if return_dist:
            return dists, closest
        
        SimilarityArr = []
        for close in closest:
            decoded_id = anime2anime_decoded.get(close)
            anime_frame = get_anime(path_df, decoded_id)
            synopsis = get_synopsis(path_synopsis_df, decoded_id)
            anime_name = anime_frame["eng_version"].values[0]
            genre = anime_frame["Genres"].values[0]
            similarity = dists[close]
            
            SimilarityArr.append({
                "anime_id": decoded_id,
                "Name": anime_name,
                "Genres": genre,
                "Synopsis": synopsis,
                "similarity": similarity
            })
        
        Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
        return Frame[Frame.anime_id != index].drop(["anime_id"], axis=1).reset_index(drop=True)
        
    except Exception as e:
        print(f'Error Occured "{e}"')


##### 4. Find Similar Users #####
def find_similar_users(item_input, path_user_weights, 
                       path_user2user_encoded, path_user2user_decoded, n=10,
                       return_dist=False, neg=False):

    user_weights = joblib.load(path_user_weights)
    user2user_encoded = joblib.load(path_user2user_encoded)
    user2user_decoded = joblib.load(path_user2user_decoded)

    try:
        index = item_input
        encoded_index = user2user_encoded.get(index)

        weights = user_weights

        dists = np.dot(weights, weights[encoded_index])
        sorted_dists = np.argsort(dists) # returns an array of indices that would sort `dists` in ascending order. In other words

        n = n+1

        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]
        
        if return_dist:
            return dists, closest
        
        SimilarityArr = []

        for close in closest:
            similarity = dists[close]

            if isinstance(item_input, int):
                decoded_id = user2user_decoded.get(close)
                SimilarityArr.append({
                    "similar_users": decoded_id,
                    "similarity": similarity,
                })
        
        similar_users = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
        return similar_users[similar_users["similar_users"] != index].reset_index(drop=True)
    
    except Exception as e:
        print("Error Occured", e)


##### 5. Get User Preference #####
def get_user_preferences(user_id, path_df, path_df_r):
    df = pd.read_csv(path_df)
    df_r = pd.read_csv(path_df_r)

    all_animes_watched_dy_user = df_r[df_r["user_id"] == user_id]

    user_rating_percentile = np.percentile(all_animes_watched_dy_user.rating, 75) # only focusing on to rating by user
    animes_watched_dy_user = all_animes_watched_dy_user[all_animes_watched_dy_user.rating >= user_rating_percentile]

    top_animes_user = animes_watched_dy_user.sort_values(by="rating", ascending=False)["anime_id"].values
    anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version", "Genres"]]

    watched_df_rows = df[df["anime_id"].isin(all_animes_watched_dy_user["anime_id"].values)]
    watched_df_rows = watched_df_rows[["eng_version", "Genres"]]

    return anime_df_rows, watched_df_rows


##### 6. Get User Recommendations #####
def get_user_recommendations(similar_users, user_pref, path_df, path_synopsis_df, path_rating_df, n=10):
    df = pd.read_csv(path_df)
    # synopsis_df = pd.read_csv(path_synopsis_df)
    # rating_df = pd.read_csv(path_rating_df)

    recommended_animes = []
    anime_list = []

    for user_id in similar_users["similar_users"].values:
        pref_list = get_user_preferences(user_id, path_df, path_rating_df)[0]

        pref_list = pref_list[~pref_list["eng_version"].isin(user_pref[1]["eng_version"].values)]

        if not pref_list.empty:
            anime_list.append(pref_list["eng_version"].values)
        
    if anime_list:
        anime_list = pd.DataFrame(anime_list)

        sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts()).head(n)

        for i, anime_name in enumerate(sorted_list.index):
            # n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]
            # or
            # n_user_pref = sorted_list.at[anime_name, sorted_list.columns[0]]
            # or
            n_user_pref = sorted_list.iloc[i, 0]

            if isinstance(anime_name, str):
                frame = get_anime(DF_PATH, anime=anime_name)
                anime_id = frame.anime_id.values[0]
                genre = frame.Genres.values[0]
                synopsis = get_synopsis(path_synopsis_df, int(anime_id))

                recommended_animes.append({
                    "n":  n_user_pref,
                    "anime_name": anime_name,
                    "Genres": genre,
                    "Synopsis": synopsis
                })
    
    return pd.DataFrame(recommended_animes).head(n)

    