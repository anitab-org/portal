from django.conf.urls import url

from membership.views import (CommunityJoinRequestListView,
                              ApproveCommunityJoinRequestView,
                              RejectCommunityJoinRequestView,
                              RequestJoinCommunityView,
                              CancelCommunityJoinRequestView,
                              LeaveCommunityView, TransferOwnershipView,
                              RemoveCommunityMemberView)

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/join_requests/$',
        CommunityJoinRequestListView.as_view(),
        name="view_community_join_request_list"),
    url(r'^(?P<slug>[\w-]+)/join_requests/approve/(?P<pk>\d+)$',
        ApproveCommunityJoinRequestView.as_view(),
        name="approve_community_join_request"),
    url(r'^(?P<slug>[\w-]+)/join_requests/reject/(?P<pk>\d+)$',
        RejectCommunityJoinRequestView.as_view(),
        name="reject_community_join_request"),
    url(r'^(?P<slug>[\w-]+)/join/$', RequestJoinCommunityView.as_view(),
        name="request_join_community"),
    url(r'^(?P<slug>[\w-]+)/cancel/$',
        CancelCommunityJoinRequestView.as_view(),
        name="cancel_community_join_request"),
    url(r'^(?P<slug>[\w-]+)/leave/$', LeaveCommunityView.as_view(),
        name="leave_community"),
    url(r'^(?P<slug>[\w-]+)/transfer_ownership/$',
        TransferOwnershipView.as_view(), name="transfer_ownership"),
    url(r'^(?P<slug>[\w-]+)/remove/(?P<username>[\w.@+-]+)/$',
        RemoveCommunityMemberView.as_view(), name="remove_member"),
]
