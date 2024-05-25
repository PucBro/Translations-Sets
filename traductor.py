import pandas as pd
from googletrans import Translator

# Cargar el archivo XLSX
file_path = '/home/diego/Descargas/EC Translations-25_05_2024 10 13 GMT+05 30.xlsx'
df = pd.read_excel(file_path)

# Inicializar el traductor
translator = Translator()

# Identificar entradas repetidas en la columna 'English (UK) [Primary]'
duplicates = df[df.duplicated(subset=['English (UK) [Primary]'], keep=False)]


if not duplicates.empty:
    print("Entradas repetidas encontradas:")
    print(duplicates)
    
    # Eliminar filas duplicadas, manteniendo la primera ocurrencia
    df = df.drop_duplicates(subset=['English (UK) [Primary]'], keep='first')

# Traducir la columna 'English (UK) [Primary]' al español
df.loc[df['Spanish'].isnull(), 'Spanish'] = df.loc[df['Spanish'].isnull(), 'English (UK) [Primary]'].apply(lambda x: translator.translate(x, src='en', dest='es').text if pd.notnull(x) else x)

# Llenar la columna 'Description' para valores nulos
description_text = 'EC_c_hznReqForInfo'
df['Description'] = df['Description'].fillna(description_text)

# Guardar el archivo modificado en un nuevo XLSX
output_file_path = '/home/diego/Descargas/EC_Translations_Modificado.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Archivo guardado en: {output_file_path}")
