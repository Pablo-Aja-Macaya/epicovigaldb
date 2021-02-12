from django.db import models
import io, csv
import re

### Posibles tests ###
class PicardTest(models.Model): #.picardOutputCleaned.tsv
    id_uvigo = models.CharField(max_length=20, primary_key=True) # a partir del nombre del archivo
    id_process = models.CharField(max_length=40)

    mean_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    median_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    pct_target_bases_1x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_10x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_100x = models.DecimalField(max_digits=7, decimal_places=6) 

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S"))

class SingleCheckTest(models.Model): #.trimmed.sorted.SingleCheck.txt
    id_uvigo = models.CharField(max_length=20, primary_key=True) # a partir de filas (primera) (sin cabecera)
    id_process = models.CharField(max_length=40)

    autocorrelation = models.DecimalField(max_digits=15, decimal_places=10) 
    variation_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    gini_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    mad = models.DecimalField(max_digits=15, decimal_places=10) 

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S"))

class NGSstatsTest(models.Model): #.ngsinfo.tsv
    id_uvigo = models.CharField(max_length=20, primary_key=True) # a partir de columna 'sampleName'
    id_process = models.CharField(max_length=40)

    total_reads = models.IntegerField()
    mapped = models.IntegerField()
    trimmed = models.IntegerField()

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S"))

class NextcladeTest(models.Model): #.csv
    id_uvigo = models.CharField(max_length=20, primary_key=True) # a partir de columna 'seqName'
    id_process = models.CharField(max_length=40)

    total_missing = models.IntegerField()
    clade = models.TextField()
    qc_private_mutations_status = models.TextField()
    qc_missing_data_status = models.TextField()
    qc_snp_clusters_status = models.TextField()
    qc_mixed_sites_status = models.TextField()

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S"))

class VariantsTest(models.Model): #.tsv
    id_uvigo = models.CharField(max_length=20, primary_key=True) # a partir del nombre del archivo
    id_process = models.CharField(max_length=40)

    pos = models.IntegerField()
    ref = models.CharField(max_length=10)
    alt = models.CharField(max_length=10)
    alt_freq = models.DecimalField(max_digits=7, decimal_places=6) 
    ref_codon = models.CharField(max_length=10)
    ref_aa = models.CharField(max_length=10)
    alt_codon = models.CharField(max_length=10)
    alt_aa = models.CharField(max_length=10)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S"))

    # No sé si quieren estos
    # frequency
    # gene
    # aa_position
    # thresholds

class LineagesTest(models.Model): #.csv
    id_uvigo = models.CharField(max_length=20, primary_key=True) # a partir de columna 'taxon'
    id_process = models.CharField(max_length=40)

    lineage = models.CharField(max_length=10)
    probability = models.DecimalField(max_digits=7, decimal_places=6) 
    pangolearn_version = models.CharField(max_length=15, blank=True)
    comments = models.TextField(max_length=50, default=None, blank=True)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S"))

class LineagesMostCommonCountries(models.Model):
    # Esta tabla se hace porque el atributo 'most common countries' de pangolin contiene cosas tipo 'Spain,Portugal'
    id_uvigo = models.CharField(max_length=20, primary_key=True)
    id_process = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now=True)

    country = models.TextField(max_length=50, default=None, blank=True)

#############################################################################
### Functions ###
# from tests.tasks import check_status

# def prueba():
#     check_status.delay()
fields_correspondence = {
    # Picard #.picardOutputCleaned.tsv
    # Muestra a partir del nombre del archivo
    'PicardTest':{
        'MEAN_TARGET_COVERAGE':'mean_target_coverage',
        'MEDIAN_TARGET_COVERAGE':'median_target_coverage',
        'PCT_TARGET_BASES_1X':'pct_target_bases_1x',
        'PCT_TARGET_BASES_10X':'pct_target_bases_10x',
        'PCT_TARGET_BASES_100X':'pct_target_bases_100x',
    },
    # SingleCheck #.trimmed.sorted.SingleCheck.txt
    # Este no tiene cabecera así que se usa el índice de la columna
    # Muestra a partir de la columna 0
    'SingleCheckTest':{
        8:'autocorrelation',
        9:'variation_coefficient',
        10:'gini_coefficient',
        11:'mad',
    },
    # NGSStats #.ngsinfo.tsv
    # Muestra # a partir de columna 'sampleName'
    'NGSstatsTest':{
        'sampleName':'id_uvigo',
        'totalReads':'total_reads',
        'mapped':'mapped',
        'trimmed':'trimmed',       
    },
    # Nextclade # .csv
    # Muestra a partir de columna 'seqName'
    'NextcladeTest':{
        'seqName':'id_uvigo',
        'totalMissing':'total_missing',
        'clade':'clade',
        'qc.privateMutations.status':'qc_private_mutations_status',
        'qc.missingData.status':'qc_missing_data_status',
        'qc.snpClusters.status':'qc_snp_clusters_status',
        'qc.mixedSites.status':'qc_mixed_sites_status',   
    },
    # iVar #.tsv
    # Muestra a partir del nombre del archivo
    'VariantsTest':{
        'POS':'pos',
        'REF':'ref',
        'ALT':'alt',
        'ALT_FREQ':'alt_freq', 
        'REF_CODON':'ref_codon',
        'REF_AA':'ref_aa',
        'ALT_CODON':'alt_codon',
        'ALT_AA':'alt_aa',           
    },
    # Pangolin # .csv
    # Muestra a partir de columna 'taxon'
    'LineagesTest':{
        'Lineage':'lineage',
        'Probability':'probability',
        'Sequence name':'id_uvigo',
        'Most common countries':'most_common_countries' ### añadir a modelo
    },
}

def detect_file(header):
    # Aproximación mala a una detección del origen de cada archivo
    # Si cambia el número de columnas no funciona
    # Igual es mejor comprobar que todos los campos que se quieren están en el archivo
    header_length_correspondence = {
        43:'NextcladeTest',
        6:'NGSstatsTest',
        53:'PicardTest',
        12:'SingleCheckTest', # este puede dar problemas, igual son 13 columnas
        19:'VariantsTest',
        7:'LineagesTest',
    }
    return header_length_correspondence.get(len(header))

def find_sample_name(string):
    # Encontrar si una cadena contiene 'EPI.*.X', si es así ese será el nombre de la muestra
    sample_name = re.search(r'EPI\..+\.\d+',string.upper())
    if sample_name:
        return sample_name.group()
    else:
        return None

def upload_picard(reader, sample_name):
    for line in reader:
        id_uvigo = sample_name
        id_process = 'U-XXX'
        mean_target_coverage = float(line['mean_target_coverage'].replace(',','.'))
        median_target_coverage = float(line['median_target_coverage'].replace(',','.'))
        pct_target_bases_1x = float(line['pct_target_bases_1x'].replace(',','.'))
        pct_target_bases_10x = float(line['pct_target_bases_10x'].replace(',','.'))
        pct_target_bases_100x = float(line['pct_target_bases_100x'].replace(',','.'))

        if not PicardTest.objects.filter(id_uvigo=id_uvigo).exists():
            _, created = PicardTest.objects.update_or_create(
                id_uvigo = id_uvigo,
                id_process = id_process,
                #date = '',
                mean_target_coverage = mean_target_coverage,
                median_target_coverage = median_target_coverage,
                pct_target_bases_1x = pct_target_bases_1x,
                pct_target_bases_10x = pct_target_bases_10x,
                pct_target_bases_100x = pct_target_bases_100x,
                )
def send_results_processing(file):
    data = file.read().decode('UTF-8')
    io_string = io.StringIO(data)
    dialect = csv.Sniffer().sniff(io_string.readline())
    io_string.seek(0)
    fieldnames = io_string.readline().strip().split(str(dialect.delimiter))
    sample_name = find_sample_name(file.name)

    # Detección del origen del archivo
    test = detect_file(fieldnames)
    
    if test != 'SingleCheckTest': # este no tiene cabecera
        # Cambio de nombres de campos a los de la base de datos
        for i in range(len(fieldnames)):
            substitute = fields_correspondence[test].get(fieldnames[i])
            if substitute:
                fieldnames[i] = substitute
        print(fieldnames)
    
        reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect)
        if test == 'PicardTest':
            upload_picard(reader, sample_name)
    
    else:
        io_string.seek(0)
        for line in io_string:
            print(line.strip().split(str(dialect.delimiter)))

