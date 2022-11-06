def build_docker_image() {
    echo "Building image from Dockerfile"
    sh "docker build . -t ${IMAGE_TAG}"
}

return this