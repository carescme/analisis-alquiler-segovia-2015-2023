# Análisis del Mercado Inmobiliario y Predicción de Alquileres: Provincia de Segovia

Este proyecto realiza un análisis integral del mercado del alquiler en la provincia de Segovia, cruzando datos de renta per cápita (INE) con precios medios de vivienda (Ministerio de Vivienda) entre los años 2015-2022. El objetivo es identificar zonas de tensión económica y anomalías donde el precio del alquiler se desacopla de la capacidad adquisitiva local.

## 📊 Resumen de Resultados
- **Correlación Renta-Alquiler:** 0.61 (Relación sólida pero influenciada por factores externos).
- **Zonas de Tensión:** Identificación de municipios con un esfuerzo financiero superior al 30%.
- **Anomalía Principal:** **Segovia Capital**, con un sobreprecio de +107€ respecto a la tendencia central de la provincia.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.8.20
- **Análisis de Datos:** Pandas, NumPy.
- **Visualización:** Seaborn, Matplotlib.
- **Machine Learning:** Scikit-Learn (Linear Regression).

## 📂 Estructura del Proyecto
El análisis se divide en cuatro notebooks secuenciales:

1. **`01_Limpieza_y_Preparacion.ipynb`**: Consolidación de fuentes de datos heterogéneas y normalización de variables.
2. **`02_Analisis_Exploratorio.ipynb`**: Cálculo de métricas de esfuerzo, análisis de correlación y visualización de la distribución provincial.
3. **`03_Analisis_Comparativo.ipynb`**: Segmentación de municipios por perfiles (Tensionados, alrededores y Oportunidad).
4. **`04_Machine_Learning.ipynb`**: Modelado predictivo y análisis de residuos para la detección de anomalías de mercado.

## 📈 Conclusiones Técnicas
A pesar de contar con una muestra limitada (n=24), el modelo de **Machine Learning** permitió diagnosticar que el mercado inmobiliario de Segovia es multivariante. El bajo $R^2$ (0.26) actúa como evidencia estadística de que factores como la presión demográfica de la Comunidad de Madrid y la escasez de oferta tienen un impacto mayor que la simple renta neta en municipios clave como **Cuellar, El Espinar y Segovia Capital**.

---
*Este proyecto forma parte de mi portfolio profesional de Data Science.*