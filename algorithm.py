import random
from dataset import init_dataset


def calculate_fitness(individual, usage_1, usage_2):
    fitness = 0
    curve = 0
    for lang in individual:
        print(lang)
        fitness += lang[usage_1] + lang[usage_2]
        curve += lang[11]

    return fitness / 6


def generate_initial_population(initial_population, dataset, usage_1, usage_2):
    population = []
    for _ in range(initial_population):
        individual = random.sample(dataset, 3)
        fitness = calculate_fitness(individual, usage_1, usage_2)
        population.append((individual, fitness))
    return population


def get_eligible(population, probability):
    eligible = []
    for i in range(population.__len__()):
        if random.random() <= probability:
            eligible.append(population[i])
    return eligible


def select_couple(population, crossover_probability):
    eligible_individuals = get_eligible(population, crossover_probability)
    pairs = []

    for individual in eligible_individuals:
        random_index = random.randint(0, len(eligible_individuals) - 1)
        pairs.append((eligible_individuals[random_index], individual))

    return pairs


def crossover(individual1, individual2):
    crossover_point = 1

    individual1 = individual1[0]
    individual2 = individual2[0]

    print("individual1" + str(individual1) + "\n")
    print("individual2" + str(individual2) + "\n")

    child1 = []
    child2 = []

    child1.extend(individual1[:crossover_point])
    child1.extend(individual2[crossover_point:])

    child2.extend(individual2[:crossover_point])
    child2.extend(individual1[crossover_point:])

    print("child1" + str(child1) + "\n")
    print("child2" + str(child2) + "\n")

    return (child1, child2)


def crossover_pairs(pairs):
    new_individuals = []

    for pair in pairs:
        child1, child2 = crossover(pair[0], pair[1])
        new_individuals.append(child1)
        new_individuals.append(child2)
    return new_individuals


def mutate_gen(child, gen_mutation_probability, dataset):
    for i in range(len(child)):
        random_flag = random.random()
        if random_flag <= gen_mutation_probability:
            while True:
                new_gen = random.choice(dataset)
                if new_gen not in child:
                    child[i] = new_gen
                    break
    return child


def mutate_children(children, individual_mutation_probability, gen_mutation_probability, dataset):
    for i in range(len(children)):
        if random.random() <= individual_mutation_probability:
            mutated_child = mutate_gen(children[i], gen_mutation_probability, dataset)
            children[i] = mutated_child
    return children


def get_statistics(population, minimize):
    best_individual = population[0]
    worst_individual = population[0]
    sum = 0

    for individual in population:
        if minimize:
            if individual[1] < best_individual[1]:
                best_individual = individual
            if individual[1] > worst_individual[1]:
                worst_individual = individual
        else:
            if individual[1] > best_individual[1]:
                best_individual = individual
            if individual[1] < worst_individual[1]:
                worst_individual = individual

        sum += individual[1]

    return {"best": best_individual, "worst": worst_individual, "average": sum / len(population)}


def prune_population(population, max_population, minimize):
    if len(population) > max_population:
        sorted_population = sorted(population, key=lambda x: x[1], reverse=not minimize)
        pruned_population = sorted_population[:max_population]
    else:
        pruned_population = population

    return pruned_population


def genetic_algorithm(usage_1, usage_2, generations, initial_population, max_population,
                      crossover_probability, individual_mutation_probability, gen_mutation_probability, minimize):

    statistics_history = []
    dataset = init_dataset()

    usages = ["artificial_intelligence", "machine_learning", "data_science", "web_dev", "enterprise_dev", "mobile_dev", "game_dev", "embedded_system", "virtual_reality"]

    population = generate_initial_population(initial_population, dataset, usage_1, usage_2)
    print(population)

    statistics = get_statistics(population, minimize)
    statistics_history.append(statistics)

    for _ in range(generations):
        pairs = select_couple(population, crossover_probability)
        print("pairs" + "\n")
        for pair in pairs:
            print(str(pair) + "\n")

        children = crossover_pairs(pairs)
        print("children" + str(children) + "\n")

        mutated_children = mutate_children(children, individual_mutation_probability, gen_mutation_probability, dataset)
        print("mutated_children" + str(mutated_children) + "\n")

        new_individuals = []
        for individual in mutated_children:
            fitness = calculate_fitness(individual, usage_1, usage_2)
            new_individual = (individual, fitness)

            new_individuals.append(new_individual)
            print("fin")

        new_individuals.extend(population)

        statistics = get_statistics(new_individuals, minimize)
        statistics_history.append(statistics)
        population = prune_population(new_individuals, max_population, minimize)
    print(population)

    return statistics_history, population
