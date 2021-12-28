from paprika_connector.connectors.connector_factory import ConnectorFactory
from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.principle.principle_repository import PrincipleRepository
from snapsnare.repositories.policy.policy_repository import PolicyRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.fragment_assignment.fragment_assignment_repository import FragmentAssignmentRepository
from snapsnare.repositories.fragment.fragment_repository import FragmentRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.component.component_repository import ComponentRepository
# The section home has a posting component
# The role Admin has list permission, which is reflected by the principle admin|list (role|policy)
# This means that only if you have the role admin the posting component is shown
# The principle admin|list is connected to the fragment

# The section home has an activities component
# The role Admin has list/get permission, this will show the activities and edit/remove options
# list means the activities component is show.
# get means the edit option is shown
# other options are
# admin|get (means can edit every posting even if not owned)
# moderator|get-owner (needs tobe the owner of the activity)
# any|list



# The posting form is connected to the section
# For the Home section, the role Admin has list/get/set permission
# list means the form is show
# get means the data can be retrieved
# set means that the data can be created or updated.

session_username = 'janripke@gmail'
session_role = 'user'

ds = {
    'type': 'postgresql',
    'host': 'localhost',
    'db': 'snapsnare',
    'username': 'snapsnare_owner',
    'password': 'snapsnare_owner'
}


def fragment(connector, section_name, component_name):
    section_repository = SectionRepository(connector)
    fragment_repository = FragmentRepository(connector)
    fragment_assignment_repository = FragmentAssignmentRepository(connector)



    component_repository = ComponentRepository(connector)
    component = component_repository.find_by(component=component_name)

    section = section_repository.find_by(name=section_name)
    fragment = fragment_repository.find_by(stn_id=section['id'], cpt_id=component['id'])

    return {
        'id': fragment['id'],
        'uuid': fragment['uuid'],
        'section': {
            'id': section['id'],
            'uuid': section['uuid'],
            'name': section['name']
        },
        'component': {
            'id': component['id'],
            'uuid': component['uuid'],
            'name': component['component']
        }
    }


def get_assignments(connector, section_name, component_name):
    fragment_ = fragment(connector, section_name, component_name)
    fragment_assignment_repository = FragmentAssignmentRepository(connector)
    principle_repository = PrincipleRepository(connector)
    policy_repository = PolicyRepository(connector)
    role_repository = RoleRepository(connector)
    assignments = fragment_assignment_repository.list_by(fmt_id=fragment_['id'])
    results = []

    for assignment in assignments:
        principle = principle_repository.find_by(id=assignment['pce_id'])
        policy = policy_repository.find_by(id=principle['ply_id'])
        role = role_repository.find_by(id=principle['rle_id'])

        results.append(
            {
                'id': assignment['id'],
                'uuid': assignment['uuid'],
                'policy': {
                    'id': policy['id'],
                    'uuid': policy['uuid'],
                    'name': policy['policy']
                },
                'role': {
                    'id': role['id'],
                    'uuid': role['uuid'],
                    'name': role['role']
                }
            }
        )
    return results


connector = ConnectorFactory.create_connector(ds)
role_repository = RoleRepository(connector)
policy_repository = PolicyRepository(connector)
principle_repository = PrincipleRepository(connector)
fragment_assignment_repository = FragmentAssignmentRepository(connector)
fragment_repository = FragmentRepository(connector)
# activity = activity_repository.find_by_uuid('4a643c89-095c-4935-bc67-67458584316e')

assignments = get_assignments(connector, 'Home', 'activities')
for assignment in assignments:
    print(assignment)
exit(0)

fragments = fragment_repository.list()
for fragment in fragments:
    print(fragment)


assignments = fragment_assignment_repository.list()
for assignment in assignments:
    principle = principle_repository.find_by(id=assignment['pce_id'])
    assignment['principle'] = principle
    assignment['policy'] = policy_repository.find_by(id=principle['ply_id'])
    assignment['role'] = role_repository.find_by(id=principle['rle_id'])
    assignment['principle'] = principle

for assignment in assignments:
    print(assignment)

#
# principles = principle_repository.list()
# for principle in principles:
#     principle['policy'] = policy_repository.find_by(id=principle['ply_id'])
#     principle['role'] = role_repository.find_by(id=principle['rle_id'])
#     print(principle)








connector.connect()
connector.close()