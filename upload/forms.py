from django import forms
from django.db.models.base import Model
from django.forms import ModelForm


class FullSampleForm(forms.Form):
    # Sample
    id_uvigo = forms.CharField(required=True)
    id_accession = forms.CharField(required=False)
    original_name = forms.CharField(required=False)
    categoria_muestra = forms.ChoiceField(choices=((None,None),('aleatoria','aleatoria'),('vigilancia','vigilancia')),required=False)
    edad = forms.IntegerField(required=False)
    sexo = forms.ChoiceField(choices=((None,None),('H','H'),('M','M')),required=False)
    patient_status = forms.ChoiceField(choices=((None,None),('S','S'),('N','N')),required=False)
    nodo_secuenciacion = forms.CharField(required=False)
    fecha_muestra = forms.DateField(required=False)
    observaciones = forms.CharField(required=False)

    # SampleMetaData
    id_paciente = forms.CharField(required=False)
    id_hospital = forms.CharField(required=False)
    numero_envio = forms.IntegerField(required=False)
    id_tubo = forms.CharField(required=False)
    id_muestra = forms.CharField(required=False)
    
    hospitalizacion = forms.ChoiceField(choices=((None,None),('S','S'),('N','N')),required=False)
    uci = forms.ChoiceField(choices=((None,None),('S','S'),('N','N')),required=False)
    
    ct_orf1ab = forms.DecimalField(required=False)
    ct_gen_e = forms.DecimalField(required=False)
    ct_gen_n = forms.DecimalField(required=False)
    ct_redrp = forms.DecimalField(required=False)
    ct_s = forms.DecimalField(required=False)

    fecha_envio_cdna = forms.DateField(required=False)
    fecha_run_ngs = forms.DateField(required=False)
    fecha_entrada_fastq = forms.DateField(required=False)
    fecha_sintomas = forms.DateField(required=False)
    fecha_diagnostico = forms.DateField(required=False)
    fecha_entrada = forms.DateField(required=False)

    # Regiones
    cp = forms.IntegerField(required=False)
    localizacion = forms.CharField(required=False)
    pais = forms.CharField(required=False)
    region = forms.CharField(required=False)
    latitud = forms.FloatField(required=False)
    longitud = forms.FloatField(required=False)

