import floppyforms as forms

class TwitterSearchForm(forms.Form):
    q = forms.CharField(required=True, label="Busqueda")
    def clean_q(self):
        data = self.cleaned_data['q']
        return '{0} filter:links'.format(data)

class URLForm(forms.Form):
    url = forms.URLField()
