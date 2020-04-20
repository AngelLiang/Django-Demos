from django import forms

from django.contrib.auth.forms import UserCreationForm as _UserCreationForm


class WalcomeForm(forms.Form):
    def save(self, commit=True):
        pass


class UserCreationForm(_UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


class CreateSuperUserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=80, required=True)
    password = forms.CharField(
        label='密码', max_length=80, required=True, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='密码确认', max_length=80, required=True, widget=forms.PasswordInput
    )
    email = forms.EmailField(label='邮箱', max_length=128, required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                # self.error_messages['password_mismatch'],
                '两次密码不匹配',
                code='password_mismatch',
            )
        return password2

    # def _post_clean(self):
    #     super()._post_clean()
    #     # Validate the password after self.instance is updated with form data
    #     # by super().
    #     password = self.cleaned_data.get('password2')
    #     if password:
    #         try:
    #             password_validation.validate_password(password, self.instance)
    #         except forms.ValidationError as error:
    #             self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
