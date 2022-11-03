#!/usr/bin/env groovy

pipeline {
    agent any
    environment {
        IMAGE_REPO = "josmbrio/microservice-ex"
        IMAGE_NAME = "py-1.0"
        DOCKER_TAG = "${IMAGE_REPO}:${IMAGE_NAME}"
    }
    
    stages {
        stage("Build") {
            steps {
                script {
                    echo "Entering build stage..."
                    echo "Building image from Dockerfile"
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-repo', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        sh "docker build . -t ${DOCKER_TAG}"
                        sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                        sh "docker push ${DOCKER_TAG}"
                    }
                    
                }
            }
        }
        
        stage("Test") {
            steps {
                script {
                    echo "Entering test stage"
                }
            }
        }

        stage("Provision Infrastructure") {
            steps {
                script {
                    echo "Entering provisioning stage"
                }
            }
        }

        stage("Deploy") {
            steps {
                script {
                    echo "Entering deployment stage"
                }
            }
        }
    }
}