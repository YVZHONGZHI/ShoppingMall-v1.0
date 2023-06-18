from w import models
from django import forms
from django.core.validators import RegexValidator


class MyRegForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=8, label='用户名:',
                               error_messages={
                                   'min_length': '用户名最少3位!',
                                   'max_length': '用户名最大8位!',
                                   'required': '用户名不能为空!'
                               },
                               widget=forms.widgets.TextInput()
                               )
    password = forms.CharField(min_length=3, max_length=8, label='密码:',
                               error_messages={
                                   'min_length': '密码最少3位!',
                                   'max_length': '密码最大8位!',
                                   'required': '密码不能为空!'
                               },
                               widget=forms.widgets.PasswordInput(),
                               validators=[RegexValidator(r'^[0-9]+$', '密码不能为非数字!')]
                               )
    confirm_password = forms.CharField(min_length=3, max_length=8, label='确认密码:',
                                       error_messages={
                                           'min_length': '确认密码最少3位!',
                                           'max_length': '确认密码最大8位!',
                                           'required': '确认密码不能为空!'
                                       },
                                       widget=forms.widgets.PasswordInput()
                                       )
    email = forms.EmailField(label='邮箱:',
                             error_messages={
                                 'invalid': '邮箱格式不正确!',
                                 'required': '邮箱不能为空!'
                             },
                             widget=forms.widgets.EmailInput()
                             )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error('username', '用户名已存在!')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password', '两次输入的密码不一致!')
        return self.cleaned_data


class EndForm(forms.Form):
    password = forms.CharField(label='输入账号密码:',
                               error_messages={
                                   'required': '账号密码不能为空!'
                               },
                               widget=forms.widgets.PasswordInput(attrs={'name': 'password'}),
                               validators=[RegexValidator(r'^[0-9]+$', '密码不能为非数字!')]
                               )