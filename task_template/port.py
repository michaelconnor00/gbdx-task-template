import os
from urlparse import urlparse


class LocalPortValidationError(Exception):
    pass


class RemotePortValidationError(Exception):
    pass


class Port(object):
    """
    A Class to configure Port instances for the custom application
    """

    def __init__(self, port_type, direction, required, value):
        # Flag as input or output port
        self.__direction = direction
        self.__task_json = dict()

        # Load Task JSON attrs
        self.__task_json['name'] = None
        self.__task_json['type'] = port_type
        self.__task_json['required'] = required
        self.__task_json['description'] = 'cloud-harness'

        if port_type == 'directory':
            # For directory ports, there can be any combination of a local file system
            # location and an S3 location. ie: fs_loc = '/local/path/' && s3_loc = None, etc.
            # EXCEPT: they can't both be None

            # TODO value is not None doesn't make sense, validate s3 url? Ignore and raise error later?
            if direction == 'Output' and value is not None:
                self.stageToS3 = True

            remote_work_path = os.environ.get('REMOTE_WORK_PATH', None)

            if remote_work_path is not None:
                self.__local_filesystem_location = None

                self.__remote_filesystem_location = os.path.join(
                    remote_work_path, direction.lower(), "%(port_name)s"
                )
                self.value = self.__remote_filesystem_location
            else:

                self.__remote_filesystem_location = None

                if value == '.':  # Shortcut for current working directory
                    self.__local_filesystem_location = os.getcwd()
                else:
                    self.__local_filesystem_location = value

                self.value = self.__local_filesystem_location

        else:
            self.value = value

    def __str__(self):
        if self.port_type == 'directory':
            return '%s: %s -- dir: %s' % (self.name, self.value, self.__local_filesystem_location)
        else:
            return '%s: %s' % (self.name, self.value)

    def __eq__(self, other):
        return self.name == other.name

    @property
    def port_type(self):
        return self.__task_json['type']

    @property
    def direction(self):
        return self.__direction

    @property
    def name(self):
        return self.__task_json['name']

    @name.setter
    def name(self, value):
        self.__task_json['name'] = value

    @property
    def remote_path(self):
        return self.__remote_filesystem_location

    @remote_path.setter
    def remote_path(self, new_path):
        self.__remote_filesystem_location = new_path

    @property
    def json(self):
        return self.__task_json

    @staticmethod
    def is_port(obj):
        """Predicate for inspect.getmodules function"""
        return isinstance(obj, Port)

    @property
    def path(self):
        if self.__local_filesystem_location is None and \
                self.__remote_filesystem_location is None and \
                self.port_type == 'directory':
            raise ValueError('Directory ports must be provided with a location')

        # If remote is True then use it no matter what
        if self.__remote_filesystem_location is not None:
            actual_path = self.__remote_filesystem_location % {'port_name': self.name}
            return actual_path
        else:
            return self.__local_filesystem_location

    def list_files(self, extensions=None):
        """
        List the ports contents by file type or all.
        :param extensions: string extensions, single string or list of extensions.
        :return: A list of full path names of each file.
        """
        if self.port_type.lower() != 'directory':
            raise ValueError("Port type is not == directory")

        filesystem_location = self.path

        for root, dirs, files in os.walk(filesystem_location):
            if extensions is None:
                return [os.path.join(root, f) for f in files]
            elif not isinstance(extensions, list):
                extensions = [extensions]

            subset_files = []

            for f in files:
                for extension in extensions:
                    if f.lower().endswith(extension.lower()):
                        subset_files.append(os.path.join(root, f))
                        break
            return subset_files

    def list_tiff(self):
        raise NotImplementedError
        # return self.list_files(extensions=['.TIFF', '.TIF', '.tiff', '.tif'])

    def list_1b(self):
        raise NotImplementedError
        # return self.list_files(extensions=['.TIL', '.til'])

    def write(self, filename, data, overwrite=False):

        if self.__direction != 'Output':
            raise ValueError('Only Output ports can be written to.')

        if self.port_type != 'directory':
            raise ValueError('Only Directory ports can be written to.')

        if os.path.isabs(filename) and os.path.isfile(filename):
            raise ValueError('File name must be relative to the Ports path')

        write_file = os.path.join(self.path, filename)

        file_mode = 'a' if not overwrite else 'w'

        self._check_or_create_dir(write_file)

        with open(write_file, file_mode) as out_file:
            out_file.write(data)

    @staticmethod
    def _check_or_create_dir(full_path_to_file):
        if os.path.isabs(full_path_to_file) and os.path.isfile(full_path_to_file):
            return
        else:
            folder = os.path.dirname(full_path_to_file)
            if not os.path.isdir(folder):
                os.makedirs(folder)

    @staticmethod
    def is_valid_filesys(path):
        if os.path.isabs(path) and os.path.isdir(path) and \
                not os.path.isfile(path):
            return True
        else:
            raise LocalPortValidationError(
                'Port value %s is not a valid filesystem location' % path
            )

    @staticmethod
    def is_valid_s3_url(url):
        """Checks if the url contains S3. Not an accurate validation of the url"""
        scheme, netloc, path, _, _, _ = urlparse(url)

        port_except = RemotePortValidationError(
            'Port value %s is not a valid s3 location' % url
        )

        if len(scheme) < 2:
            raise port_except

        if 's3' in scheme or 's3' in netloc or 's3' in path:
            return True
        else:
            raise port_except


class InputPort(Port):
    """
    Helper Port subclass for Input Ports.
    """

    def __init__(self, value, port_type='directory', required=True):
        # TODO, need to allow source parameter for ports.
        super(InputPort, self).__init__(port_type, 'Input', required, value)


class OutputPort(Port):
    """
    Helper Port subclass for Output Ports.
    """

    def __init__(self, value=None, port_type='directory', required=True):
        super(OutputPort, self).__init__(port_type, 'Output', required, value)
