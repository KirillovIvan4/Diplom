from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm


from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text='Необязательное поле. Введите ваш номер телефона.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ( 'username', 'email', 'phone_number', 'avatar', 'country', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone_number

class PasswordRecoveryForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)