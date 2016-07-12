#  Copyright (c) 2015 Cisco Systems
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import testtools

from molecule.Provisioners import OpenstackProvisioner
import molecule.utilities
from molecule.core import Molecule
import yaml
from molecule.ansible_playbook import AnsiblePlaybook


class TestOpenstackProvisioner(testtools.TestCase):
    def setUp(self):
        super(TestOpenstackProvisioner, self).setUp()
        # Setup mock molecule
        self._mock_molecule = Molecule(dict())

        self.temp = '/tmp/test_config_load_defaults_external_file.yml'
        data = {
            'molecule': {
                'molecule_dir': '.test_molecule',
                'inventory_file': 'tests/ansible_inventory'
            },
            'openstack': {
                'keypair': 'TestKey',
                'keyfile': '~/.ssh/id_rsa',
                'instances': [
                    {'name': 'test1',
                     'image': 'ubuntu',
                     'flavor': 'm1.tiny',
                     'sshuser': 'ubuntu',
                     'security_groups': ['default']}
                ]
            },
            'ansible': {
                'config_file': 'test_config',
                'inventory_file': 'test_inventory'
            }
        }

        with open(self.temp, 'w') as f:
            f.write(yaml.dump(data, default_flow_style=True))

        self._mock_molecule._config.load_defaults_file(defaults_file=self.temp)

        self._mock_molecule._state = dict()

    def test_name(self):
        openstack_provisioner = OpenstackProvisioner(self._mock_molecule)
        # false values don't exist in arg dict at all
        self.assertEqual(openstack_provisioner.name, 'openstack')

    def test_get_provisioner(self):
        self.assertEqual(
            molecule.utilities.get_provisioner(self._mock_molecule).name,
            'openstack')
