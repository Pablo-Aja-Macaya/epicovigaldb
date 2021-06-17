from django import forms
from upload.models import Sample
from django.forms import widgets

class SelectTestForm(forms.Form):
    test_choices = (
        ('Nextclade','Nextclade'),
        ('Picard','Picard'),
        # ('Pangolin','Pangolin'),
    )
    # id_uvigo = forms.ModelMultipleChoiceField(
    #     queryset=Sample.objects.all().order_by('id_uvigo').exclude(samplemetadata__fecha_entrada_fastq=None), 
    #     required=True, 
    #     widget=widgets.SelectMultiple(attrs={'size': 20}),
    #     label_suffix = ' (ctrl para seleccionar varios):')
    test = forms.ChoiceField(choices=test_choices,required=True)

class SelectInputForm(forms.Form):
    files = forms.MultipleChoiceField(required=False,
        widget=forms.SelectMultiple(attrs={'size': 25}))


# class SelectInputForm(forms.Form):
#     def __init__(self, test, *args, **kwargs):
#         super(SelectInputForm, self).__init__(*args, **kwargs)
#         self.fields['files'] = forms.MultipleChoiceField(
#             choices=((1,2)), widget=forms.SelectMultiple(attrs={'size': 10})
#         )
