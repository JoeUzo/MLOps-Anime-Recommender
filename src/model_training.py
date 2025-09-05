import joblib
import comet_ml
import numpy as np
import os
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from src.base_model import BaseModel
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from config.env_config import envconfig

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, data_path):
        self.data_path = data_path

        self.experiment = comet_ml.Experiment(
            api_key=envconfig.comet_ml_api,
            project_name="anime-recommender",
            workspace="joeuzo")
        
        logger.info("Model training and Comet ML initialized")

    def load_data(self):
        try:
            X_train_array = joblib.load(X_TRAIN_ARRAY)
            X_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_TEST)

            logger.info("Data loaded successfully")
            return X_train_array, X_test_array, y_train, y_test
    
        except Exception as e:
            logger.error(f"Failed to load data - {e}")
            raise CustomException(f"Failed to load data - {e}")


    def train_model(self):
        try:
            X_train_array, X_test_array, y_train, y_test = self.load_data()

            n_users = len(joblib.load(USER2USER_ENCODED))
            n_animes = len(joblib.load(ANIME2ANIME_ENCODED))

            base_model = BaseModel(config_path=CONFIG_PATH)
            model = base_model.RecommenderNet(n_users, n_animes)
            logger.info("Model architecture created successfully")


            start_lr = 0.0001
            min_lr = 0.0001
            max_lr = 0.001
            batch_size = 10000

            ramup_epochs = 5
            sustain_epochs = 0
            exp_decay = 0.8

            def lrfn(epoch):
                '''This functions helps to find the best learning rate for the model'''
                if epoch < ramup_epochs:
                    return (max_lr-start_lr)/ramup_epochs*epoch + start_lr
                elif epoch < ramup_epochs + sustain_epochs:
                    return max_lr
                else:
                    return(max_lr-min_lr) * exp_decay**(epoch-ramup_epochs-sustain_epochs) + min_lr 

            lr_callback = LearningRateScheduler(lambda epoch:lrfn(epoch), verbose=0)
            model_Checkpoint = ModelCheckpoint(filepath=CHECKPOINT_FILEPATH, save_weights_only=True, monitor="val_loss", mode="min", save_best_only=True)
            early_stopping = EarlyStopping(patience=3, monitor="val_loss", mode="min", restore_best_weights=True)
            my_callbacks = [model_Checkpoint, lr_callback, early_stopping]

            os.makedirs(os.path.dirname(CHECKPOINT_FILEPATH), exist_ok=True)
            os.makedirs(MODEL_DIR, exist_ok=True)
            os.makedirs(WEIGTHS_DIR, exist_ok=True)

            try:
                history = model.fit(
                    x=X_train_array,
                    y=y_train,
                    batch_size=batch_size, 
                    epochs=20,
                    verbose=1,
                    validation_data=(X_test_array, y_test),
                    callbacks=my_callbacks
                )
                model.load_weights(CHECKPOINT_FILEPATH)
                logger.info("Model trained successfully")

                for epoch in range(len(history.history["loss"])):
                    train_loss = history.history["loss"][epoch]
                    val_loss = history.history["val_loss"][epoch]
                    mse = history.history["mse"][epoch]
                    mae = history.history["mae"][epoch]

                    self.experiment.log_metric("train_loss", train_loss, step=epoch)
                    self.experiment.log_metric("val_loss", val_loss, step=epoch)
                    self.experiment.log_metric("mse", mse, step=epoch)
                    self.experiment.log_metric("mae", mae, step=epoch)

            except Exception as e:
                logger.error(f"Model training failed - {e}")
                raise CustomException(f"Model training failed - {e}")
            
            self.save_model_weights(model)

        except Exception as e:
            logger.error(f"Error during model Training process - {e}")
            raise CustomException(f"Error during model Training process - {e}")
        
    
    def extract_weights(self, layer_name, model):
        try:
            weight_layer = model.get_layer(layer_name)
            weights = weight_layer.get_weights()[0]
            weights = weights/np.linalg.norm(weights, axis=1).reshape((-1, 1))
            logger.info(f"Weights extracted from layer {layer_name} successfully")
            return weights
        
        except Exception as e:
            logger.error(f"Failed to extract weights from layer {layer_name} - {e}")
            raise CustomException(f"Failed to extract weights from layer {layer_name} - {e}")
        

    def save_model_weights(self, model):
        try:
            model.save(MODEL_PATH)
            logger.info(f"Model saved to {MODEL_PATH}")

            user_weights = self.extract_weights("user_embedding", model)
            anime_weights = self.extract_weights("anime_embedding", model)

            joblib.dump(user_weights, USER_WEIGHTS_PATH)
            joblib.dump(anime_weights, ANIME_WEIGTHS_PATH)

            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(ANIME_WEIGTHS_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)

            logger.info(f"Weights saved to {USER_WEIGHTS_PATH} and {ANIME_WEIGTHS_PATH}")

        except Exception as e:
            logger.error(f"Failed to save model weights - {e}")
            raise CustomException(f"Failed to save model weights - {e}")
        

if __name__ == "__main__":
    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()


        
    