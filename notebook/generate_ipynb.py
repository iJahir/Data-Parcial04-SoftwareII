import nbformat as nbf

nb = nbf.v4.new_notebook()

text_intro = """# Proyecto Final: Análisis de Datos (Parcial 4)
**Asignatura:** Inteligencia de Negocios  
**Fecha:** 16-05-2026

En este notebook se desarrollarán tres ejercicios prácticos exigidos por la rúbrica del docente:
1. **Análisis de Asociación:** Uso del algoritmo Apriori para identificar patrones de compra.
2. **Análisis de Correlación:** Matrices y mapas de calor para hallar relaciones entre variables numéricas.
3. **Agrupación o Clustering:** Uso de K-Means y Método del Codo para segmentación de clientes."""

code_imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
import warnings
warnings.filterwarnings('ignore')"""

# Ejercicio 1
text_ej1 = """## Ejercicio 1: Análisis de Asociación (25%)
**Objetivo:** Descubrir patrones de compra conjuntos utilizando el dataset de transacciones.
### 1. Carga y Exploración de Datos"""

code_ej1_1 = """# Cargar el archivo CSV
df_asoc = pd.read_csv('../data/clave_C_asociacion.csv')

# Mostrar las primeras filas y estructura
print("--- Primeras Filas ---")
display(df_asoc.head())
print("\\n--- Estructura del Dataset ---")
df_asoc.info()"""

text_ej1_2 = """### 2. Limpieza de Datos (Nulos y Duplicados)
Verificamos si existen datos faltantes o repetidos que puedan alterar el algoritmo."""

code_ej1_2 = """print("Valores nulos:\\n", df_asoc.isnull().sum())
print("\\nCantidad de duplicados:", df_asoc.duplicated().sum())

# Eliminamos valores nulos y duplicados
df_asoc = df_asoc.dropna()
df_asoc = df_asoc.drop_duplicates()
print("Datos limpios. Total de registros:", len(df_asoc))"""

text_ej1_3 = """### 3. Preparación de Datos para Apriori
El algoritmo Apriori de `mlxtend` requiere que los datos estén en un formato tabular de variables binarias (One-Hot Encoding), donde las filas son transacciones y las columnas son los items comprados."""

code_ej1_3 = """from mlxtend.frequent_patterns import apriori, association_rules

# Agrupamos por transaccion_id e item, sumando la cantidad
basket = (df_asoc.groupby(['transaccion_id', 'item'])['cantidad']
          .sum().unstack().reset_index().fillna(0)
          .set_index('transaccion_id'))

# Convertimos a formato binario (1 si se compró, 0 si no)
def encode_units(x):
    if x <= 0: return 0
    if x >= 1: return 1

basket_sets = basket.applymap(encode_units)
display(basket_sets.head())"""

text_ej1_4 = """### 4. Aplicación de Apriori y Generación de Reglas
Extraemos los ítems frecuentes (soporte > 0.05) y generamos reglas de asociación basadas en el 'lift'."""

code_ej1_4 = """# Items frecuentes
frequent_itemsets = apriori(basket_sets, min_support=0.05, use_colnames=True)

# Reglas de asociación
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
rules = rules.sort_values('confidence', ascending=False)

# Mostrar las 10 reglas más relevantes
print("Top 10 Reglas de Asociación:")
display(rules.head(10))"""

text_ej1_5 = """### Interpretación y Conclusiones (Negocio)
**Interpretación de Reglas:**
1. Los clientes que compran el ítem X tienen una alta probabilidad (confianza del Y%) de comprar también el ítem Z.
2. El *lift* mayor a 1 en las primeras reglas indica que los productos se compran juntos con mucha más frecuencia que si fueran compras independientes.
3. *[Nota: Ajustar esta interpretación al ver la salida real del dataset en la ejecución]*

**Recomendaciones Comerciales:**
1. **Venta Cruzada (Cross-Selling):** Crear un "bundle" o combo con los productos de mayor confianza para aumentar el ticket promedio.
2. **Promociones Dirigidas:** Ofrecer un descuento en el producto B al agregar el producto A al carrito.
3. **Distribución en Tienda/Web:** Colocar físicamente o en sugerencias web ("Los clientes también compraron...") los productos que forman las reglas más fuertes."""


# Ejercicio 2
text_ej2 = """## Ejercicio 2: Análisis de Correlación (20%)
**Objetivo:** Encontrar relaciones matemáticas entre variables numéricas para entender el comportamiento de los clientes."""

code_ej2_1 = """# Cargar y limpiar el archivo
df_corr = pd.read_csv('../data/clave_C_correlacion.csv')
df_corr = df_corr.dropna().drop_duplicates()

# Seleccionar solo variables numéricas
df_num_corr = df_corr.select_dtypes(include=[np.number])

print("Estadísticas Descriptivas:")
display(df_num_corr.describe())"""

text_ej2_2 = """### Matriz de Correlación y Mapa de Calor
Calculamos el coeficiente de correlación de Pearson y lo visualizamos con Seaborn."""

code_ej2_2 = """matriz_correlacion = df_num_corr.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Mapa de Calor - Correlación de Variables")
plt.tight_layout()
plt.savefig('../evidencia/mapa_calor_correlacion.png')
plt.show()"""

text_ej2_3 = """### Interpretación de Relaciones (Negocio)
Basado en el mapa de calor:
1. **Relación Positiva Fuerte (Ej. Ingresos vs Consumo Total):** Si observamos un valor cercano a 1, significa que los clientes con mayores ingresos tienden a consumir más.
2. **Relación Negativa (Ej. Reclamos vs Satisfacción):** Un valor negativo (ej. -0.6) indica claramente que a mayor número de reclamos, la satisfacción del cliente cae drásticamente.
3. **Tiempo de respuesta vs Satisfacción:** Si la correlación es negativa, indica que la lentitud en atender reduce la satisfacción.
4. **Edad vs Uso de la App:** Evaluar si hay relación entre la demografía y el canal digital.

**Conclusión Comercial:**
Al identificar qué factores disminuyen la satisfacción (como el tiempo de respuesta), la empresa puede reasignar recursos a atención al cliente. Además, las correlaciones positivas permiten enfocar campañas de fidelización en los segmentos más rentables."""


# Ejercicio 3
text_ej3 = """## Ejercicio 3: Agrupación o Clustering (25%)
**Objetivo:** Segmentar clientes en grupos con características similares para personalizar la atención y estrategias."""

code_ej3_1 = """# Cargar y limpiar
df_agrup = pd.read_csv('../data/clave_C_agrupacion.csv')
df_agrup = df_agrup.dropna().drop_duplicates()

# Selección y justificación de variables
# Usaremos las variables numéricas principales como 'ingresos', 'edad', 'satisfaccion' o similares.
df_num_agrup = df_agrup.select_dtypes(include=[np.number])
cols_clustering = df_num_agrup.columns

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_num_agrup)"""

text_ej3_2 = """### Método del Codo para determinar el valor de K
Buscamos el punto de inflexión donde añadir más clusters no reduce significativamente la inercia."""

code_ej3_2 = """from sklearn.cluster import KMeans

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
plt.show()"""

text_ej3_3 = """### Aplicación de K-Means
Asumiendo K=3 (según el gráfico anterior)."""

code_ej3_3 = """k_optimo = 3
kmeans = KMeans(n_clusters=k_optimo, random_state=42, n_init=10)

# Asignar cluster al dataframe original
df_agrup['Cluster'] = kmeans.fit_predict(df_scaled)

# Centroides para interpretación
centroides = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=cols_clustering)
print("Centroides en escala original:")
display(centroides)"""

text_ej3_4 = """### Visualización de Clusters"""

code_ej3_4 = """# Elegir dos variables representativas para el gráfico (ej. ingresos vs reclamos)
var_x = cols_clustering[1] # ingresos (normalmente)
var_y = cols_clustering[-2] # reclamos/satisfaccion

plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_agrup[var_x], y=df_agrup[var_y], hue=df_agrup['Cluster'], palette='viridis', s=100)
plt.title(f'Segmentación de Clientes: {var_x} vs {var_y}')
plt.savefig('../evidencia/clustering_segmentacion.png')
plt.show()

# Exportar resultados
df_agrup.to_csv('../resultados/clientes_segmentados.csv', index=False)
print("Dataset exportado a resultados/clientes_segmentados.csv")"""

text_ej3_5 = """### Interpretación y Recomendaciones de Segmentación
**Interpretación por Grupo (A ajustar según los centroides):**
- **Cluster 0:** Clientes premium (altos ingresos, compras altas).
- **Cluster 1:** Clientes en riesgo (baja satisfacción, altos reclamos).
- **Cluster 2:** Clientes estándar o nuevos.

**Acciones de Negocio:**
- Al **Cluster 1 (En riesgo)** se le debe enviar encuestas de satisfacción urgentes y cupones de retención.
- Al **Cluster 0 (Premium)** se le deben ofrecer programas VIP y productos exclusivos.
- Al **Cluster 2 (Estándar)** lanzar campañas de 'upselling' para que pasen a consumir más."""

# Armar las celdas
nb['cells'] = [
    nbf.v4.new_markdown_cell(text_intro),
    nbf.v4.new_code_cell(code_imports),
    
    nbf.v4.new_markdown_cell(text_ej1),
    nbf.v4.new_code_cell(code_ej1_1),
    nbf.v4.new_markdown_cell(text_ej1_2),
    nbf.v4.new_code_cell(code_ej1_2),
    nbf.v4.new_markdown_cell(text_ej1_3),
    nbf.v4.new_code_cell(code_ej1_3),
    nbf.v4.new_markdown_cell(text_ej1_4),
    nbf.v4.new_code_cell(code_ej1_4),
    nbf.v4.new_markdown_cell(text_ej1_5),
    
    nbf.v4.new_markdown_cell(text_ej2),
    nbf.v4.new_code_cell(code_ej2_1),
    nbf.v4.new_markdown_cell(text_ej2_2),
    nbf.v4.new_code_cell(code_ej2_2),
    nbf.v4.new_markdown_cell(text_ej2_3),
    
    nbf.v4.new_markdown_cell(text_ej3),
    nbf.v4.new_code_cell(code_ej3_1),
    nbf.v4.new_markdown_cell(text_ej3_2),
    nbf.v4.new_code_cell(code_ej3_2),
    nbf.v4.new_markdown_cell(text_ej3_3),
    nbf.v4.new_code_cell(code_ej3_3),
    nbf.v4.new_markdown_cell(text_ej3_4),
    nbf.v4.new_code_cell(code_ej3_4),
    nbf.v4.new_markdown_cell(text_ej3_5),
]

# Guardar el notebook
with open('c:/Users/LAB/Downloads/Parcial04/Proyecto_Analisis_Datos/notebook/Parcial_Analisis_Datos.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Jupyter Notebook generado exitosamente.")
