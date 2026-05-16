import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# Configuración de estilo para las gráficas
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def main():
    print("Iniciando Análisis de Datos...")
    
    # 1. Carga de datos
    # Construimos la ruta absoluta basada en la ubicación de este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "..", "data")
    archivos_csv = [
        "clave_C_agrupacion.csv",
        "clave_C_asociacion.csv",
        "clave_C_correlacion.csv"
    ]
    
    for archivo in archivos_csv:
        ruta = os.path.join(base_path, archivo)
        if not os.path.exists(ruta):
            print(f"\n[!] Archivo no encontrado: {ruta}")
            continue
            
        print(f"\n{'='*60}")
        print(f"Analizando Dataset: {archivo}")
        print(f"{'='*60}")
        
        # Carga del dataset
        df = pd.read_csv(ruta)
        
        # 2. Exploración de datos y revisión de columnas
        print("\n--- Primeras filas del dataset ---")
        print(df.head())
        
        print("\n--- Información del dataset ---")
        print(df.info())
        
        # 3. Detección de nulos y duplicados
        print("\n--- Valores Nulos detectados ---")
        nulos = df.isnull().sum()
        print(nulos[nulos > 0] if nulos.sum() > 0 else "No hay valores nulos.")
        if nulos.sum() > 0:
            df = df.dropna()
            print("-> Filas con valores nulos eliminadas para evitar errores.")
        
        print("\n--- Valores Duplicados ---")
        duplicados = df.duplicated().sum()
        print(f"Cantidad de filas duplicadas: {duplicados}")
        if duplicados > 0:
            df = df.drop_duplicates()
            print("-> Duplicados eliminados.")
        
        # 4. Estadísticas descriptivas
        print("\n--- Estadísticas Descriptivas ---")
        print(df.describe())
        
        # Seleccionar solo columnas numéricas para correlación y clustering
        df_numeric = df.select_dtypes(include=[np.number])
        
        if df_numeric.empty or df_numeric.shape[1] < 2:
            print(f"-> [!] No hay suficientes datos numéricos en {archivo} para correlación o clustering.")
            continue
            
        # 5. Matriz de Correlación y Mapa de Calor
        print("\n--- Generando Matriz de Correlación y Mapa de Calor ---")
        corr = df_numeric.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title(f"Mapa de Calor de Correlación - {archivo}")
        plt.tight_layout()
        
        # Guardar evidencia
        grafica_corr_path = os.path.join(script_dir, "..", "evidencia", f"heatmap_{archivo.replace('.csv', '.png')}")
        plt.savefig(grafica_corr_path)
        print(f"-> Mapa de calor guardado en: {grafica_corr_path}")
        # plt.show() # Descomentar para ver en ventana al ejecutar
        plt.close()
        
        # 6. Clustering con K-Means (Solo si el archivo sugiere agrupación)
        if "agrupacion" in archivo.lower():
            print("\n--- Ejecutando Clustering (K-Means) ---")
            
            # Escalar los datos
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df_numeric)
            
            # Fijamos k=3 por defecto (el usuario o analista puede ajustarlo tras evaluar el codo)
            k_optimo = 3
            kmeans = KMeans(n_clusters=k_optimo, random_state=42, n_init=10)
            df['Cluster'] = kmeans.fit_predict(df_scaled)
            
            print(f"\n-> Centroides de los {k_optimo} clusters generados (en escala original):")
            centroides = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=df_numeric.columns)
            print(centroides)
            
            # Gráficas de los Clusters (Usando las dos primeras columnas numéricas para visualización 2D)
            cols = df_numeric.columns
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=df[cols[0]], y=df[cols[1]], hue=df['Cluster'], palette="viridis", s=100)
            plt.title(f"Clustering K-Means (K={k_optimo}) - {archivo}")
            plt.xlabel(cols[0])
            plt.ylabel(cols[1])
            plt.tight_layout()
            
            # Guardar evidencia
            grafica_cluster_path = os.path.join(script_dir, "..", "evidencia", f"clusters_{archivo.replace('.csv', '.png')}")
            plt.savefig(grafica_cluster_path)
            print(f"-> Gráfica de clusters guardada en: {grafica_cluster_path}")
            # plt.show() # Descomentar para ver en ventana al ejecutar
            plt.close()
            
            # Guardar resultados
            resultado_path = os.path.join(script_dir, "..", "resultados", f"resultados_kmeans_{archivo}")
            df.to_csv(resultado_path, index=False)
            print(f"-> Resultados de clustering exportados a: {resultado_path}")

    print("\n¡Análisis completado exitosamente!")

if __name__ == "__main__":
    main()
