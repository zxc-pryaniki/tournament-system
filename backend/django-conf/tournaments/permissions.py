from rest_framework import permissions

class IsAdminRoleOrReadOnly(permissions.BasePermission):
   #check for adm rights
    def has_permission(self, request, view):
        # if GET - allow to all
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # if POST, PUT, DELETE, check for adm rights
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '') == 'admin'
        )