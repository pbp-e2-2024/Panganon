from django.utils.deprecation import MiddlewareMixin

class DisableCSRFForAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'): 
            setattr(request, '_dont_enforce_csrf_checks', True)