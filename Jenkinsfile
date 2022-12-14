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
        APP_NAMESPACE = 'ex-microservices'
        REDIS_HOST = 'redis'
    }
    
    stages {
        stage("Init") {
            steps {
                script {
                    gv = load "jenkins_scripts.groovy"
                }
            }
        }
        stage("Static Code Analysis"){
            steps{
                script {
                    dir('application') {
                        gv.analyze_code_with_sonar()
                    }
                }
            }
        }
        stage("Build Artifact") {
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
                    gv.test_docker_image(IMAGE_TAG,CONTAINER_NAME_TEST)
                }
            }
        }

        stage("Push to Repository") {
            steps {
                script {
                    echo "Pushing image to Dockerhub repository"
                    gv.login_to_docker(DOCKERHUB_CREDENTIALS_ID)
                    gv.push_to_docker(IMAGE_TAG)
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
                        def output = gv.provision_ec2_with_terraform()
                        EC2_URL_LOAD_BALANCER = output[0]
                        EC2_PUBLIC_IP_SERVER_1 = output[1]
                        EC2_PUBLIC_IP_SERVER_2 = output[2]

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

                    echo "Deploying docker image to EC2 Server 1"
                    gv.deploy_app_to_ec2("./server-cmds.sh",
                                        "./docker-compose.yaml",
                                        IMAGE_TAG,
                                        EC2_PUBLIC_IP_SERVER_1)

                    echo "Deploying docker image to EC2 Server 2"
                    gv.deploy_app_to_ec2("./server-cmds.sh",
                                        "./docker-compose.yaml",
                                        IMAGE_TAG,
                                        EC2_PUBLIC_IP_SERVER_2)

                    EC2_URL_LOAD_BALANCER.replace('"','')
                    echo "---------FOR DEVELOPMENT ENVIRONMENT-----------"
                    echo "URL: http://${EC2_URL_LOAD_BALANCER}/health"
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
                    sh "kubectl create namespace ${APP_NAMESPACE}"
                    gv.deploy_to_k8s("./kubernetes/redis.yaml")
                    gv.deploy_to_k8s("./kubernetes/microservice.yaml")
                    K8S_APP_URL_LOAD_BALANCER = gv.get_url_load_balancer_k8s(APP_NAME, APP_NAMESPACE)
                    K8S_APP_URL_LOAD_BALANCER.replace('"','')


                    echo "---------FOR PRODUCTION ENVIRONMENT----------"
                    echo "URL: http://${K8S_APP_URL_LOAD_BALANCER}/health"
                }
            }
        }
    }
    
    post {
        always {
            echo "############  END OF PIPELINE ############"
		}        
		success {
		    script {
		        echo "Pipeline executed successfully"
		    }
		}
		failure {
            echo "Error in pipeline. Please check"
		}
	}

}