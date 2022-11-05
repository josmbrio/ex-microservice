variable cluster_name {}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.29.1"

  cluster_name = var.cluster_name
  cluster_version = "1.22"

  subnet_ids = module.ex-microservice-vpc.private_subnets
  vpc_id = module.ex-microservice-vpc.vpc_id

  tags = {
    environment = "production"
    application = "microservice"
  }


  eks_managed_node_groups = {
    dev = {
      min_size     = 1
      max_size     = 1
      desired_size = 1

      instance_types = ["t2.small"]
      capacity_type  = "SPOT"
    }
  }
}