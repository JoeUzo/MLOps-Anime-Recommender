from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense, Activation, BatchNormalization
from utils.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded configuration successfully from config.yaml.")

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise CustomException(f"Failed to load configuration - {e}")
    

    def RecommenderNet(self, n_users, n_animes):
        try:
            embedding_size = self.config["model"]["embedding_size"] 

            user = Input(name="user", shape=[1])
            user_embedding = Embedding(
                name="user_embedding",
                input_dim=n_users,
                output_dim=embedding_size
            )(user)

            anime = Input(name="anime", shape=[1])
            anime_embedding = Embedding(
                name="anime_embedding",
                input_dim=n_animes,  
                output_dim=embedding_size  
            )(anime)

            
            x = Dot(name="dot_product", normalize=True, axes=2)(
                [user_embedding, anime_embedding]
            )
            x = Flatten()(x)
            x = Dense(
                1,
                kernel_initializer="he_normal"  
            )(x)
            x = BatchNormalization()(x)
            x = Activation("sigmoid")(x)
        
            model = Model(inputs=[user, anime], outputs=x)
            model.compile(
                loss=self.config["model"]["loss"],
                metrics=self.config["model"]["metrics"],
                optimizer=self.config["model"]["optimizer"]
            )

            logger.info("Model compiled successfully")
            return model

        except Exception as e:
            logger.error(f"Error in building the model: {e}")
            raise CustomException(f"Failed to build the model - {e}")