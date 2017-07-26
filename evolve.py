import os
import random
import shlex
import subprocess
import sys

inputs = ["R", "P", "S"]
bits = ["0", "1"]

number_of_generations = 10

number_per_generation = 100

current_generation = []

# 10%
breed_percent = 100

# 50%
crossover_chance = 500

# 0.1%
mutation_chance = 1

# initialisation

base_folder_name = 'bots'
os.mkdir(base_folder_name)

'''
get a random index between 0 and <total> that 
is not in the array <chosen>
'''
def get_index(total, chosen):
    choice = 0
    while choice in chosen:
        choice = random.randrange(total)
    return choice

# initial genomes

for i in range(0, number_per_generation):
    genome = ''
    for j in range(0, 25):
        for k in range(0, 3):
            genome += random.choice(bits)
        genome += random.choice(inputs)
    current_generation.append({
        'genome':genome,
        'score':0
    })

# complete process for a number of generations

for generation_number in range(0, number_of_generations):

    # create a folder to store the state machines in

    folder_name = os.path.join(base_folder_name, '{0:03}'.format(generation_number))
    os.mkdir(folder_name)

    # load the state machine code

    source = open('fsm.py', 'r')
    source_data = source.read()
    source.close()

    # for each genome create a state machine file that can be run by the runner

    for i in range(0, number_per_generation):
        dest_filename = os.path.join(folder_name, '{0:03}.py'.format(i))
        dest_data = source_data.replace('xxxGENOMExxx', current_generation[i]['genome'])
        dest = open(dest_filename, 'w')
        dest.write(dest_data)
        dest.close()

    # launch rpsrunner with parameters to run all the state machines

    gen_path = os.path.join(folder_name, '*.py')
    command = '/usr/bin/python2 rpsrunner.py -m 1 \"{0}\"'.format(gen_path)
    print command

    # split the output and try to find results for each state machine

    result = subprocess.check_output(shlex.split(command))
    lines = result.decode('ascii').split('\n')
    for i in range(0, len(lines)):
        if lines[i].startswith(folder_name):
            index = int(lines[i].split(' ')[0][9:12])
            score = int(lines[i+1].split(' ')[8][1:])
#            print index, score
            current_generation[index]['score'] = score

    # sort and select best scores

    current_generation = sorted(current_generation, key=lambda gen: gen['score'], reverse=True)

    #for genome in current_generation:
    #    print genome

    print 'top score', current_generation[0]
    #for i in range(0, number_per_generation):
    #    print i, current_generation[i]['score']

    number_to_breed = (number_per_generation * breed_percent) / 1000
    print 'breed', number_to_breed

    # breed the top x percent randonly until we have enough new genomes

    new_generation = []
    while len(new_generation) < number_per_generation:
        index_a = get_index(number_to_breed, [])
        index_b = get_index(number_to_breed, [index_a])
        #print index_a, index_b
        
        # do crossover and mutation
        new_genome = ''
        genome_a = current_generation[index_a]
        genome_b = current_generation[index_b]
        for i in range(0, len(genome_a['genome'])):

            # do crossover

            if random.randrange(1000) < crossover_chance:
                new_gene = genome_a['genome'][i]
            else:
                new_gene = genome_b['genome'][i]

            # do mutation

            if random.randrange(1000) < mutation_chance:
                if new_gene in ['0', '1']:
                    # mutate 0/1
                    if new_gene == '0':
                        new_gene = '1'
                    else:
                        new_gene = '0'
                else:
                    # mutate R/P/S
                    index = get_index(3, [inputs.index(new_gene)])
                    new_gene = inputs[index]
            new_genome += new_gene

        # add the new genome to the new generation

        new_generation.append({
            'genome':new_genome,
            'score':0
        })

    current_generation = new_generation

