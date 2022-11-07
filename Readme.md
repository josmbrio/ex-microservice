# DevOps Exercise

Set the HOST variable with the URL of the Load Balancer. **(This specific URL is not available anymore)**

```yaml
HOST=ex-micro-lb-985408906.us-east-1.elb.amazonaws.com
```

Get the token. 

```bash
curl -X POST \
  http://${HOST}/auth

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzgwNzE2MSwianRpIjoiMTNhZTU2MzktMmIwZC00MmIxLWJkZjgtZmMwODI1NTFjYjBmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImV4LXVzZXIiLCJuYmYiOjE2Njc4MDcxNjEsImV4cCI6MTY2NzgwNzIyMX0.KihhwsQwPk6cSSxKOHEz-KdxDciECqtxH0o-ivXZRHE"
}
```

Set the token value to JWT variable.

```yaml
JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzgwNjM4NywianRpIjoiNTA3YjcxZWYtZGE2YS00NzA0LTk3ODItOTM5OWU5MzRmMTFkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImV4LXVzZXIiLCJuYmYiOjE2Njc4MDYzODcsImV4cCI6MTY2NzgwNjQ0N30.RHCk16HaVuWAy0upwY-Pu-sYdCpfaOzjKt5mK2H50MQ
```

Test the endpoint using **http** protocol instead of **https**:

```bash

curl -X POST    
   -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"    
   -H "X-JWT-KWY: ${JWT}"    
   -H "Content-Type: application/json"    
   -d '{ "message" : "This is a test", "to": "Juan Perez", "from": "Rita Asturia", "timeToLifeSec" : 45 }'     
   http://${HOST}/DevOps

{
    "message": "Hello Juan Perez your message will be send"
}
```

Test again with same JWT and the access should be expired. (JWT token is unique per transaction)

```bash

curl -X POST    
   -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"    
   -H "X-JWT-KWY: ${JWT}"    
   -H "Content-Type: application/json"    
   -d '{ "message" : "This is a test", "to": "Juan Perez", "from": "Rita Asturia", "timeToLifeSec" : 45 }'     
   http://${HOST}/DevOps

{
    "msg": "Token has expired"
}
```

Test again with different method and check that we get “ERROR” in response.

```bash
curl -X GET    
   -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"    
   -H "X-JWT-KWY: ${JWT}"    
   -H "Content-Type: application/json"    
   -d '{ "message" : "This is a test", "to": "Juan Perez", "from": "Rita Asturia", "timeToLifeSec" : 45 }'     
   http://${HOST}/DevOps

{
    "message": "ERROR"
}
```

## This exercise was done by using the following:

- **For application development:** Python with Flask, JWT and Redis.
- **For the pipeline there are several stages:**
    - **Static code analysis Stage:** SonarQube
    - **************Build artifact Stage**************: Docker
    - ************************************Test image Stage:************************************ Docker run
    - ****************Publishing artifact Stage:**************** DockerHub
    - ********************************Provision Infra to Dev Environment Stage:******************************** Terraform and AWS EC2
    - **Deploy in Dev Environment Stage:** Docker Compose
    - **Deploy in Prod Environment Stage:** Kubernetes in AWS EKS
    - I used Multibranch pipeline in Jenkins using Jenkinsfile
    

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5bc04f21-d8d6-47c5-ac7f-28c2bab25a4c/Untitled.png)

## Take into consideration:

- The microservice is contenerized and can be deployed in servers with Docker, Docker Compose and Kubernetes Cluster.
- I’m using a load balancer in dev environment with two EC2 instances. For production I’m using AWS EKS cluster (k8s).
- The infrastructure as code, in this case Terraform, is versionated in this repository.
- The pipeline code is stored in this repository in the following files:
    - Jenkinsfile
    - jenkins_scripts.groovy
- I’m using a AWS S3 Bucket to store the state file for Terraform.

## Improvements to be done:

- Configure healthchecks in k8s deployemnt for app
- Use Ansible in pipeline for installing and configuring docker in EC2 instances instead of linux commands
- Use a non-root user when buiding docker image
- Secure connection with HTTPS protocol.
