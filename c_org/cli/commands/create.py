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

'''c_org apply command line'''

import logging
import os
import sys



from c_org.cli.command import C_OrgCommand
from c_org.manager import ContinuousOrganisationManager


class C_OrgCreate(C_OrgCommand):

    def __init__(self):
        super().__init__(command_id='create',
                         description='Create a Continuous Organisation')

    def run(self):
        self.parser.add_argument('--c-org',
                                 help='Continuous Organisation\'s name',
                                 type=str)
        self.parse_args()

        self.run_command()

    def run_command():
        c_org_manager = ContinuousOrganisationManager(name)
        c_org_manager.parse()
        c_org_manager.compile()
        c_org_manager.deploy()
        c_org_manager.build()