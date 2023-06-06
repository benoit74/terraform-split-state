import subprocess
import yaml
import re
import sys
from dataclasses import dataclass

@dataclass
class MoveConfig:
    resource: str
    destination: str

with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

result = subprocess.run(['terraform', 'state', 'list'], cwd=config['original_path'], stdout=subprocess.PIPE)

resources = result.stdout.decode('utf-8').strip().split('\n')
if len(resources) == 0:
    print("No resources found in original path")
    sys.exit(3)

moves = []
conflict_detected = False
for resource in resources:
    selected_destination_name = None
    conflict = False
    for destination_name, destination_config in config['destinations'].items():
        if re.search(destination_config['regex'], resource):
            if selected_destination_name:
                print(f'conflict for {destination_name}: {selected_destination_name} + {destination_config["path"]}')  
                conflict = True  
                conflict_detected = True
            else:
                selected_destination_name = destination_name
    if not conflict:
        if selected_destination_name:
            moves.append(MoveConfig(resource=resource, destination=selected_destination_name))
            print(f'{resource} will move to {selected_destination_name}')
        else:
            print(f'{resource} will not move')

if len(moves) == 0:
    print("Nothing found to do")
    sys.exit(2)
else:
    print(f"{len(moves)} resources will be moved")

answer = input("Do you want to proceed? (type yes to continue) ")

if answer != "yes":
    print("Aborted")
    sys.exit(1)

print("Pulling original state locally")
with open("/tmp/orig_state.tfstate", "w") as state:
    subprocess.run(['terraform', 'state', 'pull'], cwd=config['original_path'], stdout=state)
for destination_name, destination_config in config['destinations'].items():
    print(f"Pulling state {destination_name} locally")
    with open(f"/tmp/{destination_name}.tfstate", "w") as state:
        subprocess.run(['terraform', 'state', 'pull'], cwd=destination_config['path'], stdout=state)

print("Moving resources locally")
for move in moves:
    print(f"Moving {move.resource} to {move.destination}")
    subprocess.run(['terraform', 'state', 'mv', "-state=/tmp/orig_state.tfstate", f"-state-out=/tmp/{move.destination}.tfstate", move.resource, move.resource], stdout=subprocess.PIPE)

print("Updating origin remote state")
subprocess.run(['terraform', 'state', 'push', f"/tmp/orig_state.tfstate"], cwd=config['original_path'], stdout=subprocess.PIPE)
for destination_name, destination_config in config['destinations'].items():
    print(f"Updating remote state {destination_name}")
    subprocess.run(['terraform', 'state', 'push', f"/tmp/{destination_name}.tfstate"], cwd=destination_config['path'], stdout=subprocess.PIPE)