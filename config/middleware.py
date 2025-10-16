from django.utils.deprecation import MiddlewareMixin

class DisableCSRFMiddlewareForAPI(MiddlewareMixin):
    def process_request(self, request):
        # Skip CSRF for API routes only
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
