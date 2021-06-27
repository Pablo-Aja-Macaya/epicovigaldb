from django.db import models
from upload.models import Sample

### Posibles tests ###
class PicardTest(models.Model): #.picardOutputCleaned.tsv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir del nombre del archivo
    # id_process = models.CharField(max_length=40)

    mean_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    median_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    pct_target_bases_1x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_10x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_100x = models.DecimalField(max_digits=7, decimal_places=6) 

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','date')
    def __str__(self):
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

class SingleCheckTest(models.Model): #.trimmed.sorted.SingleCheck.txt
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir de columna (primera) (sin cabecera)
    # id_process = models.CharField(max_length=40)

    autocorrelation = models.DecimalField(max_digits=15, decimal_places=10) 
    variation_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    gini_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    mad = models.DecimalField(max_digits=15, decimal_places=10) 

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','date')
    def __str__(self):
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

class NGSstatsTest(models.Model): #.ngsinfo.tsv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir de columna 'sampleName'
    # id_process = models.CharField(max_length=40)

    total_reads = models.IntegerField()
    mapped = models.IntegerField()
    trimmed = models.IntegerField()

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','date')
    def __str__(self):
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

class NextcladeTest(models.Model): #.csv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir de columna 'seqName'
    # id_process = models.CharField(max_length=40)

    total_missing = models.IntegerField(default=None, null=True, blank=True)
    clade = models.CharField(max_length=30, default=None, blank=True)
    qc_private_mutations_status = models.CharField(max_length=30, default=None, blank=True)
    qc_missing_data_status = models.CharField(max_length=30, default=None, blank=True)
    qc_snp_clusters_status = models.CharField(max_length=30, default=None, blank=True)
    qc_mixed_sites_status = models.CharField(max_length=30, default=None, blank=True)
    qc_overall_status = models.CharField(max_length=30, default=None, blank=True)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','date')
    def __str__(self):
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

class VariantsTest(models.Model): #.tsv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir del nombre del archivo
    # id_process = models.CharField(max_length=41)
    row = models.IntegerField()

    pos = models.IntegerField(default=None, null=True, blank=True)
    ref = models.CharField(max_length=100, default=None, blank=True)
    alt = models.CharField(max_length=100, default=None, blank=True)
    ref_dp = models.IntegerField(default=None, null=True, blank=True)
    alt_dp = models.IntegerField(default=None, null=True, blank=True)
    alt_freq = models.DecimalField(max_digits=7, decimal_places=6) 
    total_dp = models.IntegerField(default=None, null=True, blank=True)
    ref_codon = models.CharField(max_length=100, default=None, blank=True)
    ref_aa = models.CharField(max_length=100, default=None, blank=True)
    alt_codon = models.CharField(max_length=100, default=None, blank=True)
    alt_aa = models.CharField(max_length=100, default=None, blank=True)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ('id_uvigo','row','id_process','date',)
        constraints = [
            models.UniqueConstraint(fields=['id_uvigo','row','date'], name='unique_constraint')
        ]
    def __str__(self):
        return str(self.id_uvigo) + f' - {self.row}' + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

# #     # No sé si quieren estos
# #     # frequency
# #     # gene
# #     # aa_position
# #     # thresholds

class Country(models.Model):
    name = models.CharField(primary_key=True,max_length=30)
    def __str__(self):
        return str(self.name)

class LineagesTest(models.Model): #.csv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE)# a partir de columna 'taxon'
    # id_process = models.CharField(max_length=40)

    lineage = models.CharField(max_length=10)
    probability = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True) 
    conflict = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True) 
    most_common_countries = models.ManyToManyField(Country, blank=True)
    pangolearn_version = models.CharField(max_length=15, blank=True, null=True)
    comments = models.TextField(max_length=50, default=None, blank=True, null=True)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','date')
    def __str__(self):
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'



