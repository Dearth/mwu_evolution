import matplotlib.pyplot as plt
import matplotlib as mpl


def get_running_totals(length, filename):

    with open(filename, 'r') as in_file:
        lines = in_file.readlines()
        timesteps = len(lines)-1
        running_total_first = [[] for _ in range(timesteps)]
        running_total_second = [[] for _ in range(timesteps)]
        first_probs = []
        second_probs = []
        for index in range(timesteps):
            first_probs.append(lines[index].strip('[]').split(', ')[:length])
            second_probs.append(lines[index].strip('[]').split(', ')[length:])

            for i in range(length):

                first_probs[index][i] = float(first_probs[index][i].strip('[]'))
                second_probs[index][i] = float(second_probs[index][i].strip('[]\n'))
                if i == 0:
                    running_total_first[index].append(first_probs[index][i])
                    running_total_second[index].append(second_probs[index][i])
                else:
                    running_total_first[index].append(running_total_first[index][i-1] + first_probs[index][i])
                    running_total_second[index].append(running_total_second[index][i-1] + second_probs[index][i])
            print('second running total is: ', len(running_total_second))
    return running_total_first, running_total_second, timesteps


def make_plot(running_total_first, running_total_second, current_iteration, file_length):
    for x in ['edit_1', 'edit_2']:
        if x == 'edit_1':
            list_to_viz = running_total_first
        else:
            list_to_viz = running_total_second

        fig = plt.figure(figsize=(8, 1.25))
        ax1 = fig.add_axes([0.1, 0.2, 0.8, 0.7])

        mini_list = ['r', 'g', 'b', 'c', 'm', 'y']
        color_array = [mini_list[i % len(mini_list)] for i in range(len(list_to_viz))]
        cmap = mpl.colors.ListedColormap(color_array)

        bounds = list_to_viz
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                       norm=norm,
                                       spacing='proportional',
                                       orientation='horizontal')

        plt.savefig(filename=(str(file_length) + '_' + x + '_' +
                              str(current_iteration*len(list_to_viz))))

        plt.clf()


for length in [50, 100, 200, 400]:
    filename = ('/home/joe/experiments/506/' + str(length) +
                '_full_random/results/weight_dump')
    a, b, parsed_lines = get_running_totals(length=length, filename=filename)
    for i in range(parsed_lines):
        make_plot(running_total_first=a[i],
                  running_total_second=b[i],
                  current_iteration=i,
                  file_length=length)
