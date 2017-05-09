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


def get_neutral_edits(temp_folder, number_to_get):
    generated_neutral_edits = []

    # open the debug file
    with open(temp_folder + '/repair.debug/repair.debug.original', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # parse it for neutral edits
            if line.find('is neutral') != -1:
                generated_neutral_edits.append(line[line.find('+') + 1:line.find('is neutral')].strip())

    # select a number of them at random and return that list
    generated_neutral_edits = random.sample(generated_neutral_edits, number_to_get)

    return generated_neutral_edits


def get_indices(indices, probabilities):
    # index_a = 0
    # index_b = 0
    # while index_a == index_b:
    index_a = choice(indices, p=probabilities[0])
    index_b = choice(indices, p=probabilities[1])

    return index_a, index_b


def generate_edit_string(index_a, index_b, edits):
    edit_one = edits[index_a]
    edit_two = edits[index_b]
    return ' '.join([edit_one, edit_two])


def drive_oracle(current_iteration, folder_root, edit_string):
    cwd = os.getcwd() + '/'
    n_prog_path = cwd + 'n_prog_code/'
    tar_path = n_prog_path + 'look-example.tar.gz'
    untar_path = folder_root + str(current_iteration) + '/'
    output_path = folder_root + str(current_iteration) + '/look-example/'
    results_path = folder_root + 'results/'

    # make a directory for n-prog and GenProg to use
    call('mkdir -p ' + output_path, shell=True)
    call('mkdir -p ' + results_path, shell=True)

    # copy the relevant files over
    call('tar -xf ' + tar_path + ' -C ' + untar_path, shell=True)

     # call GenProg
    call('cd ' + output_path + ' && ./repair --program ' + output_path +
         'look.c --search pd-oracle --oracle-genome "' + edit_string +
         '" --sanity no --fix-scheme uniform --fault-scheme uniform --pos-tests'
         ' 14 --neg-tests 1 > ' + results_path + str(current_iteration),
         shell=True)


def parse_oracle_output(location):
    score = -1
    with open(location, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.find('was neutral') != -1:
                score = int(line[line.find('passed ') +
                                 7:line.find(' negative')])
    return score


def run_experiment(number_of_edits, root_dir, exp_prefix):
    neutral_edits_dir = root_dir + exp_prefix + 'neutral_edits/'
    experiment_base = root_dir + exp_prefix
    results_dir = experiment_base + 'results/'
    weight_dump_path = results_dir + 'weight_dump'

    make_neutral_edits(temp_folder=neutral_edits_dir,
                       neutral_edits=number_of_edits)
    neutral_edits = get_neutral_edits(neutral_edits_dir,
                                      number_to_get=number_of_edits)

    indices = [x for x in range(number_of_edits)]

    # stand-in for weight matrix during early tests
    p = [[float(1/number_of_edits) for _ in range(number_of_edits)] for j in range(2)]
    weights = [[float(1/number_of_edits) for k in range(number_of_edits)] for l in range(2)]

    eta = 0.5

    memoized = {}
    i = 0
    converged = False
    while not converged:
        print(i)
        index_a, index_b = get_indices(indices=indices, probabilities=p)
        edit_string = generate_edit_string(edits=neutral_edits,
                                           index_a=index_a,
                                           index_b=index_b)
        print(edit_string)
        if edit_string not in memoized:
            drive_oracle(current_iteration=i,
                         folder_root=experiment_base,
                         edit_string=edit_string)
            memoized[edit_string] = parse_oracle_output(results_dir + str(i))
        # look up entry and update weight table
        weights[0][index_a] *= (1 + eta*memoized[edit_string])
        weights[1][index_b] *= (1 + eta*memoized[edit_string])
        # update probability matrix
        weight_sum_zero = sum(weights[0])
        weight_sum_one = sum(weights[1])

        zero_converged = False
        one_converged = False
        for update_index in range(number_of_edits):
            p[0][update_index] = weights[0][update_index] / weight_sum_zero
            p[1][update_index] = weights[1][update_index] / weight_sum_one
            if p[0][update_index] == 1.0:
                zero_converged = True
            if p[1][update_index] == 1.0:
                one_converged = True

        # print every nth result where n = num_edits
        if i % number_of_edits == 0:
            with open(weight_dump_path, 'a') as f:
                f.write(str(p) + '\n')

        # if we have reached convergence, print the final matrix and stop
        if zero_converged and one_converged:
            converged = True
            with open(weight_dump_path, 'a') as f:
                f.write('the algorithm converged at ' + str(i) + '\n')
                f.write(str(p) + '\n')

        i += 1


# ran this already
# run_experiment(number_of_edits=300, root_dir='/home/joe/experiments/506/',
#                exp_prefix='300/')

# running 12:47 tuesday
# run_experiment(number_of_edits=50, root_dir='/home/joe/experiments/506/',
#                exp_prefix='50_full_random/')
#
#
# run_experiment(number_of_edits=100, root_dir='/home/joe/experiments/506/',
#                exp_prefix='100_full_random/')
#
# run_experiment(number_of_edits=200, root_dir='/home/joe/experiments/506/',
#                exp_prefix='200_full_random/')
#
# run_experiment(number_of_edits=400, root_dir='/home/joe/experiments/506/',
#                exp_prefix='400_full_random/')

# started run at 15:15 tuesday
run_experiment(number_of_edits=800, root_dir='/home/joe/experiments/506/',
               exp_prefix='800_full_random/')


