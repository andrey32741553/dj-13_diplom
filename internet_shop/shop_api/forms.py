from django import forms


class CollectionForm(forms.ModelForm):

    def clean_product(self):
        data = self.cleaned_data['product']
        print(data)
        return data
