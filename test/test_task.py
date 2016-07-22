import json
import os
from test.test_base import TestBase


class TestTask(TestBase):

    def test_task_json(self):
        print '=====', os.environ.get('REMOTE_WORK_PATH')
        task_dict = json.loads(self.task.json())

        self.assertEqual(task_dict['name'], 'MyCustomTask')

        # Check Ports
        self.assertEqual(len(task_dict['inputPortDescriptors']), 3)
        for port in task_dict['inputPortDescriptors']:
            self.assertIn(port['name'], self.basic_inport_names)

        self.assertEqual(len(task_dict['outputPortDescriptors']), 1)
        for port in task_dict['outputPortDescriptors']:
            self.assertIn(port['name'], self.basic_outport_names)

        # Check Properties
        task_properties = task_dict['properties']
        self.assertEqual(task_properties['timeout'], 9600)
        self.assertEqual(task_properties['isPublic'], False)

    def test_task_validate(self):
        print '=====', os.environ.get('REMOTE_WORK_PATH')
        self.assertTrue(self.task.is_valid())
