resource "aws_vpc" "voyager_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = var.default_tag
  }
}

// Create a Subnet
resource "aws_subnet" "public_subnet_a" {
  vpc_id            = aws_vpc.voyager_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = var.default_tag
  }
  depends_on = [ aws_vpc.voyager_vpc ]
}

resource "aws_subnet" "public_subnet_b" {
  vpc_id            = aws_vpc.voyager_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = var.default_tag
  }
  depends_on = [ aws_vpc.voyager_vpc ]
}

resource "aws_subnet" "private_subnet_a" {
  vpc_id            = aws_vpc.voyager_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = var.default_tag
  }
  depends_on = [ aws_vpc.voyager_vpc ]
}
resource "aws_subnet" "private_subnet_b" {
  vpc_id            = aws_vpc.voyager_vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = var.default_tag
  }
  depends_on = [ aws_vpc.voyager_vpc ]
}

resource "aws_internet_gateway" "igw_redshift" {
  vpc_id     = aws_vpc.voyager_vpc.id
  depends_on = [aws_vpc.voyager_vpc]
  tags = {
    Name = var.default_tag
  }
  
}



resource "aws_redshift_subnet_group" "redshift_subnet_group_2" {
  name       = "redshift-subnet-group-2"
  subnet_ids = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id, aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]

  tags = {
    Name = var.default_tag
  }
}





resource "aws_security_group" "redshift_sg" {
  name_prefix = "redshift_sg"

  vpc_id = aws_vpc.voyager_vpc.id
  ingress = [{
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    self = false
    ipv6_cidr_blocks = []
    prefix_list_ids = []
    security_groups = []
    description = ""
  },
  {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    self = false
    ipv6_cidr_blocks = []
    prefix_list_ids = []
    security_groups = []
    description = ""
  }]
  tags = {
    Name = var.default_tag
  }
   egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.voyager_vpc.id
  tags = {
    Name = var.default_tag
  }
}

resource "aws_route" "internet_access" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw_redshift.id

}


resource "aws_route_table_association" "public_subnet_association_a" {
  subnet_id      = aws_subnet.public_subnet_a.id
  route_table_id = aws_route_table.public_route_table.id

}

resource "aws_route_table_association" "public_subnet_association_b" {
  subnet_id      = aws_subnet.public_subnet_b.id
  route_table_id = aws_route_table.public_route_table.id

}