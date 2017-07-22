from django import forms
from django.contrib.auth import (authenticate, get_user_model,
                                 login, logout)


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError('There is no user with the given username')
        else:
            user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Incorrect password')
        if not user.is_active:
            raise forms.ValidationError('This user is no longer active')
        return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     # print(email, email2)
    #     if email != email2:
    #         raise forms.ValidationError('Email must match')
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError('This email is already in use')
    #     return super(UserRegisterForm, self).clean()

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        # print(email, email2)
        if email != email2:
            raise forms.ValidationError('Email must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already in use')
        return email

