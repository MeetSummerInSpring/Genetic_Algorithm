from function import *
import matplotlib.pyplot as plt
from tqdm import tqdm, trange

calculate_limit = 100  # 迭代次数

population_size = 50  # 种群数量
chrom_length = 10  # 染色体长度

elimination_rate = 0.4  # 多少比例后的个体可能被淘汰
elimination_prob = 0.5  # 比例内个体被淘汰的概率

mating_rate = 0.4  # 交配概率
exchange_rate = 0.2  # 基因交换概率

mutation_rate = 0.1  # 变异概率

# 通过 min max 控制函数定义域
gene_min = 0  # 基因最小值
gene_max = 10  # 基因最大值


# 真实函数
def func(x):
    # return 10 * np.sin(5 * x) + 7 * np.cos(4 * x)
    return 20 * np.exp(-x) * np.sin(x)


# 初始化
func_name = "10sin(5x)+7cos(4x)"

X = []
best_X = []
best_Y = []
avg_Y = []
population_chroms = np.array(chroms_encoding(population_size, chrom_length))

for i in trange(calculate_limit):
    # 评估适应度 TODO:加入上下限控制 OK
    population_chroms_ture, population_values = \
        evaluate(population_chroms, func, chrom_length, gene_min, gene_max)

    if i != 0:
        X.append(i)
        best_X.append(population_chroms_ture[np.argmax(population_values)])
        best_Y.append(max(population_values))
        avg_Y.append(sum(population_values) / len(population_values))

    # 自然选择：精英淘汰+优等复制
    population_chroms = select(population_chroms, population_values,
                               population_size)
    # 交配
    population_chroms = crossover_mating(population_chroms, chrom_length,
                                         mating_rate, exchange_rate)
    # 变异
    population_chroms = mutation(population_chroms, chrom_length, mutation_rate)

# 画图
name = "6"

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
plt.figure(figsize=(11, 5), dpi=100)

plt.subplot(1, 2, 1)

plt.title("y=" + func_name, fontsize=18, loc="center")
plt.xlabel("x-axis", fontsize=12, loc="center")
plt.ylabel("y-axis", fontsize=12, loc="center")

func_X = np.arange(0, 10, 0.1)
func_Y = func(func_X)
plt.plot(func_X, func_Y, color="red", label="func", linestyle="--")
plt.legend()

plt.subplot(1, 2, 2)

plt.title("population_results", fontsize=18, loc="center")
plt.xlabel("iter_times", fontsize=12, loc="center")
plt.ylabel("y-axis", fontsize=12, loc="center")

plt.plot(X, best_X, color="red", label="best_x", linestyle="--")
plt.plot(X, best_Y, color="blue", label="best_y", linestyle=":")
plt.plot(X, avg_Y, color="yellow", label="avg_y", linestyle="-.")
plt.legend()

plt.savefig("result\\" + name + ".png")
print("best_function_result:", max(func_Y))
print("best_population_result:", max(best_Y))
plt.show()
