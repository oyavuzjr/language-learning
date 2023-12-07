from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) or u.is_superuser:
                return True
            raise PermissionDenied
        return False
    return user_passes_test(in_groups, login_url='login')
