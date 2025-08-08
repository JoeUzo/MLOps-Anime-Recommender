import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import RAW_DIR, CONFIG_PATH
from utils.common_functions import read_yaml

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config, nrows=5000000):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.filenames = self.config['bucket_file_names']
        self.nrows = nrows

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("Data Ingestion initialized...")

    
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            logger.info(f'Downloading files...')
            for file_name in self.filenames:
                file_path = os.path.join(RAW_DIR, file_name)
                blob = bucket.blob(file_name)
                blob.download_to_filename(file_path)

                if file_name == 'animelist.csv':
                    data = pd.read_csv(file_path, nrows=self.nrows)
                    data.to_csv(file_path, index=False)

                    logger.info(f"Large file detected, downloading only {self.nrows} rows")
       
            logger.info(f'Successfully downloaded files from GCP')
        
        except Exception as e:
            logger.error(f'Failed to download files')
            raise CustomException(f'Failed to download file from GCP {e}')
    
    
    def run(self):
        try:
            logger.info('Starting Data Ingestion process')
            self.download_csv_from_gcp()
            logger.info("Data Ingestion Completed")
        
        except CustomException as ce:
            logger.error(f"Error in data ingestion process: {str(ce)}")
        
        finally:
            logger.info("Data ingestion process completed")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH), nrows=5000000)
    data_ingestion.run()