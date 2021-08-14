from django import forms


from remplissages.models import Suivie



class SuivieForm(forms.ModelForm):
    class Meta:
        model = Suivie
        fields = ['nbre_appel', 
                    'nbre_visite_au_culte', 'nbre_invitation_au_culte', 
                    'choix_person', 'boos_suivi']
        exclude = ['person']


class SearchForm(forms.Form):
    query = forms.DateField(input_formats=['%d/%m/%Y'])