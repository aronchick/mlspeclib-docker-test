import logging
import uuid
from mlspeclib import MLObject

import random
import decimal


# Making this a class in case we want sub functions.
class StepExecution:
    input_params = {}  # noqa
    execution_params = {}  # noqa
    ml_object = MLObject()  # noqa
    logger = None  # noqa

    def __init__(self, input_params, execution_params):
        self.input_params = input_params
        self.execution_params = execution_params
        self.logger = logging.getLogger()

        # Execute all work in here.

        # Output input params & execution params
        if self.input_params is not None:
            self.logger.debug(f"Input params: {self.input_params}")

        if self.execution_params is not None:
            self.logger.debug(f"Execution params: {self.execution_params}")

    def execute(self, result_object_schema_type, result_object_schema_version):
        # Create Result object
        results_object = MLObject()
        results_object.set_type(
            schema_type=result_object_schema_type,
            schema_version=result_object_schema_version,
        )

        # Mocked up results
        return_dict = {
            "training_execution_id": str(uuid.uuid4()),
            "accuracy": float(random.randrange(0, 100)/100),
            "global_step": 10**random.randrange(2, 4),
            "loss": float(random.randrange(1000, 9999)/1000),
        }

        results_object.training_execution_id = return_dict["training_execution_id"]
        results_object.accuracy = return_dict["accuracy"]
        results_object.global_step = return_dict["global_step"]
        results_object.loss = return_dict["loss"]

        errors = results_object.validate() # noqa
        return results_object
