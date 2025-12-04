import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

try:
    df = pd.read_csv('results/results_v2.csv')
except FileNotFoundError:
    print("Arquivo CSV não encontrado!")
    exit()


plt.figure(figsize=(14, 7))

chart = sns.boxplot(
    data=df,
    x="proto", 
    y="ms", 
    hue="scenario",
    palette="viridis",
    showfliers=False
)


g = sns.catplot(
    data=df, 
    kind="bar", 
    x="scenario", 
    y="ms", 
    hue="proto", 
    col="lang",
    palette="magma",
    height=5, 
    aspect=1,
    capsize=.1,
    errorbar="sd"
)

g.fig.subplots_adjust(top=0.85)
g.fig.suptitle('RQ 01: Tempo de Resposta Médio (ms) - Menor é Melhor')
g.set_axis_labels("Cenário", "Tempo (ms)")

plt.savefig('rq01_time_comparison.png')
print("Gráfico RQ 01 gerado: rq01_time_comparison.png")



g2 = sns.catplot(
    data=df, 
    kind="bar", 
    x="scenario", 
    y="bytes", 
    hue="proto", 
    col="lang",
    palette="viridis",
    height=5, 
    aspect=1
)

g2.fig.subplots_adjust(top=0.85)
g2.fig.suptitle('RQ 02: Tamanho da Resposta (Bytes) - Menor é Melhor')
g2.set_axis_labels("Cenário", "Tamanho (Bytes)")

plt.savefig('rq02_size_comparison.png')
print("Gráfico RQ 02 gerado: rq02_size_comparison.png")

plt.show()