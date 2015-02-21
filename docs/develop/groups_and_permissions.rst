Groups and Permissions
======================

As it was previously discussed, each community is associated with 4 auth groups.
Each group implies a specific set of permissions:

* **Community: Content Contributor** -- a user from this group can:

    * add/change any tags and resource types
    * add/change Community news and resources
* **Community: Content Manager** -- a user from this group can do everything a
  user from **Community: Content Contributor** can do, plus:

    * delete any tags or resource types
    * delete Community news or resources
    * add/change/delete a Community page
    * approve/delete comments to Community posts (news, resources)
* **Community: User and Content Manager** -- a user from this group can do
  everything a user from **Community: Content Manager** can do, plus:

    * add/change/delete members of the Community
    * approve Community join requests
* **Community: Community Admin** -- a user from this group can do everything a
  user from **Community: User and Content Manager** can do, plus:

    * edit Community profile
