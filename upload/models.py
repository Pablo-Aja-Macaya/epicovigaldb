from django.db import models

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    cp = models.IntegerField()
    localizacion = models.CharField(max_length=50) 
    country = models.TextField(max_length=50, default='SPAIN') 
    region = models.TextField(max_length=50, default='EUROPE') 
    latitude = models.TextField(max_length=50, default=None)
    longitude = models.TextField(max_length=50, default=None)
   
    class Meta:
        unique_together = ('cp','localizacion')
    def __str__(self):
        return str(self.cp) +' '+ str(self.localizacion)

class Sample(models.Model):
    id_uvigo = models.CharField(max_length=20, primary_key=True)
    id_accession = models.CharField(max_length=20, default=None, blank=True)
    original_name = models.CharField(max_length=50, default=None, blank=True)
    id_region = models.IntegerField(default=0, blank=True)
    edad = models.IntegerField(default=0, blank=True)
    sexo = models.CharField(max_length=1, default=None, blank=True)
    patient_status = models.CharField(max_length=20, default=None, blank=True)
    nodo_secuenciación = models.CharField(max_length=20, default=None, blank=True)
    fecha_muestra = models.DateField()
    observaciones = models.TextField(max_length=50, default=None, blank=True)
    data_path = models.FileField(storage=('uploads/'), default=None, blank=True)

    def __str__(self):
        return str(self.id_uvigo)
    def hospital_id(self):
        return {'id_uvigo':str(self.id_uvigo.split('.')[1])}
    
class SampleMetaData(models.Model):
    id_uvigo = models.CharField(max_length=20, primary_key=True)
    id_paciente = models.CharField(max_length=20, default=None, blank=True)
    id_hospital = models.CharField(max_length=20, default=None, blank=True)
    numero_envio = models.IntegerField(default=0, blank=True)
    id_tubo = models.CharField(max_length=20, default=None, blank=True)
    id_muestra = models.CharField(max_length=20, default=None, blank=True)
    
    hospitalizacion = models.CharField(max_length=1)
    uci = models.CharField(max_length=1)
    
    ct_orf1ab = models.DecimalField(max_digits=5, decimal_places=2, default=None)
    ct_gen_e = models.DecimalField(max_digits=5, decimal_places=2, default=None)
    ct_gen_n = models.DecimalField(max_digits=5, decimal_places=2, default=None)
    ct_redrp = models.DecimalField(max_digits=5, decimal_places=2, default=None)
    ct_s = models.DecimalField(max_digits=5, decimal_places=2, default=None)

    fecha_envio_cdna = models.DateField()
    fecha_run_ngs = models.DateField()
    fecha_entrada_fastq_uvigo = models.DateField()
    fecha_sintomas = models.DateField()
    fecha_diagnostico = models.DateField()
    fecha_entrada_uv = models.DateField()

    def __str__(self):
        return str(self.id_uvigo)