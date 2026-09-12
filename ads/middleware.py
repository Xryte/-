from django.utils import timezone
from analytics.models import PageView


class VisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path
        if path.startswith(('/static/', '/media/', '/admin/', '/favicon.ico')):
            return response

        try:
            PageView.objects.create(
                path=path,
                method=request.method,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                user=request.user if request.user.is_authenticated else None,
                visited_at=timezone.now(),
            )
        except Exception:
            pass

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')