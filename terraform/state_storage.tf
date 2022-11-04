terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket = "ex-microservice-bucket"
    key = "terraform/state.tfstate"
    region = "us-east-1"
  }
}