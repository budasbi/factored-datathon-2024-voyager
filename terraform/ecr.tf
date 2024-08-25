resource "aws_ecr_repository" "lambda_voyager_datathon_repo" {
  name                 = "voyager_datathon"
  force_delete         = true
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
  tags = {
  Name = var.default_tag }
}

output "repository_url" {
  value = aws_ecr_repository.lambda_voyager_datathon_repo.repository_url
}