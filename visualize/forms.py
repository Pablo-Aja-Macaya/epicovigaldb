from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from upload.models import Sample, Region
from upload.models import SampleMetaData
from tests.models import PicardTest, NextcladeTest, NGSstatsTest, SingleCheckTest, VariantsTest
from tests.models import LineagesTest

class GraphsForm(forms.Form):
    categorias = [(i,i) for i in Sample.objects.values_list('categoria_muestra',flat=True).distinct()]
    fecha_inicial = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    fecha_final = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    categoria = forms.ChoiceField(choices=categorias, required=True)
    umbral = forms.IntegerField(required=False)
    filtro = forms.CharField(required=False)


class GraphsFormMultipleChoice(forms.Form):
    # Choices
    choices_categoria = [(i,i) for i in Sample.objects.values_list('categoria_muestra',flat=True).distinct().order_by('categoria_muestra') if i]
    choices_vigilancia = [(i,i) for i in Sample.objects.values_list('vigilancia',flat=True).distinct().order_by('vigilancia') if i]
    # choices_calidad = [(i,i) for i in Sample.objects.values_list('samplemetadata__calidad_secuenciacion',flat=True).distinct().order_by('samplemetadata__calidad_secuenciacion')]
    # Campos
    fecha_inicial = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class':'col-3 text-center form-control'}))
    fecha_final = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'class':'col-3 text-center form-control'}))
    categoria = forms.MultipleChoiceField(choices=choices_categoria, required=True, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))#
    vigilancia = forms.MultipleChoiceField(choices=choices_vigilancia, required=True, widget=forms.CheckboxSelectMultiple(attrs={'class':'ul-no-bullets '}))#,widget=forms.CheckboxSelectMultiple())
    # calidad_secuenciacion = forms.MultipleChoiceField(choices=choices_calidad, required=True, widget=forms.SelectMultiple()
    umbral = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(attrs={'class':'col-2 text-center form-control'}))
    filtro = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'class':'col-2 text-center form-control'}))

class SampleForm(ModelForm):
    id_uvigo = forms.CharField(required=False, disabled=True)
    # cp = forms.IntegerField(required=False)
    # localizacion = forms.CharField(required=False)
    # categoria_muestra = forms.ChoiceField(choices=(('1','One'),("2", "Two")), required=False)
    id_region = forms.ModelChoiceField(queryset=Region.objects.all().order_by('localizacion'), required=False)#, disabled=True)
    class Meta:
        model = Sample
        fields = '__all__'
        exclude = ['data_path']#,'id_region']
        # widgets = {
        #     'id_uvigo': forms.TextInput(attrs={'disabled': True}),
        #     'id_region': forms.TextInput(attrs={'disabled': True}),
        # }

class SampleMetaDataForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = SampleMetaData
        fields = '__all__'
        exclude = ['data_path']

class RegionForm(forms.Form):
    id_region = forms.CharField(required=False, disabled=True)
    localizacion = forms.CharField(required=False)
    cp = forms.DecimalField(required=False)
    latitud = forms.DecimalField(required=False)
    longitud = forms.DecimalField(required=False)
    division = forms.CharField(required=False)
    pais = forms.CharField(required=False)
    region = forms.CharField(required=False)


## Test forms
class SingleCheckForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = SingleCheckTest
        fields = '__all__'
class PicardForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = PicardTest
        fields = '__all__'
class NextcladeForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = NextcladeTest
        fields = '__all__'
class LineagesForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = LineagesTest
        fields = '__all__'
class NGSStatssForm(ModelForm):
    id_uvigo = forms.ModelChoiceField(queryset=Sample.objects.all() , required=False, disabled=True)
    class Meta:
        model = NGSstatsTest
        fields = '__all__'