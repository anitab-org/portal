from meetup.constants import *

groups_templates = {"member": MEMBER,
                    "organizer": ORGANIZER}

member_permissions = [
    "add_meetup_rsvp",
    "add_supportrequest",
    "change_supportrequest",
    "delete_supportrequest"
]

organizer_permissions = member_permissions + [
    "add_meetup",
    "change_meetup",
    "delete_meetup",
    "add_meetuplocation",
    "change_meetuplocation",
    "delete_meetuplocation",
    "add_meetup_location_member",
    "delete_meetup_location_member",
    "add_meetup_location_organizer",
    "delete_meetup_location_organizer",
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

group_permissions = {"member": member_permissions,
                     "organizer": organizer_permissions}
