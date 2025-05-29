import tensorflow as tf
import numpy as np
import json

# Cargar modelo
model = tf.keras.models.load_model("saved_model/modelo.keras")

# Tokenizer
with open("saved_model/vocabulary.txt", "r") as f:
    vocabulary = [line.strip() for line in f]

tokenizer = tf.keras.layers.TextVectorization(output_mode="int", output_sequence_length=20)
tokenizer.set_vocabulary(vocabulary)

# Etiquetas
with open("saved_model/etiquetas.json", "r") as f:
    etiquetas = json.load(f)

index_to_label = {v: k for k, v in etiquetas.items()}

def predecir_categoria(pregunta: str) -> str:
    texto_preprocesado = tokenizer([pregunta])
    prediccion = model.predict(texto_preprocesado)
    indice = int(np.argmax(prediccion[0]))
    return index_to_label.get(indice, "NO_ENTIENDO")