# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import click

from flask.cli import with_appcontext

from .bulk_push import run

import random
import requests
from time_execution import time_execution


@click.group()
def hal():
    """Command related to pushing records to HAL."""


@hal.command()
@with_appcontext
def push():
    # run()
    ping_google()


@time_execution
def ping_google():
    status_code = random.choice([200, 200, 200, 200, 401, 403, 404, 500])
    response = requests.get('http://httpstat.us/{}'.format(status_code))
    response.raise_for_status()
    return response
