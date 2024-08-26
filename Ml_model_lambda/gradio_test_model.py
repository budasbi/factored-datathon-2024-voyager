import pandas as pd
from sklearn.datasets import load_iris

!pip install gradio

import gradio as gr
import pandas as pd
import pickle

# Cargar el modelo desde el archivo
with open("voyager_model.pkl", "rb") as file:
    model = pickle.load(file)

# Asumamos que el modelo espera exactamente 9 características
expected_features = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else [f"feature_{i}" for i in range(9)]

# Función para predecir usando el modelo cargado
def predict(values):
    # Convertir la cadena de texto a una lista de valores flotantes
    values_list = [float(value) for value in values.split(",")]

    # Verificar que la lista tiene la cantidad correcta de valores
    if len(values_list) != len(expected_features):
        raise ValueError(f"Se esperaban {len(expected_features)} valores, pero se recibieron {len(values_list)}.")

    # Convertir la lista en un DataFrame con una sola fila
    df = pd.DataFrame([values_list], columns=expected_features)

    # Realizar predicciones
    predictions = model.predict(df)
    return predictions[0]

# Función para ser utilizada por Gradio
def gradio_interface(input_text):
    try:
        result = predict(input_text)
        return result
    except Exception as e:
        return str(e)

# Crear la interfaz de usuario con Gradio
iface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=1, placeholder="Ingrese 9 valores separados por comas"),
    outputs="text",
    live=True
)

# Ejecutar la interfaz
iface.launch()