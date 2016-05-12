'''
Created on May 7, 2016

@author: lieyongzou
'''

from django import forms
from django.contrib.auth.models import User

class RestristrationForm(forms.ModelForm):
    '''
    A form for registration
    '''
    
    password_con = forms.CharField(max_length = 20, label = 'Conform Password')
    class Meta:
        model = User
        exclude = ('last_login', 
                   'is_superuser', 
                   'groups',
                   'user_permissions', 
                   'is_staff', 
                   'is_active', 
                   'date_joined', 
                   'first_name', 
                   'last_name'
                   )
        fields = ['username', 'email', 'password', 'password_con']
    
    def clean_username(self):
        '''
        A clean method to check whether the username has been used
        '''
        data = self.cleaned_data['username']
        if len(User.objects.filter(username__exact = data)):
            raise forms.ValidationError('The username has been used!')
        return data
    
    def clean(self):
        '''
        A clean method to check whether the password matches password conformation
        '''
        data = super(RestristrationForm, self).clean()
        psw = data['password']
        psw_con = data['password_con']
        if psw and psw_con and psw != psw_con:
            raise forms.ValidationError('The password doesn\'t match!')
        return data
    