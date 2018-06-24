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
    run()




@hal.command()
@with_appcontext
def send_some_metrics():
    ping_google()



@time_execution
def ping_google():
    status_code = random.choice([200, 200, 200, 200, 401, 403, 404, 500])
    response = requests.get('http://httpstat.us/{}'.format(status_code))
    response.raise_for_status()
    return response





@hal.command()
@with_appcontext
def orcid_data_setup():
    orcid = '0000-0002-7638-5686'
    record = get_record_by_pid('lit', 1498589)
    add_orcid_to_record_author(record, u'{}'.format(orcid))
    create_orcid_token(orcid)







from copy import deepcopy
from invenio_records.models import RecordMetadata
from invenio_pidstore.models import PersistentIdentifier
from invenio_db import db
from inspirehep.utils.record_getter import get_db_record
from invenio_search.api import current_search_client as es
from invenio_oauthclient.models import RemoteToken, User, RemoteAccount, UserIdentity


def get_record_by_pid(pid_type, pid_value):
    return RecordMetadata.query.filter(RecordMetadata.id == PersistentIdentifier.object_uuid)\
        .filter(PersistentIdentifier.pid_value == str(pid_value),
                PersistentIdentifier.pid_type == pid_type).one()


def add_orcid_to_record_author(record, orcid):
    data = deepcopy(record.json)
    if not 'orcid' in str(data['authors'][0]['ids']).lower():
        data['authors'][0]['ids'].append({u'schema': u'ORCID', u'value': orcid})
        record.json = data
        db.session.add(record)
        db.session.commit()
        es.indices.refresh('records-institutions')


def create_orcid_token(orcid):
    identity = UserIdentity.query.filter_by(id=orcid, method='orcid').first()
    if not identity:
        user = User()
        db.session.add(user)
        db.session.commit()
        identity = UserIdentity(
            id=orcid,
            method='orcid',
            id_user=user.id
        )
        db.session.add(identity)
        db.session.commit()
    user = identity.user
    RemoteToken.create(
        user_id=user.id,
        client_id='myclientid',
        token='mytoken',
        secret=None,
        extra_data={
            'orcid': orcid,
            'full_name': 'Myname',
            'allow_push': True,
        }
    )
    db.session.commit()


# orcid = '0000-0002-7638-5686'
# record = get_record_by_pid('lit', 1498589)
# add_orcid_to_record_author(record, u'{}'.format(orcid))
# create_orcid_token(orcid)
