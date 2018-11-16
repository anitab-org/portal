from meetup.constants import *

groups_templates = {"community_member": COMMUNITY_MEMBER,
                    "community_moderator": COMMUNITY_MODERATOR,
                    "community_leader": COMMUNITY_LEADER}

community_member_permissions = [
    "add_meetup_rsvp",
    "add_supportrequest",
    "change_supportrequest",
    "delete_supportrequest"
]

community_moderator_permissions = community_member_permissions + [
    "add_meetup",
    "change_meetup",
    "delete_meetup",
    "add_meetup_location_member",
    "delete_meetup_location_member",
    "approve_meetup_location_joinrequest",
    "reject_meetup_location_joinrequest",
    "approve_meetup_location_meetuprequest",
    "reject_meetup_location_meetuprequest",
    "view_meetup_location_meetuprequest",
    "approve_meetup_comment",
    "reject_meetup_comment",
    "approve_support_request",
    "reject_support_request",
    "add_support_request_comment",
    "edit_support_request_comment",
    "delete_support_request_comment",
    "approve_support_request_comment",
    "reject_support_request_comment"
]

community_leader_permissions = community_moderator_permissions + [
    "change_meetuplocation",
    "add_meetuplocation",
    "add_meetup_location_moderator",
    "delete_meetup_location_moderator",
    "delete_meetuplocation",
]

group_permissions = {"community_member": community_member_permissions,
                     "community_moderator": community_moderator_permissions,
                     "community_leader": community_leader_permissions}
