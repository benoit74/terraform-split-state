terraform {
  backend "s3" {
    bucket = "tf-bbe-1"
    key    = "1_new_project/terraform.tfstate"
    region = "eu-west-1"
  }
}

resource "null_resource" "move_to_1" {
}

locals {
    items = {
        "move_to_1_1" : {}
        "move_to_1_2" : {}
        "move_to_1_3" : {}
    }
}

resource "null_resource" "items" {
    for_each = local.items
}
