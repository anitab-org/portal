from meetup.constants import *

groups_templates = {"member": MEMBER,
                    "organizer": ORGANIZER}

member_permissions = [
    "change_meetup",
    "change_meetuplocation",
    "add_rsvp",
    "change_rsvp",
    "delete_rsvp",
    "add_comment",
    "change_comment",
    "delete_comment"
]

organizer_permissions = member_permissions + [
    "add_meetup",
    "delete_meetup",
    "add_meetuplocation",
    "delete_meetuplocation",
    "add_meetup_location_member",
    "delete_meetup_location_member",
    "add_meetup_location_organizer",
    "delete_meetup_location_organizer",
    "approve_meetup_location_joinrequest",
    "reject_meetup_location_joinrequest",
    "approve_meetup_comment",
    "reject_meetup_comment"
]

group_permissions = {"member": member_permissions,
                     "organizer": organizer_permissions}
