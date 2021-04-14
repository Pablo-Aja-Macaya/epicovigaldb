from django import forms
from upload.models import Sample
from django.forms import widgets

class SelectTestForm(forms.Form):
    test_choices = (
        ('Picard','Picard'),
        ('Pangolin','Pangolin'),
    )

    id_uvigo = forms.ModelMultipleChoiceField(
        queryset=Sample.objects.all().order_by('id_uvigo').exclude(samplemetadata__fecha_entrada_fastq=None), 
        required=True, 
        widget=widgets.SelectMultiple(attrs={'size': 20}),
        label_suffix = ' (ctrl para seleccionar varios):')
    test = forms.ChoiceField(choices=test_choices,required=True)
