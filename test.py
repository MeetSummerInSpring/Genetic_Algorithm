from bisect import bisect
import copy
import numpy as np
import math
import matplotlib.pyplot as plt
a1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
a2 = copy.copy(a1)
a1[1] = 10

print(a1)
print(a2)


def func(x):
    return 10 * np.exp(-x) * np.sin(x)

# b = np.array([6, 3, 4, 1, 9])
# order = np.argsort(b)
# b = b[order]
# print(b)
# print(bisect(b, 1.1))
# print(b)


# for i in range(5):
#     print(sum(a[:i+1]))

plt.rcParams['font.sans-serif'] = ['SimHei']    # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False      # 正常显示负号
plt.figure(figsize=(11, 5),dpi=100)

# plt.plot()

plt.title("func", fontsize=18, loc="center")
plt.xlabel("x轴", fontsize=12, loc="center")
plt.ylabel("y轴", fontsize=12, loc="center")

X = np.arange(0, 10, 0.1)
plt.plot(X, func(X), color="red", label="func", linestyle="--")
# plt.plot(X, test_loss_list, color="blue", label="test_loss", linestyle=":")
# plt.xticks(range(0, epoch+1, 5), rotation=90, fontsize=12)
plt.legend()

plt.show()