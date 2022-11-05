terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket = "ex-microservice-bucket"
    key = "terraform_dev/state.tfstate"
    region = "us-east-1"
  }
}