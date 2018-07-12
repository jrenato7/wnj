from django import forms


class GalleryAddForm(forms.Form):
    image = forms.ImageField()
