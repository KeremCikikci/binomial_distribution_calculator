from scipy.stats import binom
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox
from math import ceil, floor

# GIVEN
n = int(input('n = ')) # Versuchanzahl
p = float(input('p = ')) # Treffer WK
p = round(p, 4)

a = input("k = ")

if ';' in a:
    k = None
    _min, _max = a.split(';')
    _min, _max = int(_min), int(_max)

else:
    k = int(a) # Zufallsvariable
    _min = None
    _max = None


# CALCULATIONS

def cal(n, p, k, _min, _max):
    poss = None
    interval = None
    mean = round(binom.mean(n, p, loc=0), 4)
    std = round(binom.std(n, p, loc=0), 4)

    if _min == None and _max == None:
        mean = binom.mean(n, p, loc=0)
        poss = binom.pmf(k, n, p)

    else:
        k = None

        if _min == None: _min = 0
        if _max == None: _max = n

        poss_min = binom.cdf(_min, n, p)
        poss_max = binom.cdf(_max, n, p)

        poss = poss_max - poss_min
    
    interval = [ceil(mean-std), floor(mean+std)]

    poss = round(poss, 4)

    return poss, mean, std, interval

poss, mean, std, interval = cal(n, p, k, _min, _max)

# UI
fig, ax = plt.subplots()

fig.subplots_adjust(bottom=0.3)

plt.title("Binomialverteilung", fontsize=16)
plt.xlabel('Merkmalswert')
plt.ylabel('Häufigkeitsdichte')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

x = np.arange(0, n)
ax.plot(x, binom.pmf(x, n, p), 'bo', ms=8)
ax.vlines(x, 0, binom.pmf(x, n, p), colors='b', lw=7, alpha=0.5)

rv = binom(n, p)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1)

plt.vlines(x=interval[0], ymin=0, ymax= binom.pmf(int(mean), n, p), colors='r', linestyles='dashed')
plt.vlines(x=interval[1], ymin=0, ymax= binom.pmf(int(mean), n, p), colors='r', linestyles='dashed')

info_ax = plt.axes([0.1, 0.12, 0, 0])

if _min == None and _max == None:
    TextBox(info_ax, '', initial=f"P(X={k}) = {poss}    n = {n}    p = {p}    µ = {mean}    σ = {std}    J = {interval}")
else:
    if _min != None and _max == None:
        TextBox(info_ax, '', initial=f"P(X > {_min}) = {poss}    n = {n}    p = {p}    µ = {mean}    σ = {std}    J = {interval}")
    if _min == None and _max != None:
        TextBox(info_ax, '', initial=f"P({_max} > X) = {poss}    n = {n}    p = {p}    µ = {mean}    σ = {std}    J = {interval}")
    if _min != None and _max != None:
        TextBox(info_ax, '', initial=f"P({_max} > X > {_min}) = {poss}    n = {n}    p = {p}    µ = {mean}    σ = {std}    J = {interval}")

plt.show()