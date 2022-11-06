#!/usr/bin/env groovy

def gv
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

        AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
        APP_NAME = 'ex-microservice'
    }
    
    stages {
        stage("Init") {
            steps {
                script {
                    gv = load "jenkins_scripts.groovy"
                }
            }
        }
        stage("Unit Test"){
            steps{
                script {
                    echo "Entering unit test stage"
                    dir('application') {
                        gv.test_code()
                    }
                }
            }
        }
        stage("Build") {
            steps {
                script {
                    echo "Entering build stage..."
                    gv.build_docker_image(IMAGE_TAG)
                }
            }
        }
        
        stage("Test Image") {
            steps {
                script {
                    echo "Entering test stage"
                    test_docker_image(IMAGE_TAG,CONTAINER_NAME_TEST)
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

        stage("Provisioning Infra Development)") {
            when {
                expression {
                    return env.GIT_BRANCH == "features"
                }
            }
            steps {
                script {
                    echo "Provision Development Infra"
                    dir('terraform/dev'){
                        sh "terraform init"
                        sh "terraform apply --auto-approve"
                        EC2_PUBLIC_IP_SERVER_1 = sh(
                            script: "terraform output ec2_public_ip_server_1",
                            returnStdout: true
                        ).toString().trim()

                        echo "Waiting for EC2 instance(s) to initialize"
                        sleep(time: 120, unit: "SECONDS")
                    }
                }
            }
        }
        stage("Deploy in Development") {
            when {
                expression {
                    return env.GIT_BRANCH == "features"
                }
            }
            steps {
                script {
                    echo "Deployment in EC2 instance with Docker Compose"

                    echo "Deploying docker image to EC2"
                    echo "${EC2_PUBLIC_IP_SERVER_1}"

                    def shellCmd = 'bash server-cmds.sh ${IMAGE_TAG}'
                    def ec2Instance = "ec2-user@${EC2_PUBLIC_IP_SERVER_1}"

                    sh "scp -o StrictHostKeyChecking=no server-cmds.sh ${ec2Instance}:/home/ec2-user/"
                    sh "scp -o StrictHostKeyChecking=no docker-compose.yaml ${ec2Instance}:/home/ec2-user/"
                    sh "ssh -o StrictHostKeyChecking=no ${ec2Instance} ${shellCmd}"
                }
            }
        }
        stage("Deploy in Production") {
            when {
                expression {
                    return env.GIT_BRANCH == "main"
                }
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