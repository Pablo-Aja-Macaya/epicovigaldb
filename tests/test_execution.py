######################
# Ejecución de tests #

from epicovigal.local_settings import TESTS_FOLDER_BASE
import glob
import subprocess

# Nombres de archivos
def find_target_names(folder, suffix):
    files = glob.glob(f'{folder}/*{suffix}')
    return files

def available_ids(target_folder, target_suffix):
    f = f'{TESTS_FOLDER_BASE}{target_folder}'
    files = sorted(find_target_names(f,target_suffix))
    return files

# Ejecución de tests
def execute_nextclade(fasta_file):
    output_folder = 'path/to/output'
    nextclade_executable = 'path/to/nextclade'
    root_seq = 'path/root_seq'
    input_tree = 'path/input_tree'
    qc_config = 'path/qc_input'
    gene_map = 'path/gene_map'
    output_csv = 'path/output'
    cmd = f'{nextclade_executable} --input-fasta {fasta_file} \
        --input-root-seq {root_seq} --input-tree {input_tree} \
        --input-qc-config {qc_config} --output-csv {output_csv}' 
    # p = subprocess.Popen(['ls'], cwd=output_folder)
    # p.wait()
    # return cmd
    print(cmd)

def find_test_data(test):
    if test == 'Nextclade':
        target_folder = 'consensus'
        target_suffix = 'consensus.fa'
    elif test == 'Picard':
        target_folder = 'ngs'
        target_suffix = 'trimmed.sorted.bam'
    return available_ids(target_folder, target_suffix)

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

