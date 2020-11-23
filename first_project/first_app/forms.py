from django import forms
from django.core import validators
from django.contrib.auth.models import User
from first_app.models import UserProfileInfo

years_5 = ['1995', '2005', '2015']
choices_like = [('Yes', 'Yes, I like it'), ('No', 'No, I don`t like it')]

'''def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Name has to start with Z!")'''


class FormName(forms.Form):
    name = forms.CharField(max_length=70)  #validators=[check_for_z]
    email = forms.EmailField(max_length=100, help_text="Enter valid e-mail address")
    verify_email = forms.EmailField(label='Enter your email again: ')
    text = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(widget=forms.SelectDateWidget(years=years_5))
    like = forms.ChoiceField(widget=forms.RadioSelect, choices=choices_like)

    botcatcher = forms.CharField(widget=forms.HiddenInput,
                                 required=False,
                                 validators=[validators.MaxLengthValidator(0)])
    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError('Make sure both emails are the same!')


    '''def clean_botcatcher(self):
        botcatcher = self.cleaned_data["botcatcher"]
        if len(botcatcher) > 0:
            raise forms.ValidationError("Gotcha BOT!")
        return botcatcher'''

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
