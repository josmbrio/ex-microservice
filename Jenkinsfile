#!/usr/bin/env groovy

pipeline {
    agent any
    
    stages {
        stage("Build") {
            steps {
                script {
                    echo "Entering build stage..."
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