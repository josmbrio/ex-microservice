def test_code() {
    sh "python -m pytest"
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

return this