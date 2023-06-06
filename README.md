Terraform split state
====

## Purpose

This tool is meant to split a Terraform state from one file to many. See demo for sample configuration.$

This tool probably does not work if workspaces are used.

This tool assumes that you might have direct access to Terraform state file from a local environment + that you have write access to `/tmp` folder on this local environment.

## Demo

Create an S3 bucket (empty preferably) to store your Terraform states and store its name in `shared_s3.tfbackend`

Setup AWS credentials to access this bucket (here we use an AWS_PROFILE, but it could be anything else - or even nothing if your environment is already ready)
```
export AWS_PROFILE=xxxx
```

```
cd tool
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
cd ..
```

Provision original infrastructure + init new workspaces
```
cd demo/orig_project
terraform init --backend-config=../shared_s3.tfbackend
terraform apply --auto-approve
cd ../1_new_project
terraform init --backend-config=../shared_s3.tfbackend
cd ../2_new_project
terraform init --backend-config=../shared_s3.tfbackend
cd ../orig_project_after
terraform init --backend-config=../shared_s3.tfbackend
cd ../..
```

Apply demo moves (as configured in config.yaml)
```
cd demo
python ../tool/main.py
cd ..
```

Check that everything has been moved with following actions which should all display nothing to do ("no changes"):
```
cd demo/orig_project_after
terraform plan
cd ../1_new_project
terraform plan
cd ../2_new_project
terraform plan
cd ../..
```


