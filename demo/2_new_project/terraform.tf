terraform {
  backend "s3" {
    bucket = "tf-bbe-1"
    key    = "2_new_project/terraform.tfstate"
    region = "eu-west-1"
  }
}

resource "null_resource" "move_to_2" {
}

locals {
    items = {
        "move_to_2_1" : {}
        "move_to_2_2" : {}
    }
}

resource "null_resource" "items" {
    for_each = local.items
}
