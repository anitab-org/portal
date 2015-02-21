Architecture
============

This page will give you an overview about Systers Portal project architecture.
As any other Django project Portal organizes its functionality in several apps:

* **blog** - handles showing, adding, editing and deleting news and resources.
* **common** - generic functionality that can't be part of any other app.
  For example, landing, about, contact pages, generic models, helpers, mixins
  that are used in several apps.
* **community** - community and subcommunities functionality, like
  adding new communities, views and editing community profiles, showing, adding,
  editing and deleting community pages, managing permissions regarding each
  community.
* **membership** - handles showing, creating, approving and rejecting join
  requests to a community, removing and inviting users to become members of a
  community.
* **users** - showing and editing user personal profile.

The templates are placed inside ``systers_portal/templates`` folder organized
in a folder structure similar to the apps tree. Respectively the templates
location matches the views location.
