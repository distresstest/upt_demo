from django import forms


class TrailForm(forms.Form):
    #post = forms.CharField(label='Data:')
    pass

class LocationForm(forms.Form):
    item_id = forms.IntegerField(label="A form field")
    pass