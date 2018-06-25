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






###############################################################################

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
def clear_orcid_cache():
    from inspirehep.modules.orcid.cache import OrcidCache
    cache = OrcidCache('')
    cache.redis.delete(*cache.redis.keys('orcidcache:*'))


@hal.command()
@with_appcontext
def orcid_data_setup():
    # Add 1 orcid to a record.
    orcid = '0000-0002-7638-5686'
    record = get_record_by_pid('lit', 1498589)
    if 'orcid' not in str(record.json['authors'][0]['ids']).lower():
        add_orcid_to_record_author(record, u'{}'.format(orcid))
        create_orcid_token(orcid)

    # Add 100 orcids to another record.
    record = get_record_by_pid('lit', 1498185)
    if 'orcid' not in str(record.json['authors'][0]['ids']).lower():
        add_orcids_to_record(record)
        add_all_tokens_for_record(record)




import uuid
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

def add_orcids_to_record(record):
    data = deepcopy(record.json)

    authors = []
    for _ in range(100):
        authors.append(generate_author())
    data['authors'] = authors
    record.json = data
    db.session.add(record)
    db.session.commit()
    es.indices.refresh('records-institutions')


def _generate_random_numeric_string(len=4):
    chars = '0123456789'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(len))


def _generate_random_alphabetical_string(len=7):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(len))


def _generate_orcid():
    part1 = '0000'
    part2 = '0002'
    part3 = _generate_random_numeric_string()
    part4 = _generate_random_numeric_string(len=3)
    orcid = part1 + part2 + part3 + part4
    checksum = _generate_orcid_checksum(orcid)
    return '{}-{}-{}-{}{}'.format(
        part1, part2, part3, part4, checksum
    )


def _generate_orcid_checksum(orcid):
    total = 0
    for ch in orcid:
        digit = int(ch)
        total = (total + digit) * 2
    remainder = total % 11
    result = (12 - remainder) % 11
    return 'X' if result == 10 else str(result)


def generate_author():
    name = _generate_random_alphabetical_string()
    orcid = str(_generate_orcid())
    print(orcid)
    return {
        "affiliations":[
        ],
        "full_name": name,
        "full_name_unicode_normalized": name,
        "ids":[
           {"schema": "ORCID", "value": orcid},
           # {"schema": "ORCID", "value": "0000-0002-7638-5686"},
        ],
        "name_suggest":{
           "input":[name],
           "output": name,
           "payload":{
              "bai": name
           }
        },
        "name_variations":[name],
        "signature_block": name,
        "uuid": str(uuid.uuid4())
    }


def add_all_tokens_for_record(record):
    for author in record.json['authors']:
        for id_ in author['ids']:
            if id_['schema'] == 'ORCID':
                orcid = id_['value']
                create_orcid_token(orcid)
