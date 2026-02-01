from rest_framework.permissions import BasePermission


def _get_user_from_request(request):
    return getattr(request, "user", None)

class CompanyPermissions(BasePermission):

    def has_permission(self, request, view):
        user = _get_user_from_request(request)

        if user is None or not getattr(user, "is_authenticated", False):
            return False

        if request.method == "GET":
            return user.has_perm("app.company_view")

        return user.has_perm("app.admin_view")

class TrainingPermissions(BasePermission):

    def has_permission(self, request, view):
        user = _get_user_from_request(request)

        return user.has_perm("app.training_register_view") or user.has_perm("app.admin_view")