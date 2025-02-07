provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "proxy_server" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  security_groups = ["allow-proxy"]

  tags = {
    Name = "EnterpriseProxyManager"
  }
}
