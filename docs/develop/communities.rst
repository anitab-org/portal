Communities
===========

Creating a community
--------------------

In order to create a new community, it is enough to fill out necessary fields
in a Community form.

When a new community is created, the following actions are triggered:

#. 4 new Groups are created using the name of the community
#. each new group is being assigned a set of usual Django permissions and row
   level permissions for the new Community object
#. the admin of the Community is being added to the Community admin group
#. the admin of the Community is being added to Community members

Suppose we create a community named *Systers* with an admin called *Foo*.  This 
is what is going to happen:

#. 4 new Group are created with the following names:
    * *Systers: Community Admin*
    * *Systers: User and Content Manager*
    * *Systers: Content Manager*
    * *Systers: Content Contributor*

   The naming of groups is important and helps identify a community with its
   auth Groups.
#. Groups are being assigned specific permissions. All permissions are listed 
   `in this file <https://github.com/systers/portal/blob/master/systers_portal/community/permissions.py>`_.
#. "Foo" user is added to the *Systers: Community Admin* group.
#. "Foo" user is added to *Systers* members.

Editing a community
-------------------

Community profile can be edited by changing any of the Community fields. On
community update, the actions are trigged only if name or admin have changed. 

If community name changed then:

#. community groups will be renamed according to new community name

If community admin changed then:

#. old community admin is removed from Community admin group
#. new community admin is added to Community admin group
#. new community admin is added to Community members

Suppose we rename the community from *Systers* to *Systers++*. Hence all the
community groups will be renamed:

* from *Systers: Community Admin* to *Systers++: Community Admin*
* from *Systers: User and Content Manager* to  *Systers++: User and Content 
  Manager*
* from *Systers: Content Manager* to *Systers++: Content Manager* 
* from *Systers: Content Contributor* to *Systers++: Content Contributor*

Suppose we change community admin from *Foo* user to *Bar* user. This is what 
is going to happen:

#. user *Foo* is removed from *Systers++: Community Admin* group
#. user *Bar* is added to *Systers++: Community Admin* group
#. user *Bar* is added to *Systers++* community members

Deleting a community
--------------------

When a community is deleted, all the associated Groups are also deleted.

Suppose we delete the community named *Systers*. In this case the following 
groups will be deleted:

* *Systers: Community Admin*
* *Systers: User and Content Manager*
* *Systers: Content Manager*
* *Systers: Content Contributor*
