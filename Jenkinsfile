pipeline {
    agent none 
    stages {
        stage('Initialize') {
            def dockerHome = tool 'jenkins-docker'
            env.PATH = "${dockerHome}/bin:${env.PATH}"
        }
        stage('Build') {
            agent {
                docker {
                    image 'python:latest'
                }
            }
            steps {
                sh 'python setup.py install && python setup.py test'
            }
        }
    }
}
