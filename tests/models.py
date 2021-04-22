from django.db import models
import io, csv
import re
import pathlib
import datetime
import glob
import pickle
from upload.models import Sample
import traceback

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

    pos = models.IntegerField()
    ref = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)
    alt_freq = models.DecimalField(max_digits=7, decimal_places=6) 
    ref_codon = models.CharField(max_length=100)
    ref_aa = models.CharField(max_length=100)
    alt_codon = models.CharField(max_length=100)
    alt_aa = models.CharField(max_length=100)

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
    probability = models.DecimalField(max_digits=7, decimal_places=6) 
    most_common_countries = models.ManyToManyField(Country)
    pangolearn_version = models.CharField(max_length=15, blank=True, null=True)
    comments = models.TextField(max_length=50, default=None, blank=True, null=True)

    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_uvigo','date')
    def __str__(self):
        return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'




# class LineagesMostCommonCountries(models.Model):
#     # Esta tabla se hace porque el atributo 'most common countries' de pangolin es multivaluado 'Spain,Portugal'
#     id = models.AutoField(primary_key=True)
#     id_uvigo = models.ForeignKey(LineagesTest, on_delete=models.CASCADE)
#     # id_process = models.CharField(max_length=40)
#     date = models.DateTimeField(auto_now=True)
#     country = models.CharField(max_length=30, default=None, blank=True)

#     class Meta:
#         unique_together = ('id_uvigo','country')    
#     def __str__(self):
#         return str(self.id_uvigo) + ' - ' + str(self.date.strftime("%m/%d/%Y, %H:%M:%S")) + ' (UTC)'


# class ModeloPrueba(models.Model):
#     id_uvigo = models.IntegerField(primary_key=True)
#     atr1 = models.CharField(max_length=10)



#############################################################################
### Functions ###
# from tests.tasks import check_status
import time


# def prueba():
#     check_status.delay()
fields_correspondence = {
    # Picard #.picardOutputCleaned.tsv
    # Muestra a partir del nombre del archivo
    'PicardTest':{
        'mean_target_coverage':'mean_target_coverage',
        'median_target_coverage':'median_target_coverage',
        'pct_target_bases_1x':'pct_target_bases_1x',
        'pct_target_bases_10x':'pct_target_bases_10x',
        'pct_target_bases_100x':'pct_target_bases_100x',
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
        'samplename':'id_uvigo',
        'totalreads':'total_reads',
        'mapped':'mapped',
        'trimmed':'trimmed',       
    },
    # Nextclade # .csv
    # Muestra a partir de columna 'seqName'
    'NextcladeTest':{
        'seqname':'id_uvigo',
        'totalmissing':'total_missing',
        'clade':'clade',
        'qc.privatemutations.status':'qc_private_mutations_status',
        'qc.missingdata.status':'qc_missing_data_status',
        'qc.snpclusters.status':'qc_snp_clusters_status',
        'qc.mixedsites.status':'qc_mixed_sites_status',   
    },
    # iVar #.tsv
    # Muestra a partir del nombre del archivo
    'VariantsTest':{
        'pos':'pos',
        'ref':'ref',
        'alt':'alt',
        'alt_freq':'alt_freq', 
        'ref_codon':'ref_codon',
        'ref_aa':'ref_aa',
        'alt_codon':'alt_codon',
        'alt_aa':'alt_aa',           
    },
    # Pangolin # .csv
    # Muestra a partir de columna 'taxon'
    'LineagesTest':{
        'sequence name':'id_uvigo',
        'taxon':'id_uvigo',
        'lineage':'lineage',
        'probability':'probability',
        'most common countries':'most_common_countries',
        # Extras de versión de herramienta local:
        'pangolearn_version':'pangolearn_version',
        'note':'comments'

    },
}

def detect_file(header):
    # Detección del tipo de archivo 

    # Este diccionario llevará la cuenta de cuántos campos del archivo se han encontrado para cada test
    # Se hace en caso de que haya atributos comunes en los archivos
    probs = {
        'NextcladeTest':0,
        'NGSstatsTest':0,
        'PicardTest':0,
        'SingleCheckTest':0, 
        'VariantsTest':0,
        'LineagesTest':0,
    }
    for test,fields in fields_correspondence.items():
        for name_org in fields.keys():
            if name_org in header:
                #print(True, test)
                probs[test] += 1

    # Conseguir test con el mayor número de columnas comunes con el archivo
    possible_test = max(probs, key=probs.get)
    # Si no ha habido ninguna columna común significará que lo más probable es que sea de SingleCheck (no tiene nombres de columnas)
    if probs[possible_test] == 0:
        return 'SingleCheckTest'
    else:
        return possible_test

def find_sample_name(string):
    # Encontrar si una cadena contiene alguna de las siguientes cosas:
        # Posibilidades:  EPI.X.N , SERGAS.X.N y VAL.X.N
    formats = [r'EPI\..+\.\d+.\.', r'SERGAS\..+\.\d+.\.', r'VAL\..+\.\d+.\.']
    accept = False
    # Probar las posibilidades, si encaja alguna se devuelve el nombre obtenido
    for i in formats:
        sample_name = re.search(i,string+'.')
        if sample_name:
            return sample_name.group()[:-1]
    # Si ninguna encaja se devuelve None
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
        id_uvigo = find_sample_name(sample_name)
        # id_process = 'U-XXX'
        mean_target_coverage = float(line.get('mean_target_coverage','').replace(',','.'))
        median_target_coverage = float(line.get('median_target_coverage','').replace(',','.'))
        pct_target_bases_1x = float(line.get('pct_target_bases_1x','').replace(',','.'))
        pct_target_bases_10x = float(line.get('pct_target_bases_10x','').replace(',','.'))
        pct_target_bases_100x = float(line.get('pct_target_bases_100x','').replace(',','.'))

        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = PicardTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    # 'id_process' : id_process,
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
    # Esto nos da la posición de la linea donde se encuentra el valor para cada tributo
    id_uvigo_index = fields_correspondence['SingleCheckTest']['id_uvigo']
    autocorrelation_index = fields_correspondence['SingleCheckTest']['autocorrelation']
    variation_coefficient_index = fields_correspondence['SingleCheckTest']['variation_coefficient']
    gini_coefficient_index = fields_correspondence['SingleCheckTest']['gini_coefficient']
    mad_index = fields_correspondence['SingleCheckTest']['mad']

    for line in io_string:
        lista = line.strip().split(delimiter)

        id_uvigo = find_sample_name(lista[id_uvigo_index])
        # id_process = 'U-XX'
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
                    # 'id_process' : id_process,
                    'autocorrelation' : autocorrelation,
                    'variation_coefficient' : variation_coefficient,
                    'gini_coefficient' : gini_coefficient,
                    'mad' : mad,                  
                }
            )

def upload_ngsstats(reader):
    for line in reader:
        id_uvigo = find_sample_name(line.get('id_uvigo')) # igual hay que poner aquí find_sample_name() también
        # id_process = 'U-XXX'
        total_reads = int(line.get('total_reads','').replace(',','.'))
        mapped = int(line.get('mapped','').replace(',','.'))
        trimmed = int(line.get('trimmed','').replace(',','.'))
        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = NGSstatsTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    # 'id_process' : id_process,
                    'total_reads' : total_reads,
                    'mapped' : mapped,
                    'trimmed' : trimmed,                    
                }
            )

def upload_nextclade(reader):
    for line in reader:
        id_uvigo = find_sample_name(line.get('id_uvigo'))
        # id_process = 'U-XXX'
        total_missing = int(line.get('total_missing','').replace(',','.'))
        clade = line.get('clade')
        qc_private_mutations_status = line.get('qc_private_mutations_status')
        qc_missing_data_status = line.get('qc_missing_data_status')
        qc_snp_clusters_status = line.get('qc_snp_clusters_status')
        qc_mixed_sites_status = line.get('qc_mixed_sites_status')

        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)

            _, created = NextcladeTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    # 'id_process' : id_process,
                    'total_missing' : total_missing,
                    'clade' : clade,
                    'qc_private_mutations_status' : qc_private_mutations_status,
                    'qc_missing_data_status' : qc_missing_data_status,
                    'qc_snp_clusters_status' : qc_snp_clusters_status,
                    'qc_mixed_sites_status' : qc_mixed_sites_status,                    
                }
            )


def upload_variants(reader, sample_name):
    id_uvigo = find_sample_name(sample_name)
    # id_process = 'U-XXX'
    row = 0
    if id_uvigo:
        #### METODO 1 - MAS RAPIDO QUE EL update_or_create, se reduce el tiempo al 30% en principio
        lista_objs_update = []
        lista_objs_create = []
        for line in reader:
            pos = line.get('pos')
            ref = line.get('ref')
            alt = line.get('alt')
            alt_freq = line.get('alt_freq')
            ref_codon = line.get('ref_codon')
            ref_aa = line.get('ref_aa')
            alt_codon = line.get('alt_codon')
            alt_aa = line.get('alt_aa')

            sample_reference = comprobar_existencia(id_uvigo)
            pk = VariantsTest.objects.values('pk').filter(id_uvigo=id_uvigo,row=row)
            if pk:
                # Llave primaria ya existe --> Actualización
                obj = VariantsTest.objects.get(id_uvigo=id_uvigo,row=row)
                obj.id_uvigo = sample_reference
                # obj.id_process = id_process
                obj.pos = pos
                obj.ref = ref
                obj.alt = alt
                obj.alt_freq = alt_freq
                obj.ref_codon = ref_codon
                obj.ref_aa = ref_aa
                obj.alt_codon = alt_codon
                obj.alt_aa = alt_aa                 
                lista_objs_update.append(obj)
            else:
                # Llave primaria no existe --> Creación
                obj = VariantsTest(
                    id_uvigo = sample_reference,
                    # id_process = id_process,
                    row = row,
                    pos = pos,
                    ref = ref,
                    alt = alt,
                    alt_freq = alt_freq,
                    ref_codon = ref_codon,
                    ref_aa = ref_aa,
                    alt_codon = alt_codon,
                    alt_aa = alt_aa,                  
                )
                lista_objs_create.append(obj)
            
            row += 1

        # BULK UPDATE
        update_fields = ['id_uvigo','pos','ref','alt','alt_freq','ref_codon','ref_aa','alt_codon','alt_aa']
        VariantsTest.objects.bulk_update(lista_objs_update, update_fields, batch_size=100)
        
        # BULK CREATE
        VariantsTest.objects.bulk_create(lista_objs_create, batch_size=100, ignore_conflicts=True)           


def upload_lineages(reader):
    for line in reader:
        id_uvigo = find_sample_name(line.get('id_uvigo'))
        # id_process = 'U-XXX'
        lineage = line.get('lineage')
        probability = line.get('probability')
        countries = line.get('most_common_countries','').split(',')
        pangolearn_version = line.get('pangolearn_version')

        if id_uvigo:
            sample_reference = comprobar_existencia(id_uvigo)
            _, created = LineagesTest.objects.update_or_create(
                id_uvigo=sample_reference,
                defaults={
                    'id_uvigo' : sample_reference,
                    # 'id_process' : id_process,
                    'lineage' : lineage,
                    'probability' : probability,
                    'comments' : '',
                    'pangolearn_version':pangolearn_version             
                }
            )
            lineage_reference = LineagesTest.objects.get(id_uvigo=id_uvigo)
            for country in countries:
                c = Country(name=country.strip())
                c.save()
                lineage_reference.most_common_countries.add(c)

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
    data = file.read().decode('utf-8-sig')
    io_string = io.StringIO(data)
    dialect = csv.Sniffer().sniff(io_string.readline())
    io_string.seek(0)
    fieldnames = io_string.readline().strip().lower().split(str(dialect.delimiter))
    # sin lo de lower: io_string.readline().strip().split(str(dialect.delimiter))

    sample_name = find_sample_name(file.name)

    # Detección del origen del archivo
    test = detect_file(fieldnames)
    select_test(test, io_string, sample_name, fieldnames, dialect)


#######################################
### Actualización desde carpeta

def read_log(log_file):
    with open(log_file,'rt') as log:
        lista = []
        for line in log:
            dicc = eval(line)
            lista.append(dicc)
    return lista


def write_log(log_file, fname, traceback, error):
    error_log_file = log_file
    with open(error_log_file, 'at') as log:
        dicc = {
        'archivo':fname,
        'error':error,
        'traceback':str(traceback.format_exc()).replace('"',' ').replace("'", ' ')
        }
        log.write(str(dicc)+'\n')


def update_database(fichero, fname):
    dialect = csv.Sniffer().sniff(fichero.readline())
    fichero.seek(0)
    fieldnames = fichero.readline().strip().lower().split(str(dialect.delimiter))
    sample_name = find_sample_name(fname.name)

    # Detección del origen del archivo
    test = detect_file(fieldnames)    

    # Actualizar/Insertar en base de datos
    select_test(test, fichero, sample_name, fieldnames, dialect)


def update():
    from epicovigal.local_settings import TESTS_PCKL_FOLDER, TESTS_FOLDER_BASE
    # Update database if there are new files in a folder or these have been modified
    pckl = 'objs.pkl'
    error_log_file = './test_update_error_log.txt'
    with open(error_log_file,'wt') as f: # se elimina el log anterior
        pass
    
    # En local
    pckl_folder = TESTS_PCKL_FOLDER
    folder_base = TESTS_FOLDER_BASE

    subfolders = []
    target_folders = ['nextclade','pangolin','reportData','variants']# 'ngs' 'picard','singlecheck' (estos 3 están dentro de 'reportData')
    for i in target_folders:
        subfolders.append(folder_base + i +'/') # cada uno es un /path/to/target_folder/ ... ej: /path/to/nextclade/
    
    updated = 0
    unchanged = 0
    new = 0
    errors = 0

    # Si se ha hecho previamente un pckl con los archivos y sus fechas
    if glob.glob(pckl_folder+pckl):
        with open(pckl_folder+pckl, 'rb') as f:
            file_history = pickle.load(f)
        
        for folder in subfolders:
            files = glob.glob(folder+'*')
            for f in files:
                fname = pathlib.Path(f)
                
                if '_filtered.tsv' in str(fname):
                    # El programa se salta estos archivos porque dan error seguro
                    continue

                mtime = fname.stat().st_mtime # Time of most recent content modification expressed in seconds.
                try:
                    # Si el nombre del archivo ya se ha visto en el pasado
                    if file_history.get(fname.name):
                        # Ver diferencia de tiempos respecto al valor
                        # del pickle, si son diferentes actualizar la base de datos
                        if file_history[fname.name] != mtime:
                            with open(fname, 'rt') as fichero:
                                update_database(fichero, fname)
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
                            update_database(fichero, fname)
                        new += 1

                except Exception as e:
                    write_log(error_log_file, fname, traceback, e)
                    file_history.pop(fname.name, None)
                    errors += 1

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
                try:
                    with open(fname, 'rt') as fichero:
                        update_database(fichero, fname)
                    # Se guarda en el diccionario fecha de modificación
                    file_history[fname.name] = mtime
                    new += 1

                except Exception as e:
                    write_log(error_log_file, fname, traceback, e)
                    file_history.pop(fname.name, None)
                    errors += 1


                with open(pckl_folder+pckl, 'wb') as fichero:
                    pickle.dump(file_history, fichero)
    
    return unchanged, updated, new, errors

