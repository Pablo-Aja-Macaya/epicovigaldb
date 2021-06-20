######################
# Ejecución de tests #
from epicovigal.celery import app

from epicovigal.local_settings import TESTS_FOLDER_BASE
from tests.subida_tests import find_sample_name

import glob
import subprocess
from datetime import datetime

## FUNCIONES DE STATUS
from jobstatus.models import start_process, finish_process, failed_process

# Paths generales
TESTS_OUTPUT_TMP = '../tests_output_tmp'
TESTS_OUTPUT = '../tests_output'

# Paths nextclade
NEXTCLADE_FOLDER = '../tools/nextclade/data/sars-cov-2'
NEXTCLADE_OUTPUT_FOLDER = '../output'
NEXTCLADE_EXECUTABLE = '../tools/nextclade_exe'
NEXTCLADE_ROOT_SEQ = f'{NEXTCLADE_FOLDER}/reference.fasta'
NEXTCLADE_INPUT_TREE = f'{NEXTCLADE_FOLDER}/tree.json'
NEXTCLADE_QC_CONFIG = f'{NEXTCLADE_FOLDER}/qc.json'
NEXTCLADE_GENE_MAP = f'{NEXTCLADE_FOLDER}/genemap.gff'

# Paths picard
PICARD_EXECUTABLE = '../tools/picard.jar'
PICARD_REF_FASTA = '/mnt/epicovigal/references/nCoV-2019.reference.fasta'
PICARD_LIST_AMPLICONS="/mnt/epicovigal/references/list_amplicons.interval_list"

# Nombres de archivos
def find_target_names(folder, suffix):
    files = glob.glob(f'{folder}/*{suffix}')
    return files

def available_ids(target_folder, target_suffix):
    f = f'{TESTS_FOLDER_BASE}{target_folder}'
    files = sorted(find_target_names(f,target_suffix))
    return files

# Ejecución de tests
def clean_spaces(cmd):
    # Limpiar espacios en comando
    cmd = [x for x in cmd.split(' ') if x]
    cmd = ' '.join(cmd)
    return cmd

def get_command_nextclade(fasta_file, output_folder=NEXTCLADE_OUTPUT_FOLDER, nextclade_executable=NEXTCLADE_EXECUTABLE, root_seq=NEXTCLADE_ROOT_SEQ, input_tree=NEXTCLADE_INPUT_TREE, qc_config=NEXTCLADE_QC_CONFIG, gene_map=NEXTCLADE_GENE_MAP):
    name = find_sample_name(fasta_file)
    output_csv = f'{TESTS_OUTPUT}/{name}.csv'

    # Comando    
    cmd = f'{nextclade_executable} --input-fasta {fasta_file} \
        --input-root-seq {root_seq} --input-tree {input_tree} \
        --input-qc-config {qc_config} --output-csv {output_csv}' 

    # Limpiar espacios en comando
    cmd = clean_spaces(cmd)

    return cmd

def get_command_picard(archivo, picard_path=PICARD_EXECUTABLE, ref_fasta=PICARD_REF_FASTA, list_amplicons=PICARD_LIST_AMPLICONS):
    name = find_sample_name(archivo)

    input_bam=f"{archivo}"
    output_picard=f"{TESTS_OUTPUT}/output_pcr_{name}.txt"

    cmd = f'java -jar {picard_path} CollectTargetedPcrMetrics I={input_bam} O={output_picard}\
         R={ref_fasta} AMPLICON_INTERVALS={list_amplicons} TARGET_INTERVALS={list_amplicons} COVERAGE_CAP=23000'

    # Limpiar espacios en comando
    cmd = clean_spaces(cmd)

    return cmd

def find_test_data(test):
    if test == 'Nextclade':
        target_folder = 'consensus'
        target_suffix = 'consensus.fa'
        cmd_function = test
    elif test == 'Picard':
        target_folder = 'ngs'
        target_suffix = 'trimmed.sorted.bam'
        cmd_function = test
    return available_ids(target_folder, target_suffix), cmd_function


# Variables
CMD_FUNCTION_DICT = {'Nextclade':get_command_nextclade, 'Picard':get_command_picard}


@app.task(bind=True)
def execute_command(self, files, cmd_function, execute_from_here=TESTS_OUTPUT_TMP):
    start = datetime.now()
    id = self.request.id
    command = 'Ejecucion_Test'
    start_process(id, command, start.strftime('%Y-%m-%d %H:%M:%S'))
    print(f'Starting tests... (Task ID: {id})')

    try:
        cmd_function = CMD_FUNCTION_DICT[cmd_function]
        for i in files:
            # Ejecución de test
            cmd = cmd_function(i)
            p = subprocess.call(cmd, cwd=execute_from_here, shell=True)
            # Comando para limpiar archivos temporales
            p = subprocess.call('rm ./*', cwd=execute_from_here, shell=True)
        finish = datetime.now()
        elapsed_time = finish - start
        finish_process(id, elapsed_time.seconds, 'Ejecución sin errores terminales')
    except:
        finish = datetime.now()
        elapsed_time = finish - start
        failed_process(id, elapsed_time.seconds, 'Error')


