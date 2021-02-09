from django.db import models
from tests.tasks import check_status


### Posibles tests ###
class PicardTest(models.Model): #.picardOutputCleaned.tsv
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()

    mean_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    median_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    pct_target_bases_1x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_10x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_100x = models.DecimalField(max_digits=7, decimal_places=6) 

    def __str__(self):
        return str(self.id_process)

class SingleCheckTest(models.Model): #.trimmed.sorted.SingleCheck.txt
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()

    autocorrelation = models.DecimalField(max_digits=15, decimal_places=10) 
    variation_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    gini_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    mad = models.DecimalField(max_digits=15, decimal_places=10) 
    
    def __str__(self):
        return str(self.id_process)

class NGSstatsTest(models.Model): #.ngsinfo.tsv
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()

    total_reads = models.IntegerField()
    mapped = models.IntegerField()
    trimmed = models.IntegerField()

    def __str__(self):
        return str(self.id_process)

class NextcladeTest(models.Model): #.csv
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()

    total_missing = models.IntegerField()
    clade = models.TextField()
    qc_private_mutations_status = models.TextField()
    qc_missing_data_status = models.TextField()
    qc_snp_clusters_status = models.TextField()
    qc_mixed_sites_status = models.TextField()

    def __str__(self):
        return str(self.id_process)

class VariantsTest(models.Model): #.tsv
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()

    pos = models.IntegerField()
    ref = models.CharField(max_length=10)
    alt = models.CharField(max_length=10)
    alt_freq = models.DecimalField(max_digits=7, decimal_places=6) 
    ref_codon = models.CharField(max_length=10)
    ref_aa = models.CharField(max_length=10)
    alt_codon = models.CharField(max_length=10)
    alt_aa = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id_process)

    # frequency
    # gene
    # aa_position
    # thresholds

class LineagesTest(models.Model): #_lineages.csv
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()

    lineage = models.CharField(max_length=10)
    probability = models.DecimalField(max_digits=7, decimal_places=6) 
    pangolearn_version = models.CharField(max_length=15)

    def __str__(self):
        return str(self.id_process)

### Functions ###
def prueba():
    check_status.delay()

