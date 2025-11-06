from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label = 'Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {'username': 'Имя пользователя',
                  'phone': 'Номер телефона',
                  'email': 'Ваша почта',
                  'first_name': 'Имя',
                  'last_name': 'Фамилия',
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['username'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
