from django.utils.deprecation import MiddlewareMixin


class IPMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    