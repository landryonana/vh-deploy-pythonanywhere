from django import forms


from remplissages.models import Image



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['titre', 'image', 'description']
    

class ImageFormUpdate(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['titre', 'evangelisation', 'image', 'description']


class SearchForm(forms.Form):
    query = forms.DateField()