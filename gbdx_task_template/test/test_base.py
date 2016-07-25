from unittest import TestCase
import os
import mock

from task_template import TaskTemplate, Task, InputPort, OutputPort


class MyBasicApp(TaskTemplate):

    task = Task("MyCustomTask")  # Create the Task
    task.properties = {
        "timeout": 9600,
        "isPublic": False
    }  # Update Properties

    task.first_port = InputPort(port_type="string", value="Hello")
    task.second_port = InputPort(value="~/mydata/input/")

    task.output_port = OutputPort(value="~/mydata/output/")

    def invoke(self):
        print "\n\tHello, World!"


MY_BASIC_APP_WF_DEF = {
    'tasks': [
        {
            'outputs': [
                {
                    'name': 'output_port'
                }
            ],
            'containerDescriptors': [
                {
                    'properties': {
                        'domain': 'default'
                    }
                }
            ],
            'taskType': 'MyCustomTask',
            'name': 'MyCustomTask',
            'inputs': [
                {
                    'name': 'second_port',
                    'value': '~/mydata/input/'
                },
                {
                    'name': 'first_port',
                    'value': 'Hello'
                },
                {
                    'name': 'source_bundle',
                    'value': '/Users/michaelconnor/Documents/SparkGeo/projects/Digital_Globe/TDGP/cloud-harness/source_bundle'
                }
            ]
        },
        {
            'outputs': [],
            'containerDescriptors': [
                {
                    'properties': {
                        'domain': 'default'
                    }
                }
            ],
            'taskType': 'StageDataToS3',
            'name': 'StageDataToS3_ed92cb3f-6b92-42a6-9776-202c0fa3c80e',
            'inputs': [
                {
                    'name': 'destination',
                    'value': 's3://gbd-customer-data/a157fdce-bb1d-42b3-96a9-66942896a787/e3c3bc3f-d406-4bd2-821d-a73a8badc9f5/MyCustomTask/output_port'
                },
                {
                    'source': 'MyCustomTask_7562bdd4-4cc7-4dcb-b3a7-ad6dd1f7bead:output_port',
                    'name': 'data'
                }
            ]
        }
    ],
    'name': 'e3c3bc3f-d406-4bd2-821d-a73a8badc9f5'
}


class BadTaskApp(TaskTemplate):
    task = Task("BadTask")  # Create the Task

    # No Input ports, bad schema.

    task.output_port = OutputPort(value="~/mydata/output/")

    def invoke(self):
        print "\n\tHello, World!"


class TestBase(TestCase):

    def setUp(self):
        self.task = Task("MyCustomTask")
        self.task.properties = {
            "timeout": 9600,
            "isPublic": False
        }  # Update Properties

        test_path = os.path.abspath(os.path.dirname(__file__))

        self.task.first_port = InputPort(port_type="string", value="Hello")
        self.task.second_port = InputPort(value=test_path)

        self.task.output_port = OutputPort(value=test_path)

        self.basic_inport_names = ['source_bundle', 'first_port', 'second_port']
        self.basic_outport_names = ['output_port']


def temp_env_var(**kwargs):
    """
    Decorator used for temporarily patching environment
    variables.
    :param func: The function to patch the env vars for.
    :param kwargs: key word args for env vars
    :return:
    """
    def wrap(func):

        def wrapped(self):
            """
            Temporarily set env vars from kwargs.
            :return:
            """
            with mock.patch.dict('os.environ', **kwargs):
                # Call the function
                func(self)
        return wrapped
    return wrap
