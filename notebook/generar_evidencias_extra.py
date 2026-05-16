import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules
import os

sns.set_theme(style="whitegrid")

# Función para guardar un dataframe como imagen
def render_mpl_table(data, filename, col_width=3.0, row_height=0.625, font_size=10,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0, ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors) ])
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

print("Generando foto de Reglas de Asociación...")
# 6.1 Asociación
df_asoc = pd.read_csv('../data/clave_C_asociacion.csv').dropna().drop_duplicates()
basket = (df_asoc.groupby(['transaccion_id', 'item'])['cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('transaccion_id'))

def encode_units(x):
    if x <= 0: return 0
    if x >= 1: return 1

basket_sets = basket.map(encode_units) if hasattr(basket, 'map') else basket.applymap(encode_units)
frequent_itemsets = apriori(basket_sets, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
rules = rules.sort_values('confidence', ascending=False)
top_10 = rules.head(10).copy()
top_10['antecedents'] = top_10['antecedents'].apply(lambda x: ', '.join(list(x)))
top_10['consequents'] = top_10['consequents'].apply(lambda x: ', '.join(list(x)))
top_10 = top_10[['antecedents', 'consequents', 'support', 'confidence', 'lift']].round(3)

render_mpl_table(top_10, '../evidencia/6_1_top_10_reglas_asociacion.png', col_width=2.5)

print("Generando foto del Método del Codo...")
# 6.3 Método del codo
df_agrup = pd.read_csv('../data/clave_C_agrupacion.csv').dropna().drop_duplicates()
df_num_agrup = df_agrup.select_dtypes(include=[np.number])
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_num_agrup)

inercia = []
rango_k = range(1, 10)
for k in rango_k:
    kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans_temp.fit(df_scaled)
    inercia.append(kmeans_temp.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(rango_k, inercia, marker='o', linestyle='--')
plt.title('Método del Codo para K-Means')
plt.xlabel('Número de Clusters (K)')
plt.ylabel('Inercia')
plt.savefig('../evidencia/6_3_metodo_codo.png', bbox_inches='tight')
plt.close()

print("Generando foto de los Centroides (K-Means)...")
# 6.3 Centroides
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(df_scaled)
centroides = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=df_num_agrup.columns).round(2)
centroides.insert(0, 'Cluster', ['Cluster 0', 'Cluster 1', 'Cluster 2'])

render_mpl_table(centroides, '../evidencia/6_3_centroides_kmeans.png', col_width=1.5)

print("¡Todas las fotos generadas exitosamente en la carpeta evidencia!")
