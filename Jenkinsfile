pipeline {
    agent none 
    stages {
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
