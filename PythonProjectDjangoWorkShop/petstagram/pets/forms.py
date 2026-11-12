from django import forms

from pets.models import Pet

from common.mixins import DisabledFormMixin


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'date_of_birth', 'personal_photo']
        labels = {
            'name': 'Pet Name',
            'date_of_birth': 'Date of Birth',
            'personal_photo': 'Link to image',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet Name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'personal_photo': forms.URLInput(attrs={'placeholder': 'Link to image'}),
        }

class PetCreateForm(PetForm):
    ...

class PetEditForm(PetForm):
    ...

class PetDeleteForm(DisabledFormMixin, PetForm):
    ...