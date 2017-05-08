from subprocess import call
import random
import os


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

    make_neutral_edits(temp_folder=temp_folder, neutral_edits=neutral_edits)

    # open the genomes file
    with open(temp_folder + '/repair.debug/repair.debug.original', 'r') as in_file:
        lines = in_file.readlines()
        for line in lines:
            if line.find('is neutral') != -1:
                generated_neutral_edits
    # parse it for neutral edits

    # select 100 of them at random and return that list

    return generated_neutral_edits

get_neutral_edits('/home/joe/experiments/506/neutral_edits', neutral_edits=100)
