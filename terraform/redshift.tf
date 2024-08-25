resource "aws_redshift_cluster" "voyager-cluster" {
  cluster_identifier = "voyager-cluster"
  database_name      = "gdelt_voyager"
  master_username    = var.REDSHIFT_USERNAME
  master_password    = var.REDSHIFT_PASSWORD
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  number_of_nodes = 1
  iam_roles = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.redshift_sg.id]
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group_2.name
  publicly_accessible = true
  depends_on = [ aws_redshift_subnet_group.redshift_subnet_group_2 ]
}


