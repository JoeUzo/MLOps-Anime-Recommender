import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
import sys

logger = get_logger(__name__)


class DataProcessing():
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.rating_df = None
        self.anime_df = None
        self.X_trian_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Data processing initialized")

    def load_data(self, usecols):
        try:
            self.rating_df = pd.read_csv(self.input_file, low_memory=True, usecols=usecols):
            logger.info("Data loaded successfully")
        except Exception as e:
            raise CustomException(f"Failed to load Data - {e}")
        
        
    def filter_users(self, min_rating=400):
        try:
            n_ratings = self.rating_df.user_id.value_counts()
            self.rating_df = self.rating_df[self.rating_df['user_id'].isin(n_ratings[n_ratings >=30].index)].copy()
            logger.info(f"Filtered users with at least {min_rating} ratings")

        except CustomException as e:
            raise CustomException(f"Failed to filter users", sys)
    
    def scale_ratings(self):
        try:
            min_rating = min(self.rating_df["rating"])
            max_rating = max(self.rating_df["rating"])
            
            self.rating_df["rating"] = self.rating_df["rating"].apply(lambda x: (x - min_rating)/(max_rating - min_rating)).values.astype(np.float64)
            logger.info("Ratings scaled successfully")
        except Exception as e:
            raise CustomException(f"Failed to scale ratings - {e}", sys)    
        
    
    def encode_data(self):
        try:
            ### Users
            user_id = self.rating_df["user_id"].unique().tolist()
            self.user2user_encoded = {x: i for i, x in  enumerate(user_id)}
            self.user2user_decoded = {i: x for i, x in  enumerate(user_id)}
            self.rating_df["user"] = self.rating_df["user_id"].map(self.user2user_encoded)

            ### Anime
            anime_id = self.rating_df["anime_id"].unique().tolist()
            self.anime2anime_encoded = {x: i for i, x in enumerate(anime_id)}
            self.anime2anime_decoded = {i: x for i, x in enumerate(anime_id)}
            self.rating_df["anime"] = self.rating_df["anime_id"].map(self.anime2anime_encoded)

            logger.info("Data encoded successfully")
        
        except Exception as e:
            raise CustomException(f"Failed to encode data - {e}", sys)
        
    