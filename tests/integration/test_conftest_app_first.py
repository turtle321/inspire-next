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
"""
Ensure the `app` fixture (session-scoped), the `isolated_app` and the
`invenio_db.db` singleton work smoothly when `app` is run before
`isolated_app`.

Note: these tests assume the proper ordering between the `app` fixture
(session-scoped) and the `isolated_app` fixture. Thus this test module
is meant to be run alone, like:
pytest tests/integration/test_conftest/test_conftest_isolated_app_first.py
"""

from __future__ import absolute_import, division, print_function

from invenio_db import db
from invenio_oauthclient.models import User


def test_app_session(app):
    user = User()
    db.session.add(user)
    db.session.commit()
    id_ = user.id
    # Closing the session within app must not trigger the rollback.
    db.session.close()

    assert User.query.get(id_)


def test_app_nested_session(app):
    with db.session.begin_nested():
        user = User()
        db.session.add(user)
    db.session.commit()
    id_ = user.id
    # Closing the session within app must not trigger the rollback.
    db.session.close()

    assert User.query.get(id_)


def test_isolated_app(isolated_app):
    user = User()
    db.session.add(user)
    db.session.commit()
    id_ = user.id
    # Closing the session within isolated_app fixture must trigger the rollback.
    db.session.close()

    assert not User.query.get(id_)
