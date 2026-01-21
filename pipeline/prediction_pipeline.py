from config.path_config import *
from utils.helpers import *


def hybrid_recommendation(user_id, user_Weight=0.5, content_weight=0.5):

    ### User Recommendation
    similar_users = find_similar_users(user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED)
    user_pref = get_user_preferences(user_id, DF_PATH, RATING_DF)
    user_recommended_animes = get_user_recommendations(similar_users, user_pref, DF_PATH, SYNOPSIS_DF, RATING_DF)

    user_recommended_animes_list = user_recommended_animes["anime_name"].tolist()
    #### Content Recommendation
    content_recommended_animes = []
    for anime in user_recommended_animes_list:
        similar_animes = find_similar_animes(anime, DF_PATH, SYNOPSIS_DF, ANIME_WEIGTHS_PATH, ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED)

        if similar_animes is not None and not similar_animes.empty:
            content_recommended_animes.extend(similar_animes["Name"].tolist())
        else:
            print(f"No similar Anime to {anime} found")
    
    combined_scores = {}
    for anime in user_recommended_animes_list:
        combined_scores[anime] = combined_scores.get(anime, 0) + user_Weight

    for anime in  content_recommended_animes:
        combined_scores[anime] = combined_scores.get(anime,0) + content_weight

    sorted_animes = sorted(combined_scores.items(), key=lambda x:x[1], reverse=True)
    
    return [anime for anime, score in sorted_animes[:10]]

