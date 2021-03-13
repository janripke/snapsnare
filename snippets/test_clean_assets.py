import snapsnare
import os
from pathlib import Path

from paprika_connector.connectors.connector_factory import ConnectorFactory
from snapsnare.system import utils
from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.snap.snap_repository import SnapRepository

properties = {
    'current.dir': os.path.abspath(os.getcwd()),
    'package.dir': os.path.dirname(snapsnare.__file__),
    'home.dir': str(Path.home()),
    'app.name': 'snapsnare'
}

ds = utils.load_json(properties, 'snapsnare-ds.json')

connector = ConnectorFactory.create_connector(ds)

assets = []

activity_repository = ActivityRepository(connector)
acitvities = activity_repository.list()

for activity in acitvities:
    asset = {
        'uuid': activity['uuid'],
        'found': False
    }
    assets.append(asset)

snap_repository = SnapRepository(connector)
snaps = snap_repository.list()

for snap in snaps:
    asset = {
        'uuid': snap['uuid'],
        'found': False
    }


assets_folder = os.path.join(properties.get('package.dir'), 'assets')
items = os.listdir(assets_folder)
for item in items:
    for asset in assets:
        if asset['uuid'] == item:
            asset['found'] = True


for asset in assets:
    if asset['found'] == False:
        print(asset)