from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from upload.models import Sample, Region
from upload.models import SampleMetaData
from tests.models import PicardTest, NextcladeTest, NGSstatsTest, SingleCheckTest, VariantsTest
from tests.models import LineagesTest

class GraphsForm(forms.Form):
    categorias = [(i,i) for i in Sample.objects.values_list('categoria_muestra',flat=True).distinct()]
    fecha_inicial = forms.DateField()
    fecha_final = forms.DateField()
    categoria = forms.ChoiceField(choices=categorias, required=True)
    umbral = forms.IntegerField(required=False)
    filtro = forms.CharField(required=False)



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

class RegionForm(ModelForm):
    id_region = forms.ModelChoiceField(queryset=Region.objects.all() , required=False, disabled=True)
    class Meta:
        model = Region
        fields = '__all__'

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