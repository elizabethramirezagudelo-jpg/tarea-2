import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Máquina de Reconocimiento de Patrones", layout="wide")

st.title("Tarea 2: Máquina de Puntuación de Patrones (Letra T)")
st.write("Ajusta los pesos para maximizar el puntaje de las letras 'T' y minimizar el de otras figuras.")

# ---------------------------------------------------------
# 1. DEFINICIÓN DE IMÁGENES BINARIAS (3 T y 3 No T)
# ---------------------------------------------------------
imagenes = {
    "T Tradicional (Positiva 1)": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    "T Alta (Positiva 2)": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ], 
    "T Ancha (Positiva 2)": [
        [1, 1, 1],
        [1, 1, 1],
        [0, 1, 0]
    ],
    "T Corta (Positiva 3)": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 0, 0]
    ],
    "Cruz / Más (Negativa 1)": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    "Línea Horizontal (Negativa 2)": [
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0]
    ],
    "Cuadrado Hueco (Negativa 3)": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
}

# ---------------------------------------------------------
# 2. SISTEMA DE PESOS INTERACTIVO (Perillas)
# ---------------------------------------------------------
st.sidebar.header("Ajuste de Pesos (Matriz $3 \\times 3$)")

# Creamos una matriz para guardar los sliders
w = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# Renderizar los sliders en una cuadrícula en el sidebar
for i in range(3):
    cols = st.sidebar.columns(3)
    for j in range(3):
        # Valor inicial sugerido en la guía para ciertas posiciones
        val_inicial = 2 if i == 0 else (-1 if j != 1 else 3)
        w[i][j] = cols[j].slider(f"W_{i}{j}", min_value=-5, max_value=5, value=val_inicial, step=1)

# Umbral (Threshold) opcional
threshold = st.sidebar.slider("Umbral de Decisión (Threshold)", min_value=-10, max_value=20, value=5, step=1)

# ---------------------------------------------------------
# 3. INTERFAZ PRINCIPAL Y CÁLCULO (Python Básico)
# ---------------------------------------------------------
col_izq, col_der = st.columns([1, 2])

with col_izq:
    st.subheader("Selecciona una Imagen")
    nombre_img = st.selectbox("Imagen de prueba:", list(imagenes.keys()))
    img_seleccionada = imagenes[nombre_img]
    
    # Dibujar la imagen de forma visual simple
    st.write("Visualización del patrón (1=Activo, 0=Apagado):")
    for fila in img_seleccionada:
        # Convertir 1 a cuadrado lleno y 0 a vacío para un look de "juego"
        st.code(" ".join(["⬛" if pixel == 1 else "⬜" for pixel in fila]))

with col_der:
    st.subheader("Cálculo de la Máquina")
    
    # Operación matemática básica: y = Σ(w_i * x_i)
    puntaje_total = 0
    detalles_calculo = []
    
    for i in range(3):
        for j in range(3):
            x_ij = img_seleccionada[i][j]
            w_ij = w[i][j]
            producto = x_ij * w_ij
            puntaje_total += producto
            if x_ij == 1:
                detalles_calculo.append(f"({w_ij} × {x_ij})")
    
    # Mostrar la ecuación de forma amigable
    operacion_str = " + ".join(detalles_calculo) if detalles_calculo else "0"
    st.markdown(f"**Fórmula:** $y = \\sum(w_i x_i)$")
    st.markdown(f"**Cálculo:** {operacion_str} = `{puntaje_total}`")
    
    # Resultado final basado en el Threshold
    st.write("---")
    if puntaje_total >= threshold:
        st.success(f"**¡Clasificado como T!** (Puntaje {puntaje_total} ≥ Umbral {threshold})")
    else:
        st.error(f"**No es una T** (Puntaje {puntaje_total} < Umbral {threshold})")

# ---------------------------------------------------------
# TABLA COMPARATIVA EN TIEMPO REAL
# ---------------------------------------------------------
st.write("---")
st.subheader("Rendimiento con la configuración actual de pesos")
st.write("Compara cómo rinden todas las imágenes simultáneamente con tus 'perillas' actuales:")

num_imagenes = len(imagenes)
columnas_tabla = st.columns(num_imagenes)

for idx, (nombre, img) in enumerate(imagenes.items()):
    with columnas_tabla[idx]: # Ahora 'idx' nunca superará el límite
        # Calcular puntaje
        p = sum(img[i][j] * w[i][j] for i in range(3) for j in range(3))
        es_t_real = "Positiva" in nombre
        
        st.caption(nombre)
        if p >= threshold:
            st.metric(label="Predicción: T", value=p, delta="Correcto" if es_t_real else "Falso Positivo", delta_color="normal" if es_t_real else "inverse")
        else:
            st.metric(label="Predicción: No T", value=p, delta="Falso Negativo" if es_t_real else "Correcto", delta_color="inverse" if es_t_real else "normal")