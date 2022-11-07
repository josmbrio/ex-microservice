def analyze_code_with_sonar() {}
    withCredentials([string(credentialsId: 'sonarqube-token', variable: 'TOKEN')]) {
        sh "/usr/local/sonar-scanner/bin/sonar-scanner \
            -Dsonar.projectKey=ex-microservices \
            -Dsonar.sources=. \
            -Dsonar.host.url=http://sonarqube-server:4000 \
            -Dsonar.login=${TOKEN}"
    }
}

def build_docker_image(image_tag) {
    echo "Building image from Dockerfile"
    sh "docker build . -t ${image_tag}"
}

def test_docker_image(image_tag,container_name_test) {
    sh "docker run -d -p 9000:9000 --name ${container_name_test} ${image_tag}"
    sh "docker stop ${container_name_test}"
    sh "docker rm ${container_name_test}"
}

def login_to_docker(credentials_id) {
    withCredentials([usernamePassword(credentialsId: "${credentials_id}", passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
    }
}

def push_to_docker(image_tag) {
    sh "docker push ${image_tag}"
}

def provision_ec2_with_terraform() {
    sh "terraform init"
    sh "terraform apply --auto-approve"
    load_balancer = sh(
        script: "terraform output dns_name_load_balancer",
        returnStdout: true
    ).toString().trim()
    server_1 = sh(
        script: "terraform output ec2_public_ip_server_1",
        returnStdout: true
    ).toString().trim()
    server_2 = sh(
        script: "terraform output ec2_public_ip_server_2",
        returnStdout: true
    ).toString().trim()

    def list = [load_balancer, server_1, server_2]

    return list
}

def deploy_app_to_ec2(start_script, docker_compose_file, image_tag, ip_address) {
    def shell_cmd = "bash ${start_script} ${image_tag}"
    def ec2_instance = "ec2-user@${ip_address}"
    def home_dir = "/home/ec2-user/"
    sh "scp -o StrictHostKeyChecking=no ${start_script} ${ec2_instance}:${home_dir}"
    sh "scp -o StrictHostKeyChecking=no ${docker_compose_file} ${ec2_instance}:${home_dir}"
    sh "ssh -o StrictHostKeyChecking=no ${ec2_instance} ${shell_cmd}"
}

def deploy_to_k8s() {
    sh 'envsubst < ./kubernetes/redis.yaml | kubectl apply -f -'
    sh 'envsubst < ./kubernetes/microservice.yaml | kubectl apply -f -'
}

def get_url_load_balancer_k8s(svc, namespace) {
    sh "kubectl get svc/${svc} -n ${namespace} -o jsonpath='{.status.loadBalancer.ingress[*].hostname}'"
}

def show_info_environment() {
    if (EC2_URL_LOAD_BALANCER != null) {
        echo "---------FOR DEVELOPMENT ENVIRONMENT-----------"
        echo "${EC2_URL_LOAD_BALANCER}"
        echo "${EC2_PUBLIC_IP_SERVER_1}"
        echo "URL: http://${EC2_URL_LOAD_BALANCER}/health"
    }
    if (K8S_APP_URL_LOAD_BALANCER != null) {
        echo "---------FOR PRODUCTION ENVIRONMENT-----------"
        echo "URL: http://${K8S_APP_URL_LOAD_BALANCER}"
    }
}

return this