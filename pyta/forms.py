from django import forms
from models import UserInfo
from models import RequestPriorityEntry
from widgets import DatePickerWidget


class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        widgets = {
            'photo': forms.FileInput(),
            'birth_date': DatePickerWidget(
                params="""dateFormat: 'yy-mm-dd',
                changeYear: true,
                defaultDate: '-18y',
                yearRange: 'c-20:c+10'""")
            }


class EditRequestPriorityForm(forms.ModelForm):
    class Meta:
        model = RequestPriorityEntry
