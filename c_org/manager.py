#!/usr/bin/python3
#
# Copyright (C) 2018 Continuous Organisation.
# Author: Pierre-Louis Guhur <pierre-louis.guhur@laposte.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''c_org configuration manager'''

import logging
import os
import yaml
try:
    import cPickle as pickle
except:
    import pickle
import solc
from web3 import Web3
from web3.auto import w3
import c_org.utils as utils


class ContinuousOrganisationManager(object):

    def __init__(self, name):
        self.name = name
        self._config = None
        w3.eth.defaultAccount = w3.eth.accounts[0]

    @property
    def config(self):
        return self._config['c-org']

    def load(self):
        """ Read continuous organisation build file """
        filename = utils.get_build_file(self.name)
        logging.debug("Unpickling build file {}".format(filename))
        with open(filename, 'r') as f:
            c = pickle.load(f)
        self.contract = w3.eth.contract(abi=c['abi'],
                                         address=c['address'])
        return self.contract


    def parse(self):
        filename = utils.get_config_file(self.name)
        logging.debug("Parsing configuration filename {}".format(filename))
        with open(filename, 'r') as f:
            print("foo")
            self._config = yaml.load(filename)
        return self.config

    def build(self):
        # save build file
        store = {'abi': self.interface['abi'], 'address': self.address}
        filename = utils.get_build_file(self.name, check=False)
        with open(filename, 'wb+') as f:
            pickle.dump(store, f)

        # update config file and set up deploy flag
        filename = utils.get_config_file(self.name)
        with open(filename, 'r') as f:
            self._config = yaml.load(filename)
        self._config['c-org']['deployed'] = True
        with open(filename, 'w') as f:
            yaml.dump(c, filename)


    def compile(self):
        filename = utils.get_source_file(self.name, check=False)
        with open(filename, 'r') as f:
            source_code = f.read()
        compiled_sol = solc.compile_source(source_code)
        self.id, self.interface = compiled_sol.popitem()

    def deploy(self):
        tx_hash = w3.eth.contract(abi=self.interface['abi'],
                                  bytecode=self.interface['bin']).deploy()
        self.address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return self.address




class ConfigurationError(Exception):
    """
    Configuration could not be parsed or has otherwise failed to apply
    """
    pass