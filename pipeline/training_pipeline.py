from utils.common_functions import read_yaml
from config.path_config import *
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTraining


if __name__ == "__main__":
    # data_ingestion = DataIngestion(read_yaml(CONFIG_PATH), nrows=5000000)
    # data_ingestion.run()

    data_processor = DataProcessing(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()

    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()


