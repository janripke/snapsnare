import json
from datetime import datetime
from flask import current_app
from snapsnare.repositories.jammer.jammer_repository import JammerRepository
from snapsnare.repositories.icecast_status.icecast_status_repository import IcecastStatusRepository
from markupsafe import Markup


def load():
    connector = current_app.connector
    jammer_repository = JammerRepository(connector)
    icecast_status_repository = IcecastStatusRepository(connector)

    jammers = jammer_repository.find_by(order_by='id desc') or {}

    if jammers:
        jammers['jammers'] = Markup(jammers.get('jammers'))
        dt_created_at = datetime.strptime(jammers.get('created_at'), '%Y-%m-%d %H:%M:%S.%f')
        jammers['created_at_formatted'] = dt_created_at.strftime('%d %B om %H:%M')

    if not jammers:
        jammers['jammers'] = 'Geen actieve jammers'

    icecast_status = icecast_status_repository.find_by(order_by='id desc')
    if icecast_status:
        icecast_status['source'] = json.loads(icecast_status['source'])

    jammers['icecast_status'] = icecast_status
    return jammers
