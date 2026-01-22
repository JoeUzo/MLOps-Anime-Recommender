pipeline {
    agent any
    // environment {

    // }

    stages {
        stage("Cloning from Github"){
            steps{
                echo "Cloning from Github repo"
                checkout scm
                // checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_token', url: 'https://github.com/JoeUzo/MLOps-Anime-Recommender.git']])
            }
        }
    }

}