import os
import json

from jsonschema import validate as validate_schema

from gbdx_task_template.schemas.task_descriptor import TaskDescriptor
from gbdx_task_template.port import Port, InputPort, OutputPort


class Task(object):
    """
    Class to encapsulate the Task configuration
    """

    def __init__(self, name, docker_image=None):
        self.__task_json = {
            "containerDescriptors": [{
                "type": "DOCKER",
                "properties": {"image": "tdgp/sdk_application_runner:latest"}
            }],
            "description": "GBDX SDK Custom Task",
            "inputPortDescriptors": [],
            "outputPortDescriptors": [],
            "properties": {"timeout": 7200},
            "name": name
        }

        if docker_image is not None:
            self.__task_json['containerDescriptors'][0]['properties']['image'] = docker_image

        # Add default source bundle port
        port_name = "source_bundle"
        dest_path = os.path.join(os.getcwd(), port_name)
        srcbundle = InputPort(value=dest_path)
        srcbundle.name = port_name
        self.source_bundle = srcbundle

    def __setattr__(self, key, value):
        # Check if key already exists
        if Port.is_port(value):
            value.name = key
            self.add_port(value)

        super(Task, self).__setattr__(key, value)

    @property
    def src_path(self):
        return self.source_bundle.value

    @property
    def name(self):
        return self.__task_json['name']

    @name.setter
    def name(self, value):
        self.__task_json['name'] = value

    @property
    def properties(self):
        return self.__task_json['properties']

    @properties.setter
    def properties(self, value):
        self.__task_json['properties'].update(value)

    @property
    def input_ports(self):
        return self.__task_json['inputPortDescriptors']

    @property
    def output_ports(self):
        return self.__task_json['outputPortDescriptors']

    @property
    def ports(self):
        return self.__task_json['inputPortDescriptors'], self.__task_json['outputPortDescriptors']

    def json(self):
        return json.dumps(self.__task_json, cls=CustomEncoder, indent=2)

    def add_port(self, new_port):
        if not Port.is_port(new_port):
            raise TypeError("Task ports must be of type Port")

        if new_port.direction == 'Input':
            self.__task_json['inputPortDescriptors'].append(new_port)
        elif new_port.direction == 'Output':
            self.__task_json['outputPortDescriptors'].append(new_port)

    def is_valid(self, remote=False):
        schema = TaskDescriptor().get_schema()
        validate_schema(json.loads(self.json()), schema)

        if remote:
            # Ignore output ports as gbdxtools will override value.
            ports = [
                port for port in self.input_ports if port.port_type == 'directory'
                ]
            for port in ports:
                # Will raise exception if the port is invalid.
                port.is_valid_s3_url(port.value)
        else:
            all_ports = self.ports[0] + self.ports[1]
            ports = [
                port for port in all_ports if port.port_type == 'directory' and port.name != 'source_bundle'
                ]
            for port in ports:
                # Will raise exception if the port is invalid.
                port.is_valid_filesys(port.value)

        return True


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # For Port instances
        if isinstance(obj, Port):
            return obj.json
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
