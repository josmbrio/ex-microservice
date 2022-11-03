#!/usr/bin/env groovy

pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS_ID = "docker-hub-repo"
        IMAGE_REPO = "josmbrio/microservice-ex"
        IMAGE_NAME = "py-1.0"
        IMAGE_TAG = "${IMAGE_REPO}:${IMAGE_NAME}"
    }
    
    stages {
        stage("Build") {
            steps {
                script {
                    echo "Entering build stage..."
                    echo "Building image from Dockerfile"
                    sh "docker build . -t ${IMAGE_TAG}"
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

        stage("Push to Repository") {
            steps {
                script {
                    echo "Pushing image to Dockerhub repository"
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS_ID}", passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    }
                    sh "docker push ${IMAGE_TAG}"
                    
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