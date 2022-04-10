from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from BGame.games_rental.models import Game, Review, CustomerGameRent, Slider, Platform, Genre
from common.amount import get_amount


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ('likes', 'views')


class EditGameForm(AddGameForm):
    pass


class ReviewGameForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'game')


class RentGameForm(forms.ModelForm):
    PRICE_PER_DAY = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('game').status == 'Coming Soon':
            self.fields['date'].initial = self.initial.get('game').release_date

    class Meta:
        model = CustomerGameRent
        exclude = ('user', 'game', 'amount')
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'readonly': True,

                }
            ),
            'return_date': forms.SelectDateWidget(

            ),

        }

    def clean(self):
        user_budget = self.initial.get('user').profile.budget
        if self.cleaned_data['date'] > self.cleaned_data['return_date']:
            raise ValidationError('The date of return cannot be earlier than the date of take.')

        if user_budget < get_amount(self.cleaned_data):
            raise ValidationError('You don\'t have  budget')

        user_budget -= get_amount(self.cleaned_data)
        self.initial.get('user').profile.save()

        return self.cleaned_data

    def save(self, commit=True):

        rental = super().save(commit=False)
        user = self.initial.get('user')
        amount = get_amount(self.cleaned_data)
        rent = CustomerGameRent(
            date=self.cleaned_data['date'],
            return_date=self.cleaned_data['return_date'],
            user=user,
            game=self.initial.get('game'),
            amount=amount

        )
        if commit:
            rent.save()
        return rental


class AddSliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'


class EditSliderForm(AddSliderForm):
    pass


class AddPlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class AddGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        required=True,
    )
    subject = forms.CharField(
        required=True,
        max_length=50,
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'row': 30,
            }
        ),
    )
