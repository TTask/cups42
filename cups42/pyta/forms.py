from django import forms
from models import UserInfo


class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        widgets = {
            'photo': forms.FileInput()
        }
