resource "aws_redshift_cluster" "example" {
  cluster_identifier = "voyager-cluster"
  database_name      = "gdelt_voyager"
  master_username    = var.REDSHIFT_USERNAME
  master_password    = var.REDSHIFT_PASSWORD
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  number_of_nodes = 1
  iam_roles = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.redshift_sg.id]
  cluster_subnet_group_name = aws_db_subnet_group.redshift_subnet_group.name
  publicly_accessible = true
}

resource "aws_db_subnet_group" "redshift_subnet_group" {
  name       = "my-db-subnet-group"
  subnet_ids = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id, aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
  tags = {
    Name = var.default_tag
  }
}