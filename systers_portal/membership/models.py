from django.db import models

from community.models import Community
from membership.constants import ALREADY_MEMBER, JOIN_REQUEST_EXISTS, OK
from users.models import SystersUser


class JoinRequestManager(models.Manager):
    """Model manager for JoinRequest model"""
    def create_join_request(self, user, community):
        """Create a join request by a user to a community.

        :param user: SystersUser object
        :param community: Community object
        :return: tuple (JoinRequest object, status), where Join Request can be
                 None and status is a string that conveys the result or reason
                 of the operation.
        """
        if user.is_member(community):
            return None, ALREADY_MEMBER
        if JoinRequest.objects.filter(user=user, community=community,
                                      is_approved=False).exists():
            return None, JOIN_REQUEST_EXISTS
        return JoinRequest.objects.create(user=user, community=community), OK

    def cancel_join_request(self, user, community):
        """Cancel a pending join request made by a user to a community.

        :param user: SystersUser object
        :param community: Community object
        :return: string status of canceling a request (OK if request was
                 canceled, ALREADY_MEMBER if user is a member of the community
                 and hence there shouldn't be any join requests,
                 NO PENDING_JOIN_REQUEST if there are no not approved requests)
        """
        if user.is_member(community):
            return ALREADY_MEMBER

        return user.delete_all_join_requests(community)


class JoinRequest(models.Model):
    """Model to represent a request to join a community by a user"""
    user = models.ForeignKey(SystersUser, related_name='created_by', on_delete=models.CASCADE)
    approved_by = models.ForeignKey(SystersUser, blank=True, null=True,
                                    related_name='approved_by', on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    objects = JoinRequestManager()

    def __str__(self):
        approval_status = "approved" if self.is_approved else "not approved"
        return "Join Request by {0} - {1}".format(self.user, approval_status)

    def approve(self):
        """Approve a join request."""
        if self.is_approved:
            return
        self.is_approved = True
        self.save()
