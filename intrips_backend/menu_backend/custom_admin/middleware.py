from django.shortcuts import redirect
from django.urls import reverse

class ConfirmUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ???? ???????????? ?? ???????????????? � ?????????? ???
        if not request.user.is_authenticated:
            return self.get_response(request)

        # ? ??????? ? ??????????? ????????????? ?? ?????
        if request.user.is_staff or request.user.is_superuser:
            return self.get_response(request)

        # ???? ???????????? ??? ??????????? � ?????????? ???
        if request.user.is_confirmed:
            return self.get_response(request)

        # ?????????, ??? ???????????? ????? ????? VK
        if "vk-oauth2" in request.user.social_auth.values_list("provider", flat=True):
            confirm_url = reverse('waiting_confirmation')

            # ???? ??? ?? ???????? ????????, ?? ??????????
            if request.path == confirm_url:
                return self.get_response(request)

            return redirect(confirm_url)

        return self.get_response(request)
