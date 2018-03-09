# user groups
CONTENT_CONTRIBUTOR = "{0}: Content Contributor"
CONTENT_MANAGER = "{0}: Content Manager"
USER_CONTENT_MANAGER = "{0}: User and Content Manager"
COMMUNITY_ADMIN = "{0}: Community Admin"

# community
DEFAULT_COMMUNITY_ACTIVE_PAGE = 'news'

COMMUNITY_PRESENCE_CHOICES = [
    ('Facebook Page', 'Facebook Page'),
    ('Facebook Group', 'Facebook Group'),
    ('Twitter', 'Twitter'),
    ('Instagram', 'Instagram'),
    ('Other', 'Other')
]

COMMUNITY_TYPES_CHOICES = [
    ('Affinity Group', 'Affinity Group (Latinas in Computing, LGBT, etc'),
    ('Special Interest Group',
     'Special Interest Group (Student Researchers, Systers in Government,'
     'Women in Cyber Security, etc) '),
    ('Email list', 'Email list (using Mailman3)'),
    ('Other', 'Other')
]

COMMUNITY_CHANNEL_CHOICES = [
    ('Existing Social Media Channels ', 'Existing Social Media Channels '),
    ('Request New Social Media Channels ',
     'Request New Social Media Channels '),
]

YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No')
]

# STATUS values for RequestCommunity
ORDER_NULL = "order_null"
SLUG_ALREADY_EXISTS = "slug_already_exists"
ORDER_ALREADY_EXISTS = "order_already_exists"
OK = "success"

# messages for the approval of a community request
ORDER_NULL_MSG = "Order is not set, Please choose an order."
ORDER_ALREADY_EXISTS_MSG = "Order {0} already exists, please choose an order other than {1}."
SLUG_ALREADY_EXISTS_MSG = "Slug {0} already exists, please choose a slug other than {1}."
SUCCESS_MSG = "Community created successfully!"
