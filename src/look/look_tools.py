from subprocess import call
import random
import os
from numpy.random import choice

def make_neutral_edits(temp_folder, neutral_edits):
    cwd = os.getcwd() + '/'
    n_prog_path = cwd + 'n_prog_code/'
    tar_path = n_prog_path + 'look-example.tar.gz'
    repair_path = n_prog_path + 'repair'

    # make a directory for n-prog and GenProg to use
    call('mkdir -p ' + temp_folder, shell=True)

    # copy the relevant files over
    call('tar -xf ' + tar_path + ' -C ' + temp_folder, shell=True)

    # move things down a directory for simpler paths
    call('mv ' + temp_folder + '/look-example/* ' + temp_folder, shell=True)
    call('rm -r ' + temp_folder + '/look-example', shell=True)

    # call n-prog
    call('cd n_prog_code && ./n-prog -d ' + temp_folder + ' -r ' +
         repair_path + ' -n 1 -k ' + str(neutral_edits) + ' -x ' +
         str(neutral_edits * 10) + ' -s ' + str(random.getrandbits(32)),
         shell=True)


def get_neutral_edits(temp_folder, neutral_edits):
    generated_neutral_edits = []

    # open the debug file
    with open(temp_folder + '/repair.debug/repair.debug.original', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # parse it for neutral edits
            if line.find('is neutral') != -1:
                generated_neutral_edits.append(line[line.find('+') + 1:
                line.find('is neutral')].strip())

    # select 100 of them at random and return that list
    generated_neutral_edits = random.sample(generated_neutral_edits, neutral_edits)

    return generated_neutral_edits


def generate_edit_string(edits, probabilities):
    edit_one = 'a'
    edit_two = 'a'
    while edit_one == edit_two:
        edit_one = choice(edits, p=probabilities[0])
        edit_two = choice(edits, p=probabilities[1])

    return ' '.join([edit_one, edit_two])


def drive_oracle(current_iteration, folder_root, edit_string):
    cwd = os.getcwd() + '/'
    n_prog_path = cwd + 'n_prog_code/'
    tar_path = n_prog_path + 'look-example.tar.gz'
    repair_path = n_prog_path + 'repair'
    output_path = folder_root + str(current_iteration) + '/look-example/'
    results_path = folder_root + 'results/'

    # make a directory for n-prog and GenProg to use
    call('mkdir -p ' + output_path, shell=True)
    call('mkdir -p ' + results_path, shell=True)

    # copy the relevant files over
    call('tar -xf ' + tar_path + ' -C ' + output_path, shell=True)

    # move things down a directory for simpler paths
    # call('mv ' + output_path + 'look-example/* ' + output_path, shell=True)
    # call('rm -r ' + output_path + 'look-example', shell=True)

    # call GenProg
    call('echo "\n--oracle-genome ' + edit_string +
         '" >> ' + output_path + 'configuration-default', shell=True)
    call('cd ' + n_prog_path + ' && ./repair --program ' + output_path +
         'look.c --search "pd-oracle" --oracle-genome "' +
         edit_string + '" > ' + results_path + str(current_iteration), shell=True)


def parse_oracle_output(location):

    return False

# commented out to avoid regeneration each time
# make_neutral_edits(temp_folder='/home/joe/experiments/506/neutral_edits/',
#                    neutral_edits=100)
neutral_edits = get_neutral_edits('/home/joe/experiments/506/neutral_edits/',
                                  neutral_edits=100)

# stand-in for weight matrix during early tests
p = [[0.01 for i in range(100)] for j in range(2)]

for i in range(10):
    edit_string = generate_edit_string(edits=neutral_edits, probabilities=p)
    print(edit_string)
    drive_oracle(current_iteration=i, folder_root='/home/joe/experiments/506/',
                 edit_string=edit_string)
