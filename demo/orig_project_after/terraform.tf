terraform {
  backend "s3" {
    key    = "orig_project/terraform.tfstate"
    region = "eu-west-1"
  }
}


resource "null_resource" "keep_me" {
}

locals {
    items = {
        "keep_me_1" : {}
        "keep_me_2" : {}
        "keep_me_3" : {}
    }
}

resource "null_resource" "items" {
    for_each = local.items
}
