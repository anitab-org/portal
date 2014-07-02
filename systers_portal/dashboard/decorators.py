from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import available_attrs
from django.utils.functional import wraps

from dashboard.models import Community


def membership_required(model, *lookup_vars, **kwargs):
    """Decorator for views that checks that the user is a member of the
    community by passing the Community model directly or a model which has a
    reference to that community, i.e. the model object belongs to that
    community.

    >>> from dashboard.models import Resource
    >>> membership_required(Community, "id__exact", "id")
    <function decorator at 0x...>
    >>> membership_required(Resource, "id__exact", "id")
    <function decorator at 0x...>

    :param model: Community model or model that has a community field
                  referencing Community model
    :param lookup_vars: string field lookup name and a string variable name
                        passed to the view
    :returns: inner decorator function
    :raises ValueError: if the value of the second element from request kwargs
                        is missing or None
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            lookup, varname = lookup_vars
            value = kwargs.get(varname, None)
            if value is None:
                raise ValueError("The lookup value can't be 'None'.")
            obj = get_object_or_404(model, **{lookup: value})
            systeruser = request.user.systeruser
            user_communities = systeruser.member_of_community.filter(
                members=systeruser)
            obj_community = obj if model == Community else obj.community
            if obj_community in user_communities:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


def admin_required(model, *lookup_vars, **kwargs):
    """Decorator for views that checks that the user is admin of the community
    by passing the Community model directly or a model which has a reference to
    that community, i.e. the model object belongs to that community.

    >>> from dashboard.models import News
    >>> admin_required(Community, "id__exact", "id")
    <function decorator at 0x...>
    >>> admin_required(News, "id__exact", "id")
    <function decorator at 0x...>

    :param model: Community model or model that has a community field
                  referencing Community model
    :param lookup_vars: string field lookup name and a string variable name
                        passed to the view
    :returns: inner decorator function
    :raises ValueError: if the value of the second element from request kwargs
                        is missing or None
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            lookup, varname = lookup_vars
            value = kwargs.get(varname, None)
            if value is None:
                raise ValueError("The lookup value can't be 'None'.")
            obj = get_object_or_404(model, **{lookup: value})
            systeruser = request.user.systeruser
            obj_community = obj if model == Community else obj.community
            community_admin = obj_community.community_admin
            if community_admin == systeruser:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator


def authorship_required(model, *lookup_vars, **kwargs):
    """Decorator for views that checks that the user is the author of the model.

    >>> from dashboard.models import News, Resource
    >>> authorship_required(News, "id__exact", "id")
    <function decorator at 0x...>
    >>> authorship_required(Resource, "id__exact", "id")
    <function decorator at 0x...>

    :param model: model object with author field referencing SysterUser model
    :param lookup_vars: string field lookup name and a string variable name
                        passed to the view
    :returns: inner decorator function
    :raises ValueError: if the value of the second element from request kwargs
                        is missing or None
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            lookup, varname = lookup_vars
            value = kwargs.get(varname, None)
            if value is None:
                raise ValueError("The lookup value can't be 'None'.")
            obj = get_object_or_404(model, **{lookup: value})
            systeruser = request.user.systeruser
            obj_author = obj.author
            if obj_author == systeruser:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator
