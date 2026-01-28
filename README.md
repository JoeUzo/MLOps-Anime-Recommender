# Anime Recommender System

## Project Description
This project implements an Anime Recommender System that suggests anime to users based on various factors. It leverages machine learning techniques to provide personalized recommendations.

## Features
- Data ingestion and processing of anime datasets.
- Machine learning model training for recommendation generation.
- Prediction pipeline for real-time anime recommendations.
- Web application (Flask) for user interaction.
- CI/CD pipeline (Jenkins, DVC, Docker) for automated deployment.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Anime-Recommender.git
    cd Anime-Recommender
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```

4.  **Initialize DVC (Data Version Control):**
    ```bash
    dvc init
    dvc remote add -d local_cache .dvc/cache
    dvc pull
    ```

## Usage

### Running the Application Locally

To run the Flask application:

```bash
python app.py
```

Open your web browser and navigate to `http://127.0.0.1:5000`.

### Training the Model

To retrain the recommendation model:

```bash
python pipeline/training_pipeline.py
```

### Making Predictions

To use the prediction pipeline directly (e.g., for testing):

```python
from pipeline.prediction_pipeline import PredictionPipeline

# Example usage:
predictor = PredictionPipeline()
# results = predictor.predict(user_id=123) # Or similar input
# print(results)
```

## Project Structure

```
.dvcignore
.dockerignore
.gitignore
app.py
artifacts.dvc
deployment.yaml
Dockerfile
Jenkinsfile
requirements.txt
setup.py
config/
├── __init__.py
├── config.yaml
├── env_config.py
└── path_config.py
custom_jenkins/
└── Dockerfile
notebook/
└── recommender.ipynb
pipeline/
├── __init__.py
├── prediction_pipeline.py
└── training_pipeline.py
src/
├── __init__.py
├── base_model.py
├── custom_exception.py
├── data_ingestion.py
├── data_processing.py
├── logger.py
└── model_training.py
static/
└── styles.css
templates/
└── index.html
utils/
├── __init__.py
├── common_functions.py
└── helpers.py
```

## Technologies Used
- Python
- Flask
- Scikit-learn (or other ML libraries as needed)
- DVC (Data Version Control)
- Docker
- Jenkins
- HTML/CSS
