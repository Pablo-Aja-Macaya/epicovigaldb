from django.db import models

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    cp = models.IntegerField(null=True)
    localizacion = models.CharField(max_length=50, null=True) 
    division = models.CharField(max_length=50, default=None, null=True) 
    pais = models.CharField(max_length=50, default='SPAIN') 
    region = models.CharField(max_length=50, default='EUROPE') 
    latitud = models.TextField(max_length=50, default=None, null=True)
    longitud = models.TextField(max_length=50, default=None, null=True)
   
    class Meta:
        unique_together = ('cp','localizacion')
    def __str__(self):
        return str(self.cp) +' '+ str(self.localizacion)

class Sample(models.Model):
    id_uvigo = models.CharField(max_length=20, primary_key=True)
    id_accession = models.CharField(max_length=20, default=None, blank=True, null=True)
    original_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    categoria_muestra = models.CharField(max_length=20, default=None, blank=True, null=True)
    edad = models.IntegerField(default=0, blank=True, null=True)
    sexo = models.CharField(max_length=1, default=None, blank=True, null=True)
    patient_status = models.CharField(max_length=20, default=None, blank=True, null=True)
    nodo_secuenciacion = models.CharField(max_length=50, default=None, blank=True, null=True)
    fecha_muestra = models.DateField(blank=True, null=True)
    observaciones = models.TextField(max_length=100, default=None, blank=True, null=True)
    data_path = models.FileField(storage=('uploads/'), default=None, blank=True, null=True)

    def __str__(self):
        return str(self.id_uvigo)
    def hospital_id(self):
        return {'id_uvigo':str(self.id_uvigo.split('.')[1])}
    
class SampleMetaData(models.Model):
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE)
    id_paciente = models.CharField(max_length=20, default=None, blank=True, null=True)
    id_hospital = models.CharField(max_length=20, default=None, blank=True, null=True)
    numero_envio = models.IntegerField(default=0, blank=True, null=True)
    id_tubo = models.CharField(max_length=20, default=None, blank=True, null=True)
    id_muestra = models.CharField(max_length=20, default=None, blank=True, null=True)
    
    hospitalizacion = models.CharField(max_length=1, default=None, null=True, blank=True)
    uci = models.CharField(max_length=1, default=None, null=True, blank=True)
    
    ct_orf1ab = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    ct_gen_e = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    ct_gen_n = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    ct_rdrp = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    ct_s = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)

    fecha_envio_cdna = models.DateField(blank=True, null=True)
    fecha_run_ngs = models.DateField(blank=True, null=True)
    fecha_entrada_fastq = models.DateField(blank=True, null=True)
    fecha_sintomas = models.DateField(blank=True, null=True)
    fecha_diagnostico = models.DateField(blank=True, null=True)
    fecha_entrada = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id_uvigo)


