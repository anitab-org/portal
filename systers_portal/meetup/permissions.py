from meetup.constants import *

groups_templates = {"member": MEMBER,
                    "organizer": ORGANISER,
                    "admin": ADMIN}

member_permissions = [
    "change_meetup",
    "change_meetuplocation",
    "add_rsvp",
    "change_rsvp",
    "delete_rsvp"
]

organizer_permissions = member_permissions + [
    "add_meetup",
    "delete_meetup",
    "delete_meetuplocation"
    "add_meetup_location_member",
    "delete_meetup_location_member",
    "add_meetup_location_organizer",
    "delete_meetup_location_organizer",
    "approve_meetup_location_joinrequest",
    "reject_meetup_location_joinrequest"
]

admin_permissions = organizer_permissions + [
    "add_meetuplocation"
]

group_permissions = {"member": member_permissions,
                     "organizer": organizer_permissions,
                     "admin": admin_permissions}
