import pandas as pd
import plotly.graph_objs as go

import streamlit as st

# Importa el documento, ETL
df0 = pd.read_excel('Data_Caso_BI.xlsx', skiprows=4)
df=df0.loc[:,'CLIENTE':'SI Real FACTURADO']

# Algunas transformaciones
df.columns=df.columns.str.upper()
df=df.rename(columns={'GASTO REAL FCT MONTO CLP': 'GASTO REAL', 'GASTO PROYECCIÓN INICIAL': 'GASTO PLAN'})

st.set_page_config(layout="wide")
st.sidebar.header("Filtros")


# Función que según los filtros seleccionados devuelve un dataframe filtrado
def filter_data(df, cliente, marca, pulgada, tecnología, modelo, periodo):
    if cliente != "Todos":
        df = df[df["CLIENTE"] == cliente]
    if marca != "Todos":
        df = df[df["MARCA"] == marca]
    if pulgada != "Todos":
        df = df[df["PULGADA"] == pulgada]
    if tecnología != "Todos":
        df = df[df["TECNOLOGÍA"] == tecnología]
    if modelo != "Todos":
        df = df[df["MODELO"] == modelo]
    df = df.groupby([periodo, 'CLIENTE', 'MARCA', 'PULGADA', 'TECNOLOGÍA', 'MODELO']).sum().reset_index()
    return df


def main():
    st.title("Dashboard")
    periodo = st.sidebar.selectbox("Seleccione el período de tiempo", ["SEMANA", "MES"])
    cliente = st.sidebar.selectbox("Cliente", ["Todos"] + sorted(df["CLIENTE"].unique().tolist()))
    marca = st.sidebar.selectbox("Marca", ["Todos"] + sorted(df["MARCA"].unique().tolist()))
    pulgada = st.sidebar.selectbox("Pulgada", ["Todos"] + sorted(df["PULGADA"].unique().tolist()))
    tecnología = st.sidebar.selectbox("Tecnología", ["Todos"] + sorted(df["TECNOLOGÍA"].unique().tolist()))
    modelo = st.sidebar.selectbox("Modelo", ["Todos"] + sorted(df["MODELO"].unique().tolist()))
    
    df_filtered = filter_data(df, cliente, marca, pulgada, tecnología, modelo, periodo)
    x_axis = periodo

    #Layout
   
    col1, col2 = st.columns(2, gap="medium")
    
    #Columna 1
    with col1:

        # Agrega el df por periodo
        df_grafico=df_filtered.groupby(periodo).sum().reset_index()
 
        #SELL IN

        df_grafico['% CUMPLIMIENTO SELL IN'] = df_grafico['SELL IN REAL UNIDADES'] / df_grafico['SELL IN PLAN INICIAL UNIDADES'] * 100
        bar_sell_in = go.Bar(x=df_grafico[x_axis], y=df_grafico['SELL IN REAL UNIDADES'], name='SELL IN REAL (Ud)', marker_color='#9fd3c7')
        scatter_sell_in = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['SELL IN PLAN INICIAL UNIDADES'], 
            name='SELL IN PLAN (Ud)', 
            mode='markers', 
            marker=dict(size=10, line=dict(width=3), color='#113f67', symbol='line-ew-open'))
        line_sell_in = go.Scatter(x=df_grafico[x_axis],
            y=df_grafico['% CUMPLIMIENTO SELL IN'], 
            name='% CUMPLIMIENTO SELL IN',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#a2c11c', width=2),
            hovertext=[f"{x:.2f}%" for x in df_grafico['% CUMPLIMIENTO SELL IN']],
            hoverinfo='text')

        data_sell_in = [bar_sell_in, scatter_sell_in, line_sell_in]
        layout_sell_in = go.Layout(title=f'SELL IN REAL (Ud) vs SELL IN PLAN (Ud)',
            xaxis_title=periodo, 
            yaxis_title='Unidades',
            yaxis2=dict(title='% CUMPLIMIENTO',
                overlaying='y', 
                side='right',
                autorange=False,
                range=[0,300]), 
            legend=dict(x=0.1, y=1.15, orientation="h"))
        fig_sell_in = go.Figure(data=data_sell_in, layout=layout_sell_in)


        #SELL OUT
        df_grafico['% CUMPLIMIENTO SELL OUT'] = df_grafico['SELL OUT REAL UNIDADES'] / df_grafico['SELL OUT PLAN INICIAL UNIDADES'] * 100
        bar_sell_out = go.Bar(x=df_grafico[x_axis], y=df_grafico['SELL OUT REAL UNIDADES'], name='SELL OUT REAL (Ud)', marker_color='#9fd3c7')
        scatter_sell_out = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['SELL OUT PLAN INICIAL UNIDADES'], 
            name='SELL OUT PLAN (Ud)',
            mode='markers', 
            marker=dict(size=10, line=dict(width=3), color='#113f67', symbol='line-ew-open'))
        line_sell_out = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['% CUMPLIMIENTO SELL OUT'], 
            name='% CUMPLIMIENTO SELL OUT', 
            yaxis='y2', 
            mode='lines+markers', 
            line=dict(color='#a2c11c', width=2),
            hovertext=[f"{x:.2f}%" for x in df_grafico['% CUMPLIMIENTO SELL OUT']],
            hoverinfo='text')

        data_sell_out = [bar_sell_out, scatter_sell_out, line_sell_out]
        layout_sell_out = go.Layout(title=f'SELL OUT REAL (Ud) vs SELL OUT PLAN (Ud)', 
            xaxis_title=periodo, 
            yaxis_title='Unidades', 
            yaxis2=dict(title='% CUMPLIMIENTO', 
            overlaying='y', 
            side='right', range=[0,300]), 
            legend=dict(x=0.1, y=1.15, orientation="h"))
        fig_sell_out = go.Figure(data=data_sell_out, layout=layout_sell_out)

        #TOTAL
        df_grafico['TOTAL SELL REAL UNIDADES']=df_grafico['SELL IN REAL UNIDADES'] + df_grafico['SELL OUT REAL UNIDADES']
        df_grafico['TOTAL SELL PLAN UNIDADES']=df_grafico['SELL IN PLAN INICIAL UNIDADES'] + df_grafico['SELL OUT PLAN INICIAL UNIDADES']

        df_grafico['% CUMPLIMIENTO TOTAL'] = df_grafico['TOTAL SELL REAL UNIDADES'] / df_grafico['TOTAL SELL PLAN UNIDADES'] * 100

        bar_total_sell_in = go.Bar(x=df_grafico[x_axis], y=df_grafico['SELL IN REAL UNIDADES'], name= 'SELL IN REAL (Ud)', marker_color='#2d6e7e')
        bar_total_sell_out = go.Bar(x=df_grafico[x_axis], y=df_grafico['SELL OUT REAL UNIDADES'],  name= 'SELL OUT REAL (Ud)', marker_color='#9fd3c7')

        scatter_total_sell = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['TOTAL SELL PLAN UNIDADES'], 
            name='TOTAL SELL PLAN (Ud)', 
            mode='markers', 
            marker=dict(size=10, line=dict(width=3), color='#113f67', symbol='line-ew-open'))

        line_total_sell = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['% CUMPLIMIENTO TOTAL'], 
            name='% CUMPLIMIENTO TOTAL', 
            yaxis='y2', 
            mode='lines+markers+text',
            textposition='middle center',
            line=dict(color='#a2c11c', width=2),
            hovertext=[f"{x:.2f}%" for x in df_grafico['% CUMPLIMIENTO TOTAL']],
            hoverinfo='text')

        data_total_sell = [bar_total_sell_in, bar_total_sell_out, scatter_total_sell, line_total_sell]
        layout_total_sell = go.Layout(title=f'TOTAL SELL REAL (Ud) vs TOTAL SELL PLAN (Ud)', 
            xaxis_title=periodo, 
            yaxis_title='Unidades', 
            yaxis2=dict(title='% CUMPLIMIENTO', overlaying='y', side='right', range=[0,300]), 
            legend=dict(x=0.1, y=1.15, orientation="h"))
        fig_total_sell = go.Figure(data=data_total_sell, layout=layout_total_sell)
        fig_total_sell.update_layout(barmode='stack')

        
        # Selecionador tipo de venta y desplega el gráfico correspondiente
        sales_options = ["TOTAL", "SELL IN", "SELL OUT"]
        selected_sales_option=st.selectbox("Seleccione el tipo de venta a visualizar:", sales_options)
        if selected_sales_option=="SELL IN":
            st.plotly_chart(fig_sell_in, use_column_width=True, use_container_width=True)
        elif selected_sales_option=="SELL OUT":
            st.plotly_chart(fig_sell_out, use_column_width=True, use_container_width=True)
        else:
            st.plotly_chart(fig_total_sell, use_column_width=True, use_container_width=True)
        
        # Gráfico de stock total
        df_grafico['WOS']=df_grafico['INVENTARIO DEL CANAL']/df_grafico['TOTAL SELL REAL UNIDADES']

        stock = go.Bar(x=df_grafico[x_axis], y=df_grafico['INVENTARIO DEL CANAL'], name= 'STOCK TOTAL (Ud)', marker_color='#2d6e7e')
        wos = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['WOS'], 
            name='WEEKS OF STOCK', 
            yaxis='y2', 
            mode='lines+markers',
            line=dict(color='#a2c11c', width=2),
            hovertext=[f"{x:.2f} Semanas" for x in df_grafico['WOS']],
            hoverinfo='text')
        
        data_stock = [stock, wos]
        layout_stock = go.Layout(title=f'STOCK (Ud) y WEEKS OF STOCK',
            xaxis_title=periodo, 
            yaxis_title='Unidades', 
            yaxis2=dict(title='WEEKS OF STOCK', overlaying='y', side='right', range=[0,None]),
            legend=dict(x=0.1, y=1.15, orientation="h"))
        fig_stock=go.Figure(data=data_stock, layout=layout_stock)
        st.plotly_chart(fig_stock, use_container_width=False)

        
        
    with col2:
        # Gráfico de Gasto Real vs Plan
        gasto_real = go.Bar(x=df_grafico[x_axis], y=df_grafico['GASTO REAL'], name='GASTO REAL (CLP)', marker_color='#9fd3c7')
        gasto_plan = go.Bar(x=df_grafico[x_axis], y=df_grafico['GASTO PLAN'], name='GASTO PLAN (CLP)')
        gasto_plan = go.Scatter(x=df_grafico[x_axis], 
            y=df_grafico['GASTO PLAN'],
            name='GASTO PLAN (CLP)',
            mode='markers', 
            marker=dict(size=10, line=dict(width=3), color='#113f67', symbol='line-ew-open'))
        layout_gastos = go.Layout(title='GASTO REAL vs GASTO PLAN (CLP)', 
            yaxis_title='CLP', 
            xaxis_title=periodo,
            legend=dict(x=0.1, y=1.15, orientation="h"))
        fig_gastos = go.Figure(data=[gasto_real, gasto_plan], layout=layout_gastos)
        st.plotly_chart(fig_gastos, use_column_width=True, use_container_width=True)


    #Mostrar dataframe del grafico
    st.write("Datos filtrados:")
    st.dataframe(df_grafico)


if __name__ == "__main__":
    main()