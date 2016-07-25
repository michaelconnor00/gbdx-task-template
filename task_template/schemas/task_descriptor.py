import os
import json


class TaskDescriptor():
    with open(os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
            "task_schema.json")
    )) as json_file:
        td_schema = json.load(json_file)

    @staticmethod
    def get_schema():
        return TaskDescriptor.td_schema
