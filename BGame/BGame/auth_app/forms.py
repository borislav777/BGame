from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from BGame.auth_app.models import Profile


class UserRegisterForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )
    picture = forms.ImageField()

    description = forms.CharField(

        widget=forms.Textarea(

            attrs={
                'rows': 3,

                'placeholder': 'Text',

            }
        ),
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            gender=self.cleaned_data['gender'],
            picture=self.cleaned_data['picture'],

            description=self.cleaned_data['description'],
            user=user,

        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'picture', 'description')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
