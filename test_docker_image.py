import os
import logging
from pathlib import Path
import yaml as YAML
import uuid
from io import StringIO
import sys

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdout_handler.setFormatter(formatter)
rootLogger.addHandler(stdout_handler)

for i in os.environ:
    rootLogger.debug(f"{i}:\t{os.environ.get(i)}")

parameters = {}
parameters = YAML.safe_load(Path("env_variables.yaml").read_text('utf-8'))
parameters["INPUT_input_parameters"] = (
    Path(".parameters") / "input" / "datasource.yaml"
).read_text('utf-8')

for param in parameters:
    rootLogger.debug(f"{i}:\t{param}")
    if isinstance(parameters[param], dict):
        env_value = YAML.safe_dump(parameters[param])
    else:
        env_value = parameters[param]

    os.environ[param] = env_value

os.environ["GITHUB_RUN_ID"] = str(uuid.uuid4())
os.environ["GITHUB_WORKSPACE"] = str(str(Path.cwd().resolve() / "tests"))
os.environ["VSCODE_DEBUGGING"] = "True"

parameters['GITHUB_RUN_ID'] = os.environ["GITHUB_RUN_ID"]
parameters["GITHUB_WORKSPACE"] = '/src'
parameters['INPUT_parameters_directory'] = '.parameters'
parameters['INPUT_schemas_directory'] = 'schemas'
parameters['INPUT_execution_parameters'] = 'execution/execution_parameters.yaml'

environment_vars = ""
for param in parameters:
    if isinstance(parameters[param], dict):
        env_value = YAML.safe_dump(parameters[param])
    else:
        env_value = parameters[param]
    environment_vars += f' -e "{param}={env_value}"'

exec_statement = f"docker run {environment_vars} aronchick/mlspeclib-action-docker:latest"
rootLogger.debug(exec_statement)
os.system(exec_statement)
