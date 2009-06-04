from django import forms

from django.contrib.auth.models import User

#from needletail.login.models import Band_Member
from needletail.login.models import Band

class LoginForm(forms.Form):
    band_name = forms.CharField()
    username  = forms.CharField()
    password  = forms.CharField(widget = forms.PasswordInput(render_value=
                                                             False))


class NewBandForm(forms.Form):
    band_name  = forms.CharField()
    first_name = forms.CharField()
    last_name  = forms.CharField()
    username   = forms.CharField()
    password   = forms.CharField(widget = forms.PasswordInput(render_value=
                                                              False))
    pass_conf  = forms.CharField(widget = forms.PasswordInput(render_value=
                                                              False))
    email      = forms.EmailField()

    #ensure unique username
    def clean_username(self):
        usr = self.cleaned_data['username']
        try:
            q = User.objects.get(username = usr)
            raise forms.ValidationError("Username is unavailible")
        except User.DoesNotExist:
            return usr

#    def clean_email(self):
#        e = self.cleaned_data['email']
#        try:
#            q = User.objects.get(email = e)
#            raise forms.ValidationError("Email already exists")
#        except User.DoesNotExist:
#            return e


    def clean_pass_conf(self):
        if self.cleaned_data['password'] == self.cleaned_data['pass_conf']:
            return
        else:
            raise forms.ValidationError("Password Confirmation does not match")


class CreateWebsiteForm(forms.Form):
    web_ext = forms.CharField()

    def clean_web_ext(self):
        w = self.cleaned_data['web_ext']
        try:
            w = Band.objects.get(web_ext = w)
            raise forms.ValidationError("Sorry, that web extension already "
                                        "exists. Please choose another.")
        except Band.DoesNotExist:
            return w

                                   
