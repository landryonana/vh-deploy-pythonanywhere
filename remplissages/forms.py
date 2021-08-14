from django import forms

from remplissages.models import Evangelisation, Person, Site

#==================================================================================
#===========================Evangelisation form
class EvangForm(forms.ModelForm):
    class Meta:
        model = Evangelisation
        fields = ['day', 'heure_de_debut', 'heure_de_fin', 'site', 'boss', 'actif']
    
    def clean_boss(self):
      return self.cleaned_data['boss']
    
    def clean(self):
        cleaned_data = super().clean()
        heure_de_debut = cleaned_data.get("heure_de_debut")
        heure_de_fin = cleaned_data.get("heure_de_fin")

        debut_minites = heure_de_debut.hour*60 + heure_de_debut.minute
        fin_minites = heure_de_fin.hour*60 + heure_de_fin.minute
        msg = "Heure de début doit etre inférieur ou égal à Heure de fin"
        if debut_minites>fin_minites:
            self.add_error('heure_de_debut', msg)
        
    


#====================================================================================
#===========================Person form
class PersonForm(forms.ModelForm):
    contacts = forms.IntegerField(label="Contact", help_text="Le numéro de téléphone doit avoir 09 chiffres")
    nom_et_prenom = forms.CharField(label="Nom et prenom", help_text="ce champ doit avoir au moins trois caractères")
    quartier_d_habitation = forms.CharField(label="Quartier d'habitation", help_text="ce champ doit avoir au moins trois caractères")
    class Meta:
        model = Person
        fields = ['site_evangelisation', 'nom_et_prenom', 
                    'contacts', 'quartier_d_habitation', 
                    'accepte_jesus','sexe', 'whatsapp', 'boss',
                    'sujets_de_priere', 'temoignages'
                ]

    def clean_boss(self):
        return self.cleaned_data['boss']
    
    def clean(self):
        cleaned_data = super().clean()
        nom_prenom = cleaned_data.get("nom_et_prenom")
        quartier = cleaned_data.get("quartier_d_habitation")
        accepte_jesus = cleaned_data.get("accepte_jesus")
        sexe = cleaned_data.get("sexe")

        msg1 = "Merci de renseigner ce champ"
        if accepte_jesus=="---------":
            self.add_error('accepte_jesus', msg1)
        if sexe=="---------":
            self.add_error('accepte_jesus', msg1)

        msg = "Ce champ doit avoir au moins 03 caractères"
        if len(quartier)<=2:
            self.add_error('quartier_d_habitation', msg)
        if len(nom_prenom)<=2:
            self.add_error('nom_et_prenom', msg)
    
    def clean_contacts(self):
        contact = self.cleaned_data['contacts']
        if len(str(contact))!=9:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        else:
            if len(str(contact))==9:
                contact_6 = str(contact)[0]
                print(contact_6)
                if int(contact_6)!=6:
                    raise forms.ValidationError("Le numéro de télephone doit commencer par 6")
        return contact


#===========================Person form Update
class PersonFormUpdate(forms.ModelForm):
    contacts = forms.IntegerField(label="Contact", help_text="Le numéro de téléphone doit avoir 09 chiffres")
    nom_et_prenom = forms.CharField(label="Nom et prenom", help_text="ce champ doit avoir au moins trois caractères")
    quartier_d_habitation = forms.CharField(label="Quartier d'habitation", help_text="ce champ doit avoir au moins trois caractères")
    class Meta:
        model = Person
        fields = ['site_evangelisation', 'evangelisation', 'nom_et_prenom', 
                    'contacts', 'quartier_d_habitation', 'accepte_jesus', 
                    'sexe', 'whatsapp','boss',
                    'sujets_de_priere', 'temoignages']

    def clean_boss(self):
        return self.cleaned_data['boss']
    
    def clean(self):
        cleaned_data = super().clean()
        nom_prenom = cleaned_data.get("nom_et_prenom")
        quartier = cleaned_data.get("quartier_d_habitation")
        site_evangelisation = cleaned_data.get("site_evangelisation")
        evangelisation = cleaned_data.get("evangelisation")

        msg1 = f"Le nom du site et le lieu de {evangelisation} ne sont pas identiques"
        if site_evangelisation!=evangelisation.site:
            self.add_error('site_evangelisation', msg1)

        msg = "Ce champ doit avoir au moins 03 caractères"
        if len(quartier)<=2:
            self.add_error('quartier_d_habitation', msg)
        if len(nom_prenom)<=2:
            self.add_error('nom_et_prenom', msg)
    
    def clean_contacts(self):
        contact = self.cleaned_data['contacts']
        if len(str(contact))!=9:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        else:
            if len(str(contact))==9:
                contact_6 = str(contact)[0]
                print(contact_6)
                if int(contact_6)!=6:
                    raise forms.ValidationError("Le numéro de télephone doit commencer par 6")
        return contact


#====================================================================================
#===========================Site form
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['nom_site_evangelisation', 'image']
    
    def clean_nom_site_evangelisation(self):
        nom_site = self.cleaned_data['nom_site_evangelisation']
        if len(str(nom_site))<3:
            raise forms.ValidationError("La valeur doit avoir au moins 03 caractères ")
        return nom_site