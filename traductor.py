import streamlit as st
import pandas as pd
from googletrans import Translator

# Título de la aplicación
st.title('Traducción de Archivo XLSX')

# Subida de archivos mediante drag and drop
uploaded_file = st.file_uploader("Sube tu archivo XLSX", type=["xlsx"])

# Entrada de texto para la descripción por defecto
description_text = st.text_input("Ingrese la descripción para valores nulos", "Descripción por defecto")

if uploaded_file is not None:
    # Leer el archivo XLSX
    df = pd.read_excel(uploaded_file)
    
    st.write("Archivo cargado exitosamente:")
    st.dataframe(df.head())
    
    # Identificar entradas repetidas en la columna 'English (UK) [Primary]'
    duplicates = df[df.duplicated(subset=['English (UK) [Primary]'], keep=False)]
    
    if not duplicates.empty:
        st.write("Entradas repetidas encontradas:")
        st.dataframe(duplicates)
        
        # Eliminar filas duplicadas, manteniendo la primera ocurrencia
        df = df.drop_duplicates(subset=['English (UK) [Primary]'], keep='first')
    
    # Inicializar el traductor
    translator = Translator()

    # Traducir la columna 'English (UK) [Primary]' al español
    df['Spanish'] = df['English (UK) [Primary]'].apply(lambda x: translator.translate(x, src='en', dest='es').text if pd.notnull(x) else x)

    # Llenar la columna 'Description' para valores nulos con el texto proporcionado por el usuario
    df['Description'] = df['Description'].fillna(description_text)

    # Mostrar el DataFrame modificado
    st.write("Archivo modificado:")
    st.dataframe(df.head())

    # Guardar el archivo modificado en un nuevo archivo XLSX
    output_file_path = 'FAD_Translations_Modificado.xlsx'
    df.to_excel(output_file_path, index=False)

    # Descargar el archivo modificado
    st.download_button(
        label="Descargar archivo modificado",
        data=open(output_file_path, 'rb').read(),
        file_name=output_file_path,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
