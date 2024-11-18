resource "aws_redshift_cluster" "analytics_cluster" {
  cluster_identifier = "fruitycert-cluster"
  node_type          = "ra3.xlplus"
  number_of_nodes    = 2
  master_username    = "admin"
  master_password    = "securepassword123"
  publicly_accessible = false
  tags = {
    Environment = "Production"
  }
}
