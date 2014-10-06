from django.test import TestCase
from django.contrib.auth.models import Group

from community.permissions import groups_templates
from community.utils import create_groups


class CommunityTestCase(TestCase):
    def test_create_groups(self):
        name = "Foo"
        groups = create_groups(name)
        expected_group_names = []
        for key, group_name in groups_templates.items():
            expected_group_names.append(group_name.format(name))
        group_names = []
        for group in groups:
            group_names.append(group.name)
        self.assertListEqual(expected_group_names, group_names)

        community_groups = Group.objects.filter(name__startswith=name)
        self.assertListEqual(list(community_groups), groups)
