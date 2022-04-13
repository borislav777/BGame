from django.contrib.auth import views as auth_view, authenticate, login


from django.http import HttpResponseRedirect

from django.urls import reverse_lazy, reverse
from django.views import generic as views

from BGame.auth_app.forms import UserRegisterForm, EditProfileForm
from BGame.auth_app.models import Profile, BGameUser
from BGame.games_rental.models import CustomerGameRent
from common.mixins import LoginRequired


class RegisterUserView(views.CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(reverse('index'))


class LoginUserView(auth_view.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super(LoginUserView, self).get_success_url()


class LogOutView(LoginRequired, auth_view.LogoutView):
    pass


class EditProfileVIew(LoginRequired, views.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user_id})


class DeleteProfileView(LoginRequired, views.DeleteView):
    model = BGameUser
    template_name = 'games_rental/delete_game.html'
    success_url = reverse_lazy('index')


class ChangeUserPasswordView(LoginRequired, auth_view.PasswordChangeView):
    template_name = 'accounts/change_password.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})


class ResetUserPasswordView(auth_view.PasswordResetView):
    template_name = 'accounts/reset_password.html'


class ResetUserPasswordDoneView(auth_view.PasswordResetDoneView):
    template_name = 'accounts/reset_password_done.html'


class ResetUserPasswordConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/reset_password_confirm.html'


class ResetUserPasswordCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/reset_password_complete.html'


class ProfileDetails(LoginRequired, views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rented_games = CustomerGameRent.objects.filter(user_id=self.kwargs.get('pk'))
        context.update({
            'rented_games': rented_games,
        })
        return context
