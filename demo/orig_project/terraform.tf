terraform {
  backend "s3" {
    bucket = "tf-bbe-1"
    key    = "orig_project/terraform.tfstate"
    region = "eu-west-1"
  }
}


resource "null_resource" "keep_me" {
}

resource "null_resource" "move_to_1" {
}

resource "null_resource" "move_to_2" {
}

locals {
    items = {
        "keep_me_1" : {}
        "keep_me_2" : {}
        "keep_me_3" : {}
        "move_to_1_1" : {}
        "move_to_1_2" : {}
        "move_to_1_3" : {}
        "move_to_2_1" : {}
        "move_to_2_2" : {}
    }
}

resource "null_resource" "items" {
    for_each = local.items
}
