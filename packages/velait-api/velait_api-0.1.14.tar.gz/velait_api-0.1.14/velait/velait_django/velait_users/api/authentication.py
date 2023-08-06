from rest_framework.authentication import BaseAuthentication


class MioSSOAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass

    @staticmethod
    def get_authorization_header(request):
        pass
