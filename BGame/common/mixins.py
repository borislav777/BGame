from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from BGame import settings


class LoginRequired(auth_mixins.LoginRequiredMixin):
    login_url = reverse_lazy('login')


class StaffRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect('index')
        return super(StaffRequiredMixin, self).dispatch(request,*args, **kwargs)
