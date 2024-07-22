import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    # Configuración de la página debe ser la primera instrucción
    st.set_page_config(page_title="Economic Indicators Dashboard", layout="wide")


    # Cargar los datos
    wb_prices = pd.read_excel('Indicadores.xlsx', sheet_name='WB Prices')
    imae = pd.read_excel('Indicadores.xlsx', sheet_name='IMAE (Act. Eco. Var. Interanual')
    ivae = pd.read_excel('Indicadores.xlsx', sheet_name='El Salvador (IVAE)')
    ied = pd.read_excel('Indicadores.xlsx', sheet_name='IED ')
    IPC = pd.read_excel('Indicadores.xlsx', sheet_name='IPC Var Interanual')
    EMBI = pd.read_excel('Indicadores.xlsx', sheet_name='EMBI')
    EEUU_PIBT = pd.read_excel('Indicadores.xlsx', sheet_name='EEUU - PIB Trimestral')
    EEUU_CC = pd.read_excel('Indicadores.xlsx', sheet_name='EEUU - Confianza del Consumidor')
    EEUU_DS = pd.read_excel('Indicadores.xlsx', sheet_name='EEUU - Desempleo')

    # Convertir columna 'YM' a formato datetime en 'WB Prices'
    wb_prices['YM'] = pd.to_datetime(wb_prices['YM'], format='%Y-%m')

    # Ajustar el formato de fechas en IMAE
    if 'Fechas' in imae.columns:
        imae['Fechas'] = imae['Fechas'].str.replace('Enero', '01')
        imae['Fechas'] = imae['Fechas'].str.replace('Febrero', '02')
        imae['Fechas'] = imae['Fechas'].str.replace('Marzo', '03')
        imae['Fechas'] = imae['Fechas'].str.replace('Abril', '04')
        imae['Fechas'] = imae['Fechas'].str.replace('Mayo', '05')
        imae['Fechas'] = imae['Fechas'].str.replace('Junio', '06')
        imae['Fechas'] = imae['Fechas'].str.replace('Julio', '07')
        imae['Fechas'] = imae['Fechas'].str.replace('Agosto', '08')
        imae['Fechas'] = imae['Fechas'].str.replace('Septiembre', '09')
        imae['Fechas'] = imae['Fechas'].str.replace('Octubre', '10')
        imae['Fechas'] = imae['Fechas'].str.replace('Noviembre', '11')
        imae['Fechas'] = imae['Fechas'].str.replace('Diciembre', '12')
        imae['Fechas'] = pd.to_datetime(imae['Fechas'], format='%Y-%m')
    else:
        st.error("La hoja 'IMAE (Act. Eco. Var. Interanual)' no contiene la columna 'Fechas'.")

    # Ajustar el formato de fechas en IVAE y renombrar columna si es necesario
    if 'Fechas' in ivae.columns or 'Unnamed: 0' in ivae.columns:
        ivae.rename(columns={'Unnamed: 0': 'Fechas'}, inplace=True)
        ivae['Fechas'] = pd.to_datetime(ivae['Fechas'], errors='coerce')
        ivae = ivae.dropna(subset=['Fechas'])
    else:
        st.error("La hoja 'El Salvador (IVAE)' no contiene la columna 'Fechas'.")

    # Ajustar el formato de fechas en IED y renombrar columna si es necesario
    if 'Year' in ied.columns or 'Unnamed: 0' in ied.columns:
        ied.rename(columns={'Unnamed: 0': 'Year'}, inplace=True)
        ied['Year'] = pd.to_datetime(ied['Year'], format='%Y', errors='coerce')
        ied = ied.dropna(subset=['Year'])
    else:
        st.error("La hoja 'IED' no contiene la columna 'Year'.")

    st.image("logo_black.jpg", width=200)
    

##############################################################################
    # Título del Dashboard
    st.title("Economic Indicators Dashboard")

    # Sección WB Prices
    st.header("Seleccione el rango de fechas para WB Prices")
    if 'YM' in wb_prices.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = wb_prices['YM'].min().date()
        max_date = wb_prices['YM'].max().date()
        start_date_wb_prices, end_date_wb_prices = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
    
    #start_date = st.date_input("Fecha de inicio", value=wb_prices['YM'].min(), key='wb_start_date')
    #end_date = st.date_input("Fecha de fin", value=wb_prices['YM'].max(), key='wb_end_date')

    wb_prices_filtered = wb_prices[(wb_prices['YM'] >= pd.to_datetime(start_date_wb_prices)) & (wb_prices['YM'] <= pd.to_datetime(end_date_wb_prices))]

    st.header("Precios de Materias Primas")
    st.subheader("2014 a 2024, en $ por bbl, mmtbu, mt")
    line_fig = px.line(wb_prices_filtered, x='YM', y=['Crude oil, average ($/bbl)', 'Natural gas, US ($/mmbtu)', 
                                                      'Natural gas, Europe ($/mmbtu)', 'Maize ($/mt)', 
                                                      'Rice, Thai 5%  ($/mt)', 'Wheat, US SRW ($/mt)'],
                       title='Crude Oil y Natural Gas a lo largo del tiempo')
    
    line_fig.update_layout(yaxis=dict(title='Valores'))
    st.plotly_chart(line_fig, use_container_width=True)
    
    st.header("Precios Promedio de Productos Alimenticios")
    st.subheader("2014 a 2024, en $ por kg")
    line_fig = px.line(wb_prices_filtered, x='YM', y=['Beef ** ($/kg)', 'Chicken ** ($/kg)', 
                                                      'Coffee, Arabica ($/kg)', 'Coffee, Robusta ($/kg)', 
                                                      'Sugar, world ($/kg)'],
                       title='Alimentos')
    
    line_fig.update_layout(yaxis=dict(title='Valores'))
    st.plotly_chart(line_fig, use_container_width=True)

    st.subheader("Maize y Rice a lo largo del tiempo")
    line_fig2 = px.line(wb_prices_filtered, x='YM', y=['Maize ($/mt)', 'Rice, Thai 5%  ($/mt)'],
                        title='Maize y Rice a lo largo del tiempo')
    
    line_fig2.update_layout(yaxis=dict(title='Valores'))
    st.plotly_chart(line_fig2, use_container_width=True)

    st.subheader("Beef y Chicken a lo largo del tiempo")
    line_fig3 = px.line(wb_prices_filtered, x='YM', y=['Beef ** ($/kg)', 'Chicken ** ($/kg)'],
                        title='Beef y Chicken a lo largo del tiempo')
    line_fig3.update_layout(yaxis=dict(title='Valores'))
    st.plotly_chart(line_fig3, use_container_width=True)

    st.subheader("Sugar y Coffee a lo largo del tiempo")
    line_fig4 = px.line(wb_prices_filtered, x='YM', y=['Sugar, world ($/kg)', 'Coffee, Arabica ($/kg)', 'Coffee, Robusta ($/kg)'],
                        title='Sugar y Coffee a lo largo del tiempo')
    line_fig4.update_layout(yaxis=dict(title='Valores'))
    st.plotly_chart(line_fig4, use_container_width=True)


    # Filtrar los datos de la última fecha disponible
    ultima_fecha = wb_prices_filtered['YM'].max()
    datos_ultima_fecha = wb_prices_filtered[wb_prices_filtered['YM'] == ultima_fecha]

    # Mostrar tabla con los datos de la última fecha disponible
    st.subheader("Datos de la última fecha disponible")
    st.table(datos_ultima_fecha)


    ##########################################################################################

    # Sección IMAE
    st.header("Seleccione el rango de fechas para IMAE")
    if 'Fechas' in imae.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = imae['Fechas'].min().date()
        max_date = imae['Fechas'].max().date()
        start_date_imae, end_date_imae = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
        #start_date_imae = st.date_input("Fecha de inicio IMAE", value=imae['Fechas'].min(), key='imae_start_date')
        #end_date_imae = st.date_input("Fecha de fin IMAE", value=imae['Fechas'].max(), key='imae_end_date')

        imae_filtered = imae[(imae['Fechas'] >= pd.to_datetime(start_date_imae)) & (imae['Fechas'] <= pd.to_datetime(end_date_imae))]

        st.header("Indice Mensual de Actividad Economica (IMAE) en Centroamerica")
        st.subheader("2014 a 2024, Desagregado por País")
        imae_line_fig = px.line(imae_filtered, x='Fechas', y=imae.columns[1:], title='IMAE a lo largo del tiempo - Todos los países')
        imae_line_fig.update_layout(yaxis=dict(title='Valores'))
        st.plotly_chart(imae_line_fig, use_container_width=True)
    else:
        st.error("La hoja 'IMAE (Act. Eco. Var. Interanual)' no contiene la columna 'Fechas'.")


    
    # Filtrar los datos de la última fecha disponible
    ultima_fecha = imae_filtered['Fechas'].max()
    datos_ultima_fecha = imae_filtered[imae_filtered['Fechas'] == ultima_fecha]

    # Mostrar tabla con los datos de la última fecha disponible
    st.subheader("Datos de la última fecha disponible")
    st.table(datos_ultima_fecha)


    ############################################################################################
    # Sección IVAE
    st.header("Seleccione el rango de fechas para IVAE")
    if 'Fechas' in ivae.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = ivae['Fechas'].min().date()
        max_date = ivae['Fechas'].max().date()
        start_date_ivae, end_date_ivae = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
        #start_date_ivae = st.date_input("Fecha de inicio IVAE", value=ivae['Fechas'].min(), key='ivae_start_date')
        #end_date_ivae = st.date_input("Fecha de fin IVAE", value=ivae['Fechas'].max(), key='ivae_end_date')

        # ¡Aquí se arregla el problema!
        from datetime import datetime, date
        start_date_ivae = datetime.combine(start_date_ivae, datetime.min.time())
        end_date_ivae = datetime.combine(end_date_ivae, datetime.min.time())

        ivae_filtered = ivae[(ivae['Fechas'] >= start_date_ivae) & (ivae['Fechas'] <= end_date_ivae)]

        st.header("Indice de Variacion de la Actividad Economica en El Salvador")
        st.subheader("2014 a 2024, Desagregado por sector")
        # Gráfico específico tipo línea para IVAE y sus componentes
        fig = go.Figure()
        # Corrección para manejar columnas no numéricas
        ivae_filtered = ivae_filtered.loc[:, ~ivae_filtered.columns.str.contains('^Unnamed')]
        for column in ivae_filtered.columns[1:]:
            # Convertir la columna a numérica, reemplazando valores no numéricos con NaN
            ivae_filtered[column] = pd.to_numeric(ivae_filtered[column], errors='coerce')
            fig.add_trace(go.Scatter(x=ivae_filtered['Fechas'], y=ivae_filtered[column], mode='lines', name=column))
        fig.update_layout(title='IVAE y sus componentes a lo largo del tiempo', xaxis_title='Fecha', yaxis_title='Valores', legend=dict(orientation='h', yanchor='top', y=-0.2, xanchor='center', x=0.5))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("La hoja 'El Salvador (IVAE)' no contiene la columna 'Fechas'.")

    # Filtrar los datos de la última fecha disponible
    ultima_fecha = ivae_filtered['Fechas'].max()
    datos_ultima_fecha = ivae_filtered[ivae_filtered['Fechas'] == ultima_fecha]

    # Mostrar tabla con los datos de la última fecha disponible
    st.subheader("Datos de la última fecha disponible")
    st.table(datos_ultima_fecha)


###############################################################################


    # Ajustar el formato de fechas en IPC y renombrar columna si es necesario
    if 'Fechas' in IPC.columns or 'Unnamed: 0' in IPC.columns:
        IPC.rename(columns={'Unnamed: 0': 'Fechas'}, inplace=True)
        IPC['Fechas'] = pd.to_datetime(IPC['Fechas'], errors='coerce')
        IPC = IPC.dropna(subset=['Fechas'])
    else:
        st.error("La hoja 'IPC Var Interanual' no contiene la columna 'Fechas'.")


    # Sección IPC
    st.header("Seleccione el rango de fechas para IPC")
    if 'Fechas' in IPC.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = IPC['Fechas'].min().date()
        max_date = IPC['Fechas'].max().date()
        start_date_IPC, end_date_IPC = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
        #start_date_IPC = st.date_input("Fecha de inicio IPC", value=IPC['Fechas'].min(), key='IPC_start_date')
        #end_date_IPC = st.date_input("Fecha de fin IPC", value=IPC['Fechas'].max(), key='IPC_end_date')

        # ¡Aquí se arregla el problema!
        from datetime import datetime, date
        start_date_IPC = datetime.combine(start_date_IPC, datetime.min.time())
        end_date_IPC = datetime.combine(end_date_IPC, datetime.min.time())

        IPC_filtered = IPC[(IPC['Fechas'] >= start_date_IPC) & (IPC['Fechas'] <= end_date_IPC)]

        st.header("Indice de Precios al Consumidor, Variacion Interanual a Nivel C.A. 2014 a 2024")
        st.subheader("2014 a 2024, Países de Centroamérica")
        # Gráfico específico tipo línea para IPC y sus componentes
        fig = go.Figure()
        # Corrección para manejar columnas no numéricas
        IPC_filtered = IPC_filtered.loc[:, ~IPC_filtered.columns.str.contains('^Unnamed')]
        for column in IPC_filtered.columns[1:]:
            # Convertir la columna a numérica, reemplazando valores no numéricos con NaN
            IPC_filtered[column] = pd.to_numeric(IPC_filtered[column], errors='coerce')
            fig.add_trace(go.Scatter(x=IPC_filtered['Fechas'], y=IPC_filtered[column], mode='lines', name=column))
            fig.update_layout(yaxis=dict(title='Valores'))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("La hoja 'El Salvador (IPC)' no contiene la columna 'Fechas'.")


    # Filtrar los datos de la última fecha disponible
    ultima_fecha = IPC_filtered['Fechas'].max()
    datos_ultima_fecha = IPC_filtered[IPC_filtered['Fechas'] == ultima_fecha]

    # Mostrar tabla con los datos de la última fecha disponible
    st.subheader("Datos de la última fecha disponible")
    st.table(datos_ultima_fecha)


    ###############################################################################


    # Ajustar el formato de fechas en EMBI y renombrar columna si es necesario
    if 'Fecha' in EMBI.columns or 'Unnamed: 0' in EMBI.columns:
        EMBI.rename(columns={'Unnamed: 0': 'Fecha'}, inplace=True)
        EMBI['Fecha'] = pd.to_datetime(EMBI['Fecha'], errors='coerce')
        EMBI = EMBI.dropna(subset=['Fecha'])
    else:
        st.error("La hoja 'EMBI' no contiene la columna 'Fechas'.")


    # Sección EMBI
    st.header("Seleccione el rango de fechas para EMBI")
    if 'Fecha' in EMBI.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = EMBI['Fecha'].min().date()
        max_date = EMBI['Fecha'].max().date()
        start_date_EMBI, end_date_EMBI = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
        #start_date_EMBI = st.date_input("Fecha de inicio EMBI", value=EMBI['Fecha'].min(), key='EMBI_start_date')
        #end_date_EMBI = st.date_input("Fecha de fin EMBI", value=EMBI['Fecha'].max(), key='EMBI_end_date')

        # ¡Aquí se arregla el problema!
        from datetime import datetime, date
        start_date_EMBI = datetime.combine(start_date_EMBI, datetime.min.time())
        end_date_EMBI = datetime.combine(end_date_EMBI, datetime.min.time())

        EMBI_filtered = EMBI[(EMBI['Fecha'] >= start_date_EMBI) & (EMBI['Fecha'] <= end_date_EMBI)]

        st.header("EMBI")
        st.subheader("2014 a 2024, Países de Centroamérica")
        # Gráfico específico tipo línea para EMBI y sus componentes
        fig = go.Figure()
        # Corrección para manejar columnas no numéricas
        EMBI_filtered = EMBI_filtered.loc[:, ~EMBI_filtered.columns.str.contains('^Unnamed')]
        for column in EMBI_filtered.columns[1:]:
            # Convertir la columna a numérica, reemplazando valores no numéricos con NaN
            EMBI_filtered[column] = pd.to_numeric(EMBI_filtered[column], errors='coerce')
            fig.add_trace(go.Scatter(x=EMBI_filtered['Fecha'], y=EMBI_filtered[column], mode='lines', name=column))
            fig.update_layout(yaxis=dict(title='Valores'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("La hoja 'El Salvador (EMBI)' no contiene la columna 'Fechas'.")


        # Filtrar los datos de la última fecha disponible
        ultima_fecha = EMBI_filtered['Fecha'].max()
        datos_ultima_fecha = EMBI_filtered[EMBI_filtered['Fecha'] == ultima_fecha]

        # Mostrar tabla con los datos de la última fecha disponible
        st.subheader("Datos de la última fecha disponible")
        st.table(datos_ultima_fecha)


    ###############################################################################
    def convert_to_date(trimestre):
        if isinstance(trimestre, str) and '_' in trimestre:
            year, quarter = trimestre.split('_')
            month = (int(quarter) - 1) * 3 + 3  # Último mes del trimestre
            return pd.to_datetime(f"{year}-{month:02d}-01", errors='coerce')
        else:
            return pd.NaT

    if 'Trimestre' in EEUU_PIBT.columns:
        EEUU_PIBT['Fecha'] = EEUU_PIBT['Trimestre'].apply(convert_to_date)
        # Eliminar filas con fechas inválidas
        EEUU_PIBT = EEUU_PIBT.dropna(subset=['Fecha'])
        # Eliminar la columna original Trimestre
        EEUU_PIBT.drop(columns=['Trimestre'], inplace=True)
        # Reordenar las columnas para que 'Fecha' esté antes de 'Variación Interanual del PIB'
        cols = ['Fecha', 'Variación Interanual del PIB'] + [col for col in EEUU_PIBT.columns if col not in ['Fecha', 'Variación Interanual del PIB']]
        EEUU_PIBT = EEUU_PIBT[cols]
    else:
        st.error("La columna 'Trimestre' no se encuentra en el DataFrame.")

    # Sección en Streamlit para seleccionar el rango de Trimestre
    st.header("Seleccione el rango de Trimestre para EEUU PIB Trimestral")

    if 'Fecha' in EEUU_PIBT.columns:
        # Crear un control deslizante para el rango de Fecha
        min_date = EEUU_PIBT['Fecha'].min().date()
        max_date = EEUU_PIBT['Fecha'].max().date()
        start_date_EEUU_PIBT, end_date_EEUU_PIBT = st.slider(
            "Rango de Fecha",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
        
        # Convertir las fechas seleccionadas a datetime
        start_date_EEUU_PIBT = datetime.combine(start_date_EEUU_PIBT, datetime.min.time())
        end_date_EEUU_PIBT = datetime.combine(end_date_EEUU_PIBT, datetime.min.time())

        # Filtrar los datos basado en el rango seleccionado
        EEUU_PIBT_filtered = EEUU_PIBT[(EEUU_PIBT['Fecha'] >= start_date_EEUU_PIBT) & 
                                    (EEUU_PIBT['Fecha'] <= end_date_EEUU_PIBT)]

        st.header("Variación Interanual del PIB Trimestral")
        st.subheader("Estados Unidos, 2020 a 2024")
        
        # Gráfico específico tipo línea para EEUU_PIBT y sus componentes
        fig = go.Figure()
        # Corrección para manejar columnas no numéricas y excluir 'Fecha'
        columns_to_plot = EEUU_PIBT_filtered.columns.difference(['Fecha'])
        for column in columns_to_plot:
            # Convertir la columna a numérica, reemplazando valores no numéricos con NaN
            EEUU_PIBT_filtered[column] = pd.to_numeric(EEUU_PIBT_filtered[column], errors='coerce')
            fig.add_trace(go.Scatter(x=EEUU_PIBT_filtered['Fecha'], y=EEUU_PIBT_filtered[column], mode='lines', name=column))
        fig.update_layout(yaxis=dict(title='Valores'))

        st.plotly_chart(fig, use_container_width=True)
        
        # Filtrar los datos de la última fecha disponible
        ultima_fecha = EEUU_PIBT_filtered['Fecha'].max()
        datos_ultima_fecha = EEUU_PIBT_filtered[EEUU_PIBT_filtered['Fecha'] == ultima_fecha]

        # Mostrar tabla con los datos de la última fecha disponible
        st.subheader("Datos de la última fecha disponible")
        st.table(datos_ultima_fecha)


    ###############################################################################


    # Ajustar el formato de fechas en EEUU_CC y renombrar columna si es necesario
    if 'observation_date' in EEUU_CC.columns or 'Unnamed: 0' in EEUU_CC.columns:
        EEUU_CC.rename(columns={'Unnamed: 0': 'observation_date'}, inplace=True)
        EEUU_CC['observation_date'] = pd.to_datetime(EEUU_CC['observation_date'], errors='coerce')
        EEUU_CC = EEUU_CC.dropna(subset=['observation_date'])
    else:
        st.error("La hoja 'EEUU_CC' no contiene la columna 'observation_date'.")


    # Sección EEUU_CC
    st.header("Seleccione el rango de fechas para EEUU Confianza del Consumidor")
    if 'observation_date' in EEUU_CC.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = EEUU_CC['observation_date'].min().date()
        max_date = EEUU_CC['observation_date'].max().date()
        start_date_EEUU_CC, end_date_EEUU_CC = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD",
            key='slider_eeuu_cc'
        )
        #start_date_EEUU_CC = st.date_input("Fecha de inicio EEUU_CC", value=EEUU_CC['Fecha'].min(), key='EEUU_CC_start_date')
        #end_date_EEUU_CC = st.date_input("Fecha de fin EEUU_CC", value=EEUU_CC['Fecha'].max(), key='EEUU_CC_end_date')

        # ¡Aquí se arregla el problema!
        from datetime import datetime, date
        start_date_EEUU_CC = datetime.combine(start_date_EEUU_CC, datetime.min.time())
        end_date_EEUU_CC = datetime.combine(end_date_EEUU_CC, datetime.min.time())

        EEUU_CC_filtered = EEUU_CC[(EEUU_CC['observation_date'] >= start_date_EEUU_CC) & (EEUU_CC['observation_date'] <= end_date_EEUU_CC)]

        st.header("Universidad de Michigan, Sentimiento del Consumidor en EEUU")
        st.subheader("2014 a 2024, Año Base=1966 Q1")
        # Gráfico específico tipo línea para EEUU_CC y sus componentes
        fig = go.Figure()
        # Corrección para manejar columnas no numéricas
        EEUU_CC_filtered = EEUU_CC_filtered.loc[:, ~EEUU_CC_filtered.columns.str.contains('^Unnamed')]
        for column in EEUU_CC_filtered.columns[1:]:
            # Convertir la columna a numérica, reemplazando valores no numéricos con NaN
            EEUU_CC_filtered[column] = pd.to_numeric(EEUU_CC_filtered[column], errors='coerce')
            fig.add_trace(go.Scatter(x=EEUU_CC_filtered['observation_date'], y=EEUU_CC_filtered[column], mode='lines', name=column))
            fig.update_layout(yaxis=dict(title='Valores'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("La hoja 'El Salvador (EEUU_CC)' no contiene la columna 'Fechas'.")


    # Filtrar los datos de la última fecha disponible
    ultima_fecha = EEUU_CC_filtered['observation_date'].max()
    datos_ultima_fecha = EEUU_CC_filtered[EEUU_CC_filtered['observation_date'] == ultima_fecha]


    # Mostrar tabla con los datos de la última fecha disponible
    st.subheader("Datos de la última fecha disponible")
    st.table(datos_ultima_fecha)


    ###############################################################################


    # Ajustar el formato de fechas en EEUU_DS y renombrar columna si es necesario
    if 'Month' in EEUU_DS.columns or 'Unnamed: 0' in EEUU_DS.columns:
        EEUU_DS.rename(columns={'Unnamed: 0': 'Month'}, inplace=True)
        EEUU_DS['Month'] = pd.to_datetime(EEUU_DS['Month'], errors='coerce')
        EEUU_DS = EEUU_DS.dropna(subset=['Month'])
    else:
        st.error("La hoja 'EEUU_DS' no contiene la columna 'Month'.")


    # Sección EEUU_DS
    st.header("Seleccione el rango de fechas para EEUU Desempleo")
    if 'Month' in EEUU_DS.columns:
        # Crear un control deslizante para el rango de fechas
        min_date = EEUU_DS['Month'].min().date()
        max_date = EEUU_DS['Month'].max().date()
        start_date_EEUU_DS, end_date_EEUU_DS = st.slider(
            "Rango de fechas",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD",
            key='slider_eeuu_ds'
        )
        #start_date_EEUU_DS = st.date_input("Fecha de inicio EEUU_DS", value=EEUU_DS['Fecha'].min(), key='EEUU_DS_start_date')
        #end_date_EEUU_DS = st.date_input("Fecha de fin EEUU_DS", value=EEUU_DS['Fecha'].max(), key='EEUU_DS_end_date')

        # ¡Aquí se arregla el problema!
        from datetime import datetime, date
        start_date_EEUU_DS = datetime.combine(start_date_EEUU_DS, datetime.min.time())
        end_date_EEUU_DS = datetime.combine(end_date_EEUU_DS, datetime.min.time())

        EEUU_DS_filtered = EEUU_DS[(EEUU_DS['Month'] >= start_date_EEUU_DS) & (EEUU_DS['Month'] <= end_date_EEUU_DS)]

        st.header("Desempleo en EEUU, Total y Latino")
        st.subheader("Desde 2014 a 2024")
        # Gráfico específico tipo línea para EEUU_DS y sus componentes
        fig = go.Figure()
        # Corrección para manejar columnas no numéricas
        EEUU_DS_filtered = EEUU_DS_filtered.loc[:, ~EEUU_DS_filtered.columns.str.contains('^Unnamed')]
        for column in EEUU_DS_filtered.columns[1:]:
            # Convertir la columna a numérica, reemplazando valores no numéricos con NaN
            EEUU_DS_filtered[column] = pd.to_numeric(EEUU_DS_filtered[column], errors='coerce')
            fig.add_trace(go.Scatter(x=EEUU_DS_filtered['Month'], y=EEUU_DS_filtered[column], mode='lines', name=column))
            fig.update_layout(yaxis=dict(title='Valores'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("La hoja 'EEUU - Desempleo' no contiene la columna 'Month'.")


    # Filtrar los datos de la última fecha disponible
    ultima_fecha = EEUU_DS_filtered['Month'].max()
    datos_ultima_fecha = EEUU_DS_filtered[EEUU_DS_filtered['Month'] == ultima_fecha]


    # Mostrar tabla con los datos de la última fecha disponible
    st.subheader("Datos de la última fecha disponible")
    st.table(datos_ultima_fecha)


    ###############################################################################



if __name__ == "__main__":
    main()
