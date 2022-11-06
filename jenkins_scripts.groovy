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
return this