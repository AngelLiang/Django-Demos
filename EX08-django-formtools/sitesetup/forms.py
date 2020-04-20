from django import forms


class WalcomeForm(forms.Form):
    pass


class CreateSuperUserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=80, required=True)
    password = forms.CharField(
        label='密码', max_length=80, required=True)
    password2 = forms.CharField(label='密码确认', max_length=80, required=True)
    email = forms.EmailField(label='邮箱', max_length=128, required=False)


class DoneForm(forms.Form):
    pass
