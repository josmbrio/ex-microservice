#!/usr/bin/env groovy

pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS_ID = "docker-hub-repo"
        IMAGE_REPO_NAME_P1 = "josmbrio"
        IMAGE_REPO_NAME_P2 = "microservice-ex"
        IMAGE_REPO = "${IMAGE_REPO_NAME_P1}/${IMAGE_REPO_NAME_P2}"
        IMAGE_NAME = "py-1.0"
        IMAGE_TAG = "${IMAGE_REPO}:${IMAGE_NAME}"
        CONTAINER_NAME_TEST = "${IMAGE_REPO_NAME_P2}_test_pipeline"
    }
    
    stages {

        stage("Unit Test"){
            steps{
                script {
                    echo "Entering unit test stage"
                    sh "python -m pytest"
                }
            }
        }
        stage("Build") {
            steps {
                script {
                    echo "Entering build stage..."
                    echo "Building image from Dockerfile"
                    sh "docker build . -t ${IMAGE_TAG}"
                }
            }
        }
        
        stage("Test Image") {
            steps {
                script {
                    echo "Entering test stage"
                    sh "docker run -d -p 9000:9000 --name ${CONTAINER_NAME_TEST} ${IMAGE_TAG}"

                    sh "docker stop ${CONTAINER_NAME_TEST}"
                    sh "docker rm ${CONTAINER_NAME_TEST}"
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
            environment {
                AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
                APP_NAME = 'ex-microservice'
            }
            steps {
                script {
                    echo "Entering deployment stage"
                    sh 'envsubst < ./kubernetes/redis.yaml | kubectl apply -f -'
                    sh 'envsubst < ./kubernetes/microservice.yaml | kubectl apply -f -'


                }
            }
        }
    }
    
    post {
        always {
            echo "############  END OF PIPELINE ############"
		}        
		success {
			echo "Pipeline executed successfully"
		}
		failure {
            echo "Error in pipeline. Please check"
		}
	}

}