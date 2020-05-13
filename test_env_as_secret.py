import os
from pathlib import Path

os.environ["INPUT_test_environment_variables_override"] = Path("env_variables.yaml").read_text('utf-8')
os.system('python3 test_docker_image.py')
