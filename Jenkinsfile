pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'proven-tractor-467615-j1'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
        KUBECTL_AUTH_PLUGIN = '/usr/lib/google-cloud-sdk/bin'
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
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                    echo 'DVC pull...'
                    sh '''
                    . ${VENV_DIR}/bin/activate  
                    dvc pull
                    '''
                }
            }
        }

        stage("Build and push image to GCR"){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                    echo 'Build and push image to GCR...'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account -- key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet

                    docker build -t gcr.io/${GCP_PROJECT}/anime-recommender:latest .
                    docker push gcr.io/${GCP_PROJECT}/anime-recommender:latest
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes"){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                    echo 'Deploy to Kubernetes...'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                    gcloud auth activate-service-account -- key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}

                    gcloud container clusters get-credentials ml-app-cluster --region us-cental1
                    kubectl apply -f deployment.yaml
                    '''
                }
            }
        }

    }
}