# import streamlit as st 
# import pandas as pd


# df = pd.read_csv('Market Share Corretoras - df.csv')

# df = df[['Corretora Consolidada', 'Nº Contratos', 'Ano', 'Tipo', 'Share %', 'Valor Financeiro']]
# df['Ano'] = df['Ano'].astype(str)
# df['Ano'] = df['Ano'].str.replace(',','')

# df['Share %'] = df['Share %'].str.replace('%', '')
# df['Share %'] = df['Share %'].str.replace(',', '.')
# df['Share %'] = pd.to_numeric(df['Share %'], errors='coerce')

# df['Valor Financeiro'] = df['Valor Financeiro'].str.replace(',', '.')
# df['Valor Financeiro'] = pd.to_numeric(df['Valor Financeiro'], errors='coerce')

# df['Nº Contratos'] = df['Nº Contratos'].astype(str)
# df['Nº Contratos'] = df['Nº Contratos'].str.replace(',','')
# df['Nº Contratos'] = pd.to_numeric(df['Nº Contratos'], errors='coerce')

# st.title('Market Share Corretoras')

# tipos_disponiveis = df["Tipo"].unique()
# tipos_disponiveis = ['Todos'] + df["Tipo"].unique().tolist()


# tipo_selecionado = st.selectbox("Selecione o Tipo de Mercado:", options=tipos_disponiveis)

# if tipo_selecionado != 'Todos':
#     df = df[df["Tipo"] == tipo_selecionado]

# valor = "Share %"
# if tipo_selecionado == 'BOVESPA TOTAL':
#     valor = 'Valor Financeiro'
    
# df2 = pd.pivot_table(
#     df,
#     values=valor,
#     index=["Corretora Consolidada"],
#     columns=["Ano"],   
#     aggfunc="sum",
#     fill_value=0
# )

# df2 = df2.sort_values(by=df2.columns[-1], ascending=False)
# df2 = df2.reset_index()

# df3 = pd.pivot_table(
#     df,
#     values=['Nº Contratos'],
#     index=["Corretora Consolidada"],
#     columns=["Ano"],   
#     aggfunc="sum",
#     fill_value=0
# )
# df3 = df3.sort_values(by=df3.columns[-1], ascending=False)
# df3 = df3.reset_index()

# df3['Gráfico'] = df3[df3.columns[1:]].apply(list, axis=1)


# col1, col2 = st.columns(2)
# if valor == 'Valor Financeiro':
#     with col1:
#         st.subheader(f'Bovespa Total por Corretora')
#         st.dataframe(df2, hide_index=True)
# else:
#     with col1: 
#         if tipo_selecionado != 'Todos':        
#             st.subheader(f'Market Share % de {tipo_selecionado}')
#             st.dataframe(df2, hide_index=True)

#     with col2:
#         st.subheader(f'Nº Contratos de {tipo_selecionado}')
#         df3 = df3[['Corretora Consolidada', 'Nº Contratos', 'Gráfico']]
#         st.dataframe(df3, hide_index=True,column_config={

#         "": st.column_config.LineChartColumn(
#             "Últimos anos",
#             width="medium"
#          ),
#     },)