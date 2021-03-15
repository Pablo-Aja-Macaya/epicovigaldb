from django.db import models
import io, csv
import re
import pathlib
import datetime
import glob
import pickle
from upload.models import Sample

### Posibles tests ###
class PicardTest(models.Model): #.picardOutputCleaned.tsv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir del nombre del archivo
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
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

class SingleCheckTest(models.Model): #.trimmed.sorted.SingleCheck.txt
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir de columna (primera) (sin cabecera)
    id_process = models.CharField(max_length=40)

    autocorrelation = models.DecimalField(max_digits=15, decimal_places=10) 
    variation_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    gini_coefficient = models.DecimalField(max_digits=15, decimal_places=10) 
    mad = models.DecimalField(max_digits=15, decimal_places=10) 

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S") + ' (UTC)')

class NGSstatsTest(models.Model): #.ngsinfo.tsv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir de columna 'sampleName'
    id_process = models.CharField(max_length=40)

    total_reads = models.IntegerField()
    mapped = models.IntegerField()
    trimmed = models.IntegerField()

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S") + ' (UTC)')

class NextcladeTest(models.Model): #.csv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir de columna 'seqName'
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
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

class VariantsTest(models.Model): #.tsv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE) # a partir del nombre del archivo
    id_process = models.CharField(max_length=41)
    row = models.IntegerField()

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
        # unique_together = ('id_uvigo','row','id_process','date',)
        constraints = [
            models.UniqueConstraint(fields=['id_uvigo','row','id_process','date'], name='unique_constraint')
        ]
    def __str__(self):
        return str(self.id_uvigo) + f' - {self.row}' + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'

# #     # No sé si quieren estos
# #     # frequency
# #     # gene
# #     # aa_position
# #     # thresholds

class LineagesTest(models.Model): #.csv
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(Sample, on_delete=models.CASCADE)# a partir de columna 'taxon'
    id_process = models.CharField(max_length=40)

    lineage = models.CharField(max_length=10)
    probability = models.DecimalField(max_digits=7, decimal_places=6) 
    pangolearn_version = models.CharField(max_length=15, blank=True)
    comments = models.TextField(max_length=50, default=None, blank=True)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','id_process','date')
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S") + ' (UTC)')

class LineagesMostCommonCountries(models.Model):
    # Esta tabla se hace porque el atributo 'most common countries' de pangolin es multivaluado 'Spain,Portugal'
    id = models.AutoField(primary_key=True)
    id_uvigo = models.ForeignKey(LineagesTest, on_delete=models.CASCADE)
    id_process = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now=True)
    country = models.TextField(max_length=50, default=None, blank=True)
    
    def __str__(self):
        return str(self.id_uvigo + ' - ' + self.date.strftime("%m/%d/%Y, %H:%M:%S") + ' (UTC)')

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
        'id_uvigo':0,
        'autocorrelation':8,
        'variation_coefficient':9,
        'gini_coefficient':10,
        'mad':11,
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
        'Sequence name':'id_uvigo',
        'Lineage':'lineage',
        'Probability':'probability',
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
    sample_name = re.search(r'EPI\..+\.\d+\.',string)
    if sample_name:
        return sample_name.group()[:-1]
    else:
        return None


def comprobar_existencia(id_uvigo):
    '''
    Comprobación de la existencia de la muestra en la base de datos
    Si no existe se crea la entrada
    '''
    try:
        sample_reference = Sample.objects.get(id_uvigo=id_uvigo)
    except:
        _, created = Sample.objects.update_or_create(
                id_uvigo = id_uvigo,
                defaults = {
                    'id_uvigo' : id_uvigo,
                    'id_accession' : None,
                    'id_region' : None,
                    'original_name' : None,
                    'categoria_muestra':None,
                    'edad' : None,
                    'sexo' : None,
                    'patient_status' : None,
                    'nodo_secuenciacion' : None,
                    'fecha_muestra' : None,
                    'observaciones' : None                        
                }
            )
        sample_reference = Sample.objects.get(id_uvigo=id_uvigo)
    
    return sample_reference
    
###################################
### Subida según test #####
def upload_picard(reader, sample_name):
    for line in reader:
        id_uvigo = sample_name
        id_process = 'U-XXX'
        mean_target_coverage = float(line['mean_target_coverage'].replace(',','.'))
        median_target_coverage = float(line['median_target_coverage'].replace(',','.'))
        pct_target_bases_1x = float(line['pct_target_bases_1x'].replace(',','.'))
        pct_target_bases_10x = float(line['pct_target_bases_10x'].replace(',','.'))
        pct_target_bases_100x = float(line['pct_target_bases_100x'].replace(',','.'))

        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = PicardTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    'id_process' : id_process,
                    'mean_target_coverage' : mean_target_coverage,
                    'median_target_coverage' : median_target_coverage,
                    'pct_target_bases_1x' : pct_target_bases_1x,
                    'pct_target_bases_10x' : pct_target_bases_10x,
                    'pct_target_bases_100x' : pct_target_bases_100x,                   
                }
            )

def upload_singlecheck(io_string, delimiter):
    io_string.seek(0)

    # TO-DO: usar diccionario fields_correspondence
    id_uvigo_index = fields_correspondence['SingleCheckTest']['id_uvigo']
    autocorrelation_index = fields_correspondence['SingleCheckTest']['autocorrelation']
    variation_coefficient_index = fields_correspondence['SingleCheckTest']['variation_coefficient']
    gini_coefficient_index = fields_correspondence['SingleCheckTest']['gini_coefficient']
    mad_index = fields_correspondence['SingleCheckTest']['mad']

    for line in io_string:
        lista = line.strip().split(delimiter)

        id_uvigo = find_sample_name(lista[id_uvigo_index])
        id_process = 'U-XX'
        autocorrelation = lista[autocorrelation_index]
        variation_coefficient = lista[variation_coefficient_index]
        gini_coefficient = lista[gini_coefficient_index]
        mad = lista[mad_index]      

        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = SingleCheckTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    'id_process' : id_process,
                    'autocorrelation' : autocorrelation,
                    'variation_coefficient' : variation_coefficient,
                    'gini_coefficient' : gini_coefficient,
                    'mad' : mad,                  
                }
            )

def upload_ngsstats(reader):
    for line in reader:
        id_uvigo = line['id_uvigo'] # igual hay que poner aquí find_sample_name() también
        id_process = 'U-XXX'
        total_reads = int(line['total_reads'].replace(',','.'))
        mapped = int(line['mapped'].replace(',','.'))
        trimmed = int(line['trimmed'].replace(',','.'))
        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = NGSstatsTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    'id_process' : id_process,
                    'total_reads' : total_reads,
                    'mapped' : mapped,
                    'trimmed' : trimmed,                    
                }
            )

def upload_nextclade(reader):
    for line in reader:
        id_uvigo = find_sample_name(line['id_uvigo'])
        id_process = 'U-XXX'
        total_missing = int(line['total_missing'].replace(',','.'))
        clade = line['clade']
        qc_private_mutations_status = line['qc_private_mutations_status']
        qc_missing_data_status = line['qc_missing_data_status']
        qc_snp_clusters_status = line['qc_snp_clusters_status']
        qc_mixed_sites_status = line['qc_mixed_sites_status']

        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = NextcladeTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    'id_process' : id_process,
                    'total_missing' : total_missing,
                    'clade' : clade,
                    'qc_private_mutations_status' : qc_private_mutations_status,
                    'qc_missing_data_status' : qc_missing_data_status,
                    'qc_snp_clusters_status' : qc_snp_clusters_status,
                    'qc_mixed_sites_status' : qc_mixed_sites_status,                    
                }
            )


def upload_variants(reader, sample_name):
    id_uvigo = sample_name
    id_process = 'U-XXX'
    row = 0
    ## HAY QUE ARREGLAR ESTA SUBIDA
    ## HABRA QUE HACER LLAVE PRIMARIA DE id_uvigo y cada fila?
    if id_uvigo:
        for line in reader:
            pos = line['pos']
            ref = line['ref']
            alt = line['alt']
            alt_freq = line['alt_freq']
            ref_codon = line['ref_codon']
            ref_aa = line['ref_aa']
            alt_codon = line['alt_codon']
            alt_aa = line['alt_aa']

            sample_reference = comprobar_existencia(id_uvigo)
            _, created = VariantsTest.objects.update_or_create(
                id_uvigo=sample_reference,
                row=row,
                defaults={
                    'id_uvigo' : sample_reference,
                    'id_process' : id_process,
                    'row' : row,
                    'pos' : pos,
                    'ref' : ref,
                    'alt' : alt,
                    'alt_freq' : alt_freq,
                    'ref_codon' : ref_codon,
                    'ref_aa' : ref_aa,
                    'alt_codon' : alt_codon,
                    'alt_aa' : alt_aa,                    
                }
            )                
            row += 1

def upload_lineages(reader):
    for line in reader:
        id_uvigo = find_sample_name(line['id_uvigo'])
        id_process = 'U-XXX'
        lineage = line['lineage']
        probability = line['probability']
        countries = line['most_common_countries'].split(',')


        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = LineagesTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    'id_process' : id_process,
                    'lineage' : lineage,
                    'probability' : probability,
                    'comments' : ''                
                }
            )
            lineage_reference = LineagesTest.objects.get(id_uvigo=id_uvigo)
            for country in countries:
                country = country.strip()
                _, created = LineagesMostCommonCountries.objects.update_or_create(
                    id_uvigo=lineage_reference,
                    defaults={
                        'id_uvigo' : lineage_reference,
                        'id_process' : id_process,
                        'country' : country,
                
                    }
                )

################################
def select_test(test, file, sample_name, fieldnames, dialect):
    if test != 'SingleCheckTest': # este no tiene cabecera
        # Cambio de nombres de campos a los de la base de datos
        for i in range(len(fieldnames)):
            substitute = fields_correspondence[test].get(fieldnames[i])
            if substitute:
                fieldnames[i] = substitute

        reader = csv.DictReader(file, fieldnames=fieldnames, dialect=dialect)
        if test == 'PicardTest':
            upload_picard(reader, sample_name)
        elif test == 'NGSstatsTest':
            upload_ngsstats(reader)
        elif test == 'NextcladeTest':
            upload_nextclade(reader)
        elif test == 'VariantsTest':
            upload_variants(reader, sample_name)
        elif test == 'LineagesTest':
            upload_lineages(reader)
    else:
        upload_singlecheck(file, str(dialect.delimiter))

def send_results_processing(file):
    data = file.read().decode('UTF-8')
    io_string = io.StringIO(data)
    dialect = csv.Sniffer().sniff(io_string.readline())
    io_string.seek(0)
    fieldnames = io_string.readline().strip().split(str(dialect.delimiter))
    sample_name = find_sample_name(file.name)

    # Detección del origen del archivo
    test = detect_file(fieldnames)
    select_test(test, io_string, sample_name, fieldnames, dialect)


#######################################
### Actualización desde carpeta
# def update():
#     # Update database if there are new files in a folder or these have been modified
#     pckl = 'objs.pkl'
#     pckl_folder = '/home/pabs/MasterBioinformatica/TFM/test/'
#     folder = '/home/pabs/MasterBioinformatica/TFM/test/carpeta_prueba_inputs/'



#     updated = 0
#     unchanged = 0
#     new = 0

#     # Si se ha hecho previamente un pckl con los archivos y sus fechas
#     if glob.glob(pckl_folder+'*.pkl'):
#         with open(pckl_folder+pckl, 'rb') as f:
#             file_history = pickle.load(f)
#         files = glob.glob(folder+'*')
#         for f in files:
#             fname = pathlib.Path(f)
#             mtime = fname.stat().st_mtime # Time of most recent content modification expressed in seconds.

#             # Si el nombre del archivo ya se ha visto en el pasado
#             if file_history.get(fname.name):
#                 # Ver diferencia de tiempos respecto al valor
#                 # del pickle, si son diferentes actualizar la base de datos
#                 if file_history[fname.name] != mtime:
#                     with open(fname, 'rt') as fichero:
#                         dialect = csv.Sniffer().sniff(fichero.readline())
#                         fichero.seek(0)
#                         fieldnames = fichero.readline().strip().split(str(dialect.delimiter))
#                         sample_name = find_sample_name(fname.name)

#                         # Detección del origen del archivo
#                         test = detect_file(fieldnames)    

#                         # Actualizar base de datos
#                         select_test(test, fichero, sample_name, fieldnames, dialect)

#                     # Se guarda en el diccionario la nueva fecha de modificación
#                     file_history[fname.name] = mtime
#                     updated += 1

#                 else:
#                     unchanged += 1

#             # Si el nombre del archivo es nuevo    
#             else:
#                 file_history[fname.name] = mtime
#                 # insertar los datos del archivo en la base de datos
#                 with open(fname, 'rt') as fichero:
#                     dialect = csv.Sniffer().sniff(fichero.readline())
#                     fichero.seek(0)
#                     fieldnames = fichero.readline().strip().split(str(dialect.delimiter))
#                     sample_name = find_sample_name(fname.name)

#                     # Detección del origen del archivo
#                     test = detect_file(fieldnames)    

#                     # Insertar en base de datos
#                     select_test(test, fichero, sample_name, fieldnames, dialect)
                
#                 new += 1

#         with open(pckl_folder+pckl, 'wb') as fichero:
#             pickle.dump(file_history, fichero)
    
#     # Si no hay un pckl coger todos los archivos y actualziar la base de datos
#     # después hacer un pckl
#     # Esto es para la primera vez    
#     else:
#         file_history = {}
#         files = glob.glob(folder+'*')
#         for f in files:
#             fname = pathlib.Path(f)
#             mtime = fname.stat().st_mtime # Time of most recent content modification expressed in seconds.

#             with open(fname, 'rt') as fichero:
#                 dialect = csv.Sniffer().sniff(fichero.readline())
#                 fichero.seek(0)
#                 fieldnames = fichero.readline().strip().split(str(dialect.delimiter))
#                 sample_name = find_sample_name(fname.name)

#                 # Detección del origen del archivo
#                 test = detect_file(fieldnames)    

#                 # Insertar en base de datos
#                 select_test(test, fichero, sample_name, fieldnames, dialect)

#             # Se guarda en el diccionario fecha de modificación
#             file_history[fname.name] = mtime
        
#         new += 1

#         with open(pckl_folder+pckl, 'wb') as fichero:
#             pickle.dump(file_history, fichero)
    
#     return unchanged, updated, new

def update():
    # Update database if there are new files in a folder or these have been modified
    pckl = 'objs.pkl'
    pckl_folder = '/home/pabs/MasterBioinformatica/TFM/test/'
    
    folder_base = '/home/pabs/MasterBioinformatica/TFM/test/testcesga/'
    
    subfolders = []
    target_folders = ['picard','nextclade','pangolin','ngs','variants']
    for i in target_folders:
        subfolders.append(folder_base + i +'/') # cada uno es un /path/to/target_folder/ ... ej: /path/to/nextclade/
    
    updated = 0
    unchanged = 0
    new = 0

    # Si se ha hecho previamente un pckl con los archivos y sus fechas
    if glob.glob(pckl_folder+pckl):
        with open(pckl_folder+pckl, 'rb') as f:
            file_history = pickle.load(f)
        
        for folder in subfolders:
            print(folder)
            files = glob.glob(folder+'*')

            for f in files:
                fname = pathlib.Path(f)
                mtime = fname.stat().st_mtime # Time of most recent content modification expressed in seconds.

                # Si el nombre del archivo ya se ha visto en el pasado
                if file_history.get(fname.name):
                    # Ver diferencia de tiempos respecto al valor
                    # del pickle, si son diferentes actualizar la base de datos
                    if file_history[fname.name] != mtime:
                        with open(fname, 'rt') as fichero:
                            dialect = csv.Sniffer().sniff(fichero.readline())
                            fichero.seek(0)
                            fieldnames = fichero.readline().strip().split(str(dialect.delimiter))
                            sample_name = find_sample_name(fname.name)

                            # Detección del origen del archivo
                            test = detect_file(fieldnames)    

                            # Actualizar base de datos
                            select_test(test, fichero, sample_name, fieldnames, dialect)

                        # Se guarda en el diccionario la nueva fecha de modificación
                        file_history[fname.name] = mtime
                        updated += 1

                    else:
                        unchanged += 1

                # Si el nombre del archivo es nuevo    
                else:
                    file_history[fname.name] = mtime
                    # insertar los datos del archivo en la base de datos
                    with open(fname, 'rt') as fichero:
                        dialect = csv.Sniffer().sniff(fichero.readline())
                        fichero.seek(0)
                        fieldnames = fichero.readline().strip().split(str(dialect.delimiter))
                        sample_name = find_sample_name(fname.name)

                        # Detección del origen del archivo
                        test = detect_file(fieldnames)    

                        # Insertar en base de datos
                        select_test(test, fichero, sample_name, fieldnames, dialect)
                    
                    new += 1

            with open(pckl_folder+pckl, 'wb') as fichero:
                pickle.dump(file_history, fichero)
    
    # Si no hay un pckl coger todos los archivos y actualziar la base de datos
    # después hacer un pckl
    # Esto es para la primera vez    
    else:
        file_history = {}
        for folder in subfolders:
            files = glob.glob(folder+'*')

            for f in files:
                fname = pathlib.Path(f)
                mtime = fname.stat().st_mtime # Time of most recent content modification expressed in seconds.

                with open(fname, 'rt') as fichero:
                    dialect = csv.Sniffer().sniff(fichero.readline())
                    fichero.seek(0)
                    fieldnames = fichero.readline().strip().split(str(dialect.delimiter))
                    sample_name = find_sample_name(fname.name)

                    # Detección del origen del archivo
                    test = detect_file(fieldnames)    

                    # Insertar en base de datos
                    select_test(test, fichero, sample_name, fieldnames, dialect)

                # Se guarda en el diccionario fecha de modificación
                file_history[fname.name] = mtime
            
            new += 1

            with open(pckl_folder+pckl, 'wb') as fichero:
                pickle.dump(file_history, fichero)
    
    return unchanged, updated, new
