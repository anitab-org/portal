groups_templates = {"content_contributor": "{0}: Content Contributor",
                    "content_manager": "{0}: Content Manager",
                    "user_content_manager": "{0}: User and Content Manager",
                    "community_admin": "{0}: Community Admin"}

content_contributor_permissions = [
    "add_tag",
    "change_tag",
    "add_resourcetype",
    "change_resourcetype",
    "add_community_news",
    "change_community_news",
    "add_community_resource",
    "change_community_resource",
]

content_manager_permissions = content_contributor_permissions + [
    "delete_tag",
    "delete_resourcetype",
    "delete_community_news",
    "delete_community_resource",
    "add_community_page",
    "delete_community_page",
    "approve_community_comment",
    "delete_community_comment",
]

user_content_manager_permissions = content_manager_permissions + [
    "add_community_systersuser",
    "change_community_systersuser",
    "delete_community_systersuser",
    "approve_community_joinrequest"
]

community_admin_permissions = user_content_manager_permissions + [
    "change_community",
]

group_permissions = {
    "content_contributor": content_contributor_permissions,
    "content_manager": content_manager_permissions,
    "user_content_manager": user_content_manager_permissions,
    "community_admin": community_admin_permissions
}
