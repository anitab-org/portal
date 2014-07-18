from django.contrib.auth.models import Group, Permission
from south.signals import post_migrate


permissions = [
    "add_tag",
    "change_tag",
    "add_resourcetype",
    "change_resourcetype",
    # djangocms_text_ckeditor permissions
    "add_text",
    "change_text",
    "delete_text",
    # djangocms_picture permissions
    "add_picture",
    "change_picture",
    "delete_picture",
    # djangocms_video permissions
    "add_video",
    "change_video",
    "delete_video",
]


def create_generic_group(app, **kwargs):
    """Create a user group with generic permissions. Every user that is member
    of any other custom group, should become a member of this group too.

    :param app: string app's label
    """
    if app == "cms":
        verbosity = kwargs.get("verbosity")
        if verbosity > 0:
            print "Initializing data post_migrate"
        name = "Generic permissions"
        role, created = Group.objects.get_or_create(name=name)
        if verbosity > 1 and created:
            print "Creating group {0}".format(name)
        for perm in permissions:
            role.permissions.add(Permission.objects.get(codename=perm))
            if verbosity > 1:
                print "Permitting {0} to {1}".format(name, perm)
        role.save()


post_migrate.connect(create_generic_group)
