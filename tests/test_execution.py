######################
# Ejecución de tests #

from epicovigal.local_settings import TESTS_FOLDER_BASE
import glob
import subprocess

# Paths generales
TESTS_OUTPUT_TMP = '../tests_output_tmp'
TESTS_OUTPUT = '../tests_output'

# Paths nextclade
NEXTCLADE_FOLDER = '../tools/nextclade/data/sars-cov-2'
NEXTCLADE_OUTPUT_FOLDER = '../output'
NEXTCLADE_EXECUTABLE = '../tools/nextclade_exe'
NEXTCLADE_ROOT_SEQ = f'{NEXTCLADE_FOLDER}/root_seq'
NEXTCLADE_INPUT_TREE = f'{NEXTCLADE_FOLDER}/input_tree'
NEXTCLADE_QC_CONFIG = f'{NEXTCLADE_FOLDER}/qc_config'
NEXTCLADE_GENE_MAP = f'{NEXTCLADE_FOLDER}/gene_map'

# Paths picard



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
    output_csv = f'{TESTS_OUTPUT}/prueba.csv'

    # Comando    
    cmd = f'{nextclade_executable} --input-fasta {fasta_file} \
        --input-root-seq {root_seq} --input-tree {input_tree} \
        --input-qc-config {qc_config} --output-csv {output_csv}' 

    # Limpiar espacios en comando
    cmd = clean_spaces(cmd)

    return cmd

def get_command_picard(archivo, ):
    output_picard="output_pcr_.txt"
    input_bam=f"{archivo}.trimmed.sorted.bam"
    picard_path = 'path/to/picard'
    ref_fasta = 'path/ref_fasta'
    list_amplicons = 'path/list_amplicons'

    cmd = f'java -jar {picard_path} CollectTargetedPcrMetrics I={input_bam} O={output_picard}\
         R={ref_fasta} AMPLICON_INTERVALS={list_amplicons} TARGET_INTERVALS={list_amplicons} COVERAGE_CAP=23000'

    # Limpiar espacios en comando
    cmd = clean_spaces(cmd)

    return cmd

def find_test_data(test):
    if test == 'Nextclade':
        target_folder = 'consensus'
        target_suffix = 'consensus.fa'
        cmd_function = get_command_nextclade
    elif test == 'Picard':
        target_folder = 'ngs'
        target_suffix = 'trimmed.sorted.bam'
        cmd_function = get_command_picard
    return available_ids(target_folder, target_suffix), cmd_function


def execute_command(cmd, execute_from_here=TESTS_OUTPUT_TMP):
    # Ejecución de test
    p = subprocess.call(cmd, cwd=execute_from_here, shell=True)
    # Comando para limpiar archivos temporales
    # p = subprocess.call('rm ./*', cwd=execute_from_here, shell=True)

# return cmd

# target_folder = 'ngs'
# target_suffix = 'sorted.bam'
# available_ids(target_folder, target_suffix)

# target_folder = 'consensus'
# target_suffix = 'consensus.fa'
# target_files = available_ids(target_folder, target_suffix)

# execute_nextclade('fasta.consensus.fa')

### Form 1 ###
# Presentar posibles tests --> Eligen uno
### Form 2 ###
# Presentar posibles muestras --> Eligen una lista
# Presentar variables elegidas

