pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage("Cloning from Github"){
            steps{
                echo "Cloning from Github repo"
                checkout scm
                // checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_token', url: 'https://github.com/JoeUzo/MLOps-Anime-Recommender.git']])
            }
        }

        stage("Making a virtual environment"){
            steps{
                echo "Making a virtual environment"
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }

        stage("DVC pull"){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIAlS')]){
                    sh '''
                    echo 'DVC pull...'
                    . ${VENV_DIR}/bin/activate  
                    dvc pull
                    '''
                }
            }
        }
    }

}