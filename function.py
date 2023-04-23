import numpy as np
import random
import math
from bisect import bisect


# 初始化：二进制编码基因
def chroms_encoding(population_size, chrom_length):
    pop_chroms = []

    for i in range(population_size):
        chrom = []
        for j in range(chrom_length):
            chrom.append(random.randint(0, 1))
        pop_chroms.append(chrom)

    return pop_chroms


# 单个基因的解码
def gene_decoding(chrom):
    chrom_unnor = 0

    for i in range(len(chrom)):
        chrom_unnor += chrom[i] * math.pow(2, i)

    return chrom_unnor


# 将基因归一化后计算种群的适应度  TODO:筛选 max min OK
def evaluate(pop_chroms, func, chrom_length, gene_min=0, gene_max=10):
    population_values = []
    pop_chroms_ture = []

    # zero_point = (gene_min + gene_max) / 2
    scale = gene_max - gene_min

    for chrom in pop_chroms:
        # 十进制数
        chrom_unnor = gene_decoding(chrom)
        # 对x做归一变化 规范定义域 TODO:范围以外是否舍去 OK
        chrom_true = scale / (math.pow(2, chrom_length) - 1) * (chrom_unnor - 0) + gene_min

        # # 对范围外的做裁剪 这种映射方法不会进
        # if chrom_true > gene_max or chrom_true < gene_min:
        #     population_values.append(0)
        #     print("Population")
        # else:
        #     population_values.append(func(chrom_true))

        pop_chroms_ture.append(chrom_true)
        population_values.append(func(chrom_true))

    return pop_chroms_ture, population_values


# 繁衍 适应度越高 后代数量多的概率更大 轮盘赌筛选
def select(pop_chroms, population_values, elimination_rate, elimination_prob):
    # # 淘汰
    # # TODO: population_values 应该都为正数 OK
    # pop_chroms_ = []
    # population_values_ = []
    # value_max = max(population_values)
    # value_min = min(population_values)
    # value_eli = (value_max - value_min) * elimination_rate + value_min
    #
    # for i in range(len(pop_chroms)):
    #     # 淘汰线以下且命中便淘汰
    #     if population_values[i] < value_eli and random.random() < elimination_prob:
    #         continue
    #     else:
    #         pop_chroms_.append(pop_chroms[i])
    #         population_values_.append(population_values[i])
    #
    # pop_chroms = pop_chroms_
    # population_values = population_values_

    # 根据个体适应度计算个体繁衍概率 TODO:有负值
    value_sum = sum(population_values)
    population_probs = []
    for value in population_values:
        population_probs.append(value / value_sum)

    # 排序 不加np不能直接索引转数组
    order = np.argsort(population_probs)
    population_probs = np.array(population_probs)[order]
    pop_chroms = np.array(pop_chroms)[order]

    # 计算累加概率 方便计算轮盘赌
    population_sum_probs = []
    probs_sum = 0
    for i in range(len(population_probs)):
        probs_sum += population_probs[i]
        population_sum_probs.append(probs_sum)

    # 轮盘赌加入新个体 成为新种群
    new_pop_chroms = []
    for i in range(len(pop_chroms)):
        rand_prob = random.random()
        # prob_k < prob < prob_{k+1}
        chrom_selected = bisect(population_sum_probs, rand_prob)
        new_pop_chroms.append(pop_chroms[chrom_selected])

    return new_pop_chroms


# 交配
def crossover_mating(pop_chroms, chrom_length, mating_rate, exchange_rate):
    """

    :param pop_chroms: 种群基因
    :param exchange_rate: 染色体互换的概率
    :param mating_rate: 交配的概率
    :return:
    """
    # for的时候len不会变，但内部会变
    population_len = len(pop_chroms)

    for i in range(population_len):
        mating_prob = random.random()

        # 第i个体交配
        if mating_prob > mating_rate:
            child1 = pop_chroms[i]  # female
            child2 = pop_chroms[random.randint(0, population_len - 1)]  # male

            # 两个子代的基因交换
            for j in range(chrom_length):
                exchange_prob = random.random()

                # 第j处基因交换
                if exchange_prob > exchange_rate:
                    child1[j], child2[j] = child2[j], child1[j]

            pop_chroms.append(child1)
            pop_chroms.append(child2)

        else:
            continue

    return pop_chroms


# 变异
def mutation(pop_chroms, chrom_length, mutation_rate):
    """

    :param pop_chroms:
    :param mutation_rate: 每条染色体的变异概率
    :return:
    """
    # 用item不能给list赋值
    for i in range(len(pop_chroms)):
        for j in range(chrom_length):
            mutation_prob = random.random()
            if mutation_prob > mutation_rate:
                if pop_chroms[i][j] == 1:
                    pop_chroms[i][j] = 0
                else:
                    pop_chroms[i][j] = 1

    return pop_chroms
