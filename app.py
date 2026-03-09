import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Procesador de CSV", page_icon="📊")

st.title("🚀 Procesador de CSV AFIP")
st.write("Sube tu archivo y descarga el resultado con formato Unix (LF).")

uploaded_file = st.file_uploader("Elegir archivo CSV", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8-sig')

        st.success("Archivo cargado correctamente.")

        columns_to_delete = [9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        available_indices = [i for i in columns_to_delete if i < len(df.columns)]
        column_names = [df.columns[i] for i in available_indices]
        df = df.drop(columns=column_names)

        nombres_correctos = [
            "Fecha de Emisión", "Tipo de Comprobante", "Punto de Venta",
            "Número Desde", "Número Hasta", "Cód. Autorización",
            "Tipo Doc. Emisor", "Nro. Doc. Emisor", "Denominación Emisor",
            "Tipo Cambio", "Moneda", "Imp. Neto Gravado",
            "Imp. Neto No Gravado", "Imp. Op. Exentas", "Otros Tributos",
            "IVA", "Imp. Total"
        ]
        date = datetime.now().strftime('%Y%m%d')

        if len(df.columns) == len(nombres_correctos):
            df.columns = nombres_correctos
        else:
            st.warning(f"Ojo: El número de columnas resultantes ({len(df.columns)}) no coincide con el de nombres esperados.")

        if 'Moneda' in df.columns:
            df['Moneda'] = df['Moneda'].replace('$', 'PES')

       
        output = io.StringIO()
        
        header_line = ';'.join(f'"{h}"' for h in df.columns) + '\n'
        output.write(header_line)
        
        df.to_csv(output, index=False, header=False, sep=';', lineterminator='\n')
        
        csv_bytes = output.getvalue().encode('utf-8')

        st.download_button(
            label="⬇️ Descargar archivo corregido",
            data=csv_bytes,
            file_name = f"AFIPComprobanteEmitidoActualizado_{date}.csv",
            mime="text/csv"
        )
        
        st.info("Vista previa de los datos procesados:")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Hubo un error: {e}")