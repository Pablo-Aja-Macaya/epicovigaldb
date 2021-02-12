from django.db import models
import io, csv

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

    # No sé si quieren estos
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
    # TO-DO añadir columna de comentarios
    def __str__(self):
        return str(self.id_process)



#############################################################################
### Functions ###
# from tests.tasks import check_status

# def prueba():
#     check_status.delay()


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

def send_results_processing(file):
    fields_correspondence = {
        # Picard #.picardOutputCleaned.tsv
        'PicardTest':{
            'MEAN_TARGET_COVERAGE':'mean_target_coverage',
            'MEDIAN_TARGET_COVERAGE':'median_target_coverage',
            'PCT_TARGET_BASES_1X':'pct_target_bases_1x',
            'PCT_TARGET_BASES_10X':'pct_target_bases_10x',
            'PCT_TARGET_BASES_100X':'pct_target_bases_100x',
        },
        # SingleCheck #.trimmed.sorted.SingleCheck.txt
        # Este no tiene cabecera así que se usa el índice de la columna
        'SingleCheckTest':{
            8:'autocorrelation',
            9:'variation_coefficient',
            10:'gini_coefficient',
            11:'mad',
        },
        # NGSStats #.ngsinfo.tsv
        'NGSstatsTest':{
            'totalReads':'total_reads',
            'mapped':'mapped',
            'trimmed':'trimmed',       
        },
        # Nextclade # .csv
        'NextcladeTest':{
            'totalMissing':'total_missing',
            'clade':'clade',
            'qc.privateMutations.status':'qc_private_mutations_status',
            'qc.missingData.status':'qc_missing_data_status',
            'qc.snpClusters.status':'qc_snp_clusters_status',
            'qc.mixedSites.status':'qc_mixed_sites_status',   
        },
        # iVar #.tsv
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
        'LineagesTest':{
            'Lineage':'lineage',
            'Probability':'probability',
            'Sequence name':'',### añadir a modelo
            'Most common countries':'most_common_countries' ### añadir a modelo
            # TO-DO añadir columna de comentarios
        },
    }
    
    data = file.read().decode('UTF-8')
    io_string = io.StringIO(data)
    dialect = csv.Sniffer().sniff(io_string.readline())
    io_string.seek(0)
    fieldnames = io_string.readline().strip().split(str(dialect.delimiter))
    print(file)
    
    # Cambio de nombres de campos a los de la base de datos 
    test = detect_file(fieldnames)
    if test != 'SingleCheckTest': # este no tiene cabecera
        for i in range(len(fieldnames)):
            substitute = fields_correspondence[test].get(fieldnames[i])
            if substitute:
                fieldnames[i] = substitute
        print(fieldnames)
    
        reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect)
        for line in reader:
            print(line)     
    
    else:
        io_string.seek(0)
        for line in io_string:
            print(line.strip().split(str(dialect.delimiter)))

