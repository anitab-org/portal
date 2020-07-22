from meetup.constants import *

groups_templates = {"community_member": COMMUNITY_MEMBER,
                    "community_moderator": COMMUNITY_MODERATOR,
                    "community_leader": COMMUNITY_LEADER}

community_member_permissions = [
    "add_meetup_rsvp",
    "add_support_request"
]

community_moderator_permissions = community_member_permissions + [
    "add_meetups",
    "change_meetups",
    "delete_meetups",
    "approve_meetup_request",
    "reject_meetup_request",
    "view_meetup_request",
    "approve_support_request",
    "reject_support_request"
]

community_leader_permissions = community_moderator_permissions

group_permissions = {"community_member": community_member_permissions,
                     "community_moderator": community_moderator_permissions,
                     "community_leader": community_leader_permissions}
