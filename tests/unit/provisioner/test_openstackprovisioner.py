#  Copyright (c) 2015-2016 Cisco Systems
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

import pytest
# from unittest.mock import Mock, MagicMock, patch

from molecule import config
from molecule import core
from molecule.provisioners import openstackprovisioner


@pytest.fixture()
def molecule_instance(temp_files):
    c = temp_files(fixtures=['molecule_openstack_config'])
    m = core.Molecule(dict())
    m.config = config.Config(configs=c)

    return m


@pytest.fixture()
def openstack_instance(molecule_instance, request):
    o = openstackprovisioner.OpenstackProvisioner(molecule_instance)

    return o

# Mock shade response
# def get_mock_server_config(*args, **kwargs):
#     with open('test/server.json', 'r') as json_mock:
#         return (json.loads(json_mock.read()))

# Mock shade class
# def get_mock_consulate(*args, **kwargs):
#     server = Mock()
#     server.health = Mock()
#     server.health.service = MagicMock(side_effect=get_mock_server_config)
#     return (server)


def test_keypair_name(openstack_instance):
    result_keypair_name = openstack_instance.get_keypair_name()

    import re
    assert re.match(r'molecule-[0-9a-fA-F]+', result_keypair_name)


def test_keyfile(openstack_instance):
    openstack_instance.get_keyfile()
    from os.path import expanduser
    home = expanduser("~")
    fileloc = home + "/.ssh/id_rsa"
    import os
    assert os.path.isfile(fileloc)
    assert os.path.isfile(fileloc + '.pub')


def test_name(openstack_instance):
    assert 'openstack' == openstack_instance.name


def test_get_provisioner(molecule_instance):
    assert 'openstack' == molecule_instance.get_provisioner().name


def test_instances(openstack_instance):
    assert 'molecule-openstack-01' == openstack_instance.instances[0]['name']


def test_ssh_user(openstack_instance):
    assert 'ubuntu' == openstack_instance.instances[0]['sshuser']


def test_security_groups(openstack_instance):
    assert 'default' == openstack_instance.instances[0]['security_groups'][0]
