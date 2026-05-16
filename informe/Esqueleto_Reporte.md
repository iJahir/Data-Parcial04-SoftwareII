# Reporte Final: Evaluación Ordinaria 4
**UNIVERSIDAD TECNOLÓGICA DE EL SALVADOR**
**FACULTAD DE INFORMÁTICA Y CIENCIAS APLICADAS - ESCUELA DE INFORMÁTICA**

**Asignatura:** TÉCNICAS DE PRODUCCIÓN INDUSTRIAL DE SOFTWARE II (TE2)
**Profesor:** Jorge Edwin Machado
**Sección:** 01 | **Ciclo:** 01-2026
**Alumno:** Aldo Jahir Marroquin Villator
**No de carnet:** 25-1628-2020
**Fecha:** 16-05-2026

---

## 1. Introducción
El presente informe documenta los resultados obtenidos tras aplicar técnicas de Inteligencia de Negocios y Minería de Datos sobre distintos conjuntos de información comercial. El objetivo principal de este trabajo es extraer valor de los datos "crudos" mediante algoritmos estadísticos y de Machine Learning no supervisado, permitiendo a la empresa tomar decisiones informadas y estratégicas basadas en el comportamiento real de sus clientes.

## 2. Objetivos
- **Objetivo General:** Desarrollar e interpretar modelos de agrupación, correlación y asociación para encontrar patrones ocultos en el comportamiento comercial y demográfico de los clientes.
- **Objetivos Específicos:**
  - Identificar reglas de compra conjunta mediante el algoritmo Apriori para estrategias de venta cruzada.
  - Determinar relaciones matemáticas (correlaciones positivas y negativas) entre métricas de clientes (como ingresos y reclamos) que impacten la satisfacción y ventas.
  - Segmentar a la cartera de clientes utilizando K-Means para diseñar acciones de marketing focalizadas.

---

## 3. Desarrollo y Resultados

### 3.1 Ejercicio 1: Análisis de Asociación (Reglas de Compra)
**Descripción:** Se utilizó el dataset de transacciones para identificar qué productos se compran típicamente juntos. Tras preparar los datos en un formato binario por transacción, se aplicó el algoritmo Apriori fijando un soporte mínimo del 5%.

**Captura del Código y Top Reglas:**
*(Inserta aquí una captura de pantalla del Notebook mostrando el Top 10 de reglas generadas)*

**Interpretación (Lenguaje de Negocio):**
- **Regla 1:** Los clientes que adquieren [Producto A] tienen un [X]% de probabilidad de comprar [Producto B]. Su indicador de *Lift* es de [Y], lo que significa que la probabilidad de que se compren juntos es mucho mayor que si se compraran al azar.
- *(Repite para las 5 reglas principales que arroje tu Notebook)*

**Recomendaciones Comerciales:**
1. Crear un paquete promocional uniendo el Producto A y el Producto B, ya que los clientes los perciben como complementarios.
2. Posicionar físicamente o en el carrito web el Producto B justo antes del proceso de pago cuando el cliente lleva el Producto A.
3. Ofrecer envío gratuito cuando se adquiera el conjunto completo de las asociaciones más fuertes.

---

### 3.2 Ejercicio 2: Análisis de Correlación
**Descripción:** Se evaluó el dataset de métricas de cliente para entender la interacción entre variables numéricas.

**Captura del Mapa de Calor:**
*(Inserta aquí la imagen `heatmap_clave_C_correlacion.png` que se encuentra en la carpeta evidencia)*

**Interpretación:**
- **Correlación Positiva más fuerte:** Se halló entre [Ingresos] y [Consumo]. Esto significa que a mayor ingreso, los clientes gastan proporcionalmente más.
- **Correlación Negativa más fuerte:** Se observó entre [Reclamos] y [Satisfacción]. A medida que crecen los reclamos de un cliente, su satisfacción desciende considerablemente.
- *(Explica 2 relaciones más que observes en los colores del mapa)*

**Conclusión Comercial:**
Las correlaciones demuestran que reducir el tiempo de respuesta y los reclamos es vital, ya que impactan matemáticamente la satisfacción y, eventualmente, la retención. La empresa debe enfocar su soporte al cliente en los segmentos que muestran caídas en satisfacción.

---

### 3.3 Ejercicio 3: Agrupación o Clustering (K-Means)
**Descripción:** Con el objetivo de segmentar a la clientela, se usó el algoritmo K-Means. Tras normalizar los datos, el método del codo sugirió agrupar en 3 clústeres.

**Captura del Gráfico de Clusters:**
*(Inserta aquí la imagen `clustering_segmentacion.png` que se encuentra en la carpeta evidencia)*

**Interpretación de Grupos (Clústeres):**
- **Cluster 0 (Premium):** Representa clientes de altos ingresos que compran frecuentemente y gastan mucho.
- **Cluster 1 (En Riesgo):** Segmento con alta tasa de reclamos, baja satisfacción y uso mínimo de la app.
- **Cluster 2 (Estándar):** El grueso de los clientes. Compran esporádicamente pero no presentan quejas graves.

**Acciones de Negocio:**
- **Para Cluster 0:** Lanzar membresía VIP que ofrezca beneficios exclusivos para recompensar su lealtad.
- **Para Cluster 1:** Iniciar campaña de retención inmediata, ofreciendo bonos de disculpa o atención prioritaria para mitigar la insatisfacción.
- **Para Cluster 2:** Enviar boletines de marketing ("newsletter") para incrementar su frecuencia de compra mediante ofertas relámpago.

---

## 4. Conclusiones Generales
El análisis desarrollado permitió transformar tres conjuntos de datos aislados en estrategias de negocio concretas. Se comprobó que el análisis de datos no supervisado no solo describe la situación actual, sino que prevé el comportamiento futuro (como la propensión a comprar productos juntos). La implementación de estas recomendaciones puede traducirse en mayores ingresos mediante venta cruzada, y mayor retención abordando a los clientes del Clúster "en riesgo" antes de que abandonen la empresa.
