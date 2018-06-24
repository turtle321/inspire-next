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

web: gunicorn inspirehep.wsgi -c gunicorn.cfg
#worker: celery worker -E -A inspirehep.celery --loglevel=INFO --workdir="${VIRTUAL_ENV}" --pidfile="${VIRTUAL_ENV}/worker.pid" --purge -Q celery,migrator,harvests,orcid_push
worker: HTTP_PROXY=127.0.0.1:8080 celery worker -E -A inspirehep.celery --loglevel=INFO --workdir="${VIRTUAL_ENV}" --pidfile="${VIRTUAL_ENV}/worker.pid" --purge -Q celery,migrator,harvests,orcid_push
#workermon: celery flower -A inspirehep.celery


cache: redis-server
# beat: celery beat -A inspirehep.celery --loglevel=INFO --workdir="${VIRTUAL_ENV}" --pidfile="${VIRTUAL_ENV}/worker_beat.pid"
# mathoid: node_modules/mathoid/server.js -c mathoid.config.yaml

# ES new port
#indexer: elasticsearch -Dcluster.name="inspire" -Ddiscovery.zen.ping.multicast.enabled=false -Dpath.data="$VIRTUAL_ENV/var/data/elasticsearch"  -Dpath.logs="$VIRTUAL_ENV/var/log/elasticsearch"
indexer: elasticsearch -Dcluster.name="inspire" -Ddiscovery.zen.ping.multicast.enabled=false -Dpath.data="$VIRTUAL_ENV/var/data/elasticsearch"  -Dpath.logs="$VIRTUAL_ENV/var/log/elasticsearch" -Dhttp.port=9255 -Dtransport.tcp.port=9355
