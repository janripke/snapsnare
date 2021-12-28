from paprika_connector.connectors.connector_factory import ConnectorFactory
from snapsnare.repositories.activity.activity_repository import ActivityRepository




snapsnare_ds = {
  'type': 'postgresql',
  'host': 'localhost',
  'db': 'snapsnare',
  'username': 'snapsnare_owner',
  'password': 'snapsnare_owner'
}


connector = ConnectorFactory.create_connector(snapsnare_ds)

activity_repository = ActivityRepository(connector)
# activity = activity_repository.find_by_uuid('4a643c89-095c-4935-bc67-67458584316e')
activity = activity_repository.find_by(uuid='4a643c89-095c-4935-bc67-67458584316e')
if activity:
  content = activity.get('content')
  content = content.replace(chr(13), '\r')
  print(content)
connector.connect()
connector.close()