from django.core.exceptions import PermissionDenied
from reuse.models import UserProfile

def user_is_seller(function):
    def wrap(request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        if profile.isSeller == True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
