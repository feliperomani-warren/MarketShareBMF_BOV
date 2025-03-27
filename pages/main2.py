import pandas as pd
import streamlit as st 
import altair as alt

st.set_page_config(page_title="Market Share Corretoras", page_icon=":material/finance_mode:", layout="wide")#, initial_sidebar_state="expanded")
color_scale_assets = ["#C64F39", "#AC783F", "#D8A370", "#34639C", "#688EC7", "#356D3E", "#69986F", "#44737E", "#749EA9", "#7E527A", "#A880A4", "#913042", "#BC6672", "#51448C", "#7E74B7"]



@st.cache_data
def processar_planilha(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)

    nomes_chaves = ["DI1", "DOL", "FRC", "DAP", "mini DOL", "mini IND", "FRP0", "BOVESPA TOTAL", "BM&F TOTAL"]
    meses = ("Jan", "Fev", "Mar", "Abr", "Mai", "Jun","Jul", "Ago", "Set", "Out", "Nov", "Dez")
    anos_abas = ("25")
    meses_para_numeros = {mes: i+1 for i, mes in enumerate(meses)}
    abas_filtradas = [sheet for sheet in xls.sheet_names if sheet.endswith(anos_abas)]

    dfs_dict = {}
    for aba in abas_filtradas:
        df1 = pd.read_excel(uploaded_file, sheet_name=aba, header=3)
        assert len(nomes_chaves) == (df1.shape[1] // 5), "Erro: Número de chaves não corresponde ao número de DataFrames esperados!"
        
        nome_mes = aba[:3]
        num_mes = meses_para_numeros.get(nome_mes, None)
        
        for i, nome in enumerate(nomes_chaves):
            df_temp = df1.iloc[:, i*5:(i+1)*5].copy()
            df_temp.columns = [col.split(".")[0] for col in df_temp.columns]
            
            df_temp["Ativo"] = nome
            df_temp["Mês"] = aba
            df_temp["Número do Mês"] = num_mes
            df_temp["Ano"] = 2025

            if nome not in dfs_dict:
                dfs_dict[nome] = []

            dfs_dict[nome].append(df_temp)

    df = pd.concat([pd.concat(dfs_dict[key], ignore_index=True) for key in dfs_dict], ignore_index=True)
    df = df.dropna(subset=["Corretora"])
    
    # df = df[df["Ativo"] != "BM&F TOTAL"]
    df["Número do Mês"] = df["Número do Mês"].astype(str)
    df = df[["Ativo", "Posição", "Corretora", "Nº Contratos", "Share %", "Valor Financeiro", "Ano", "Número do Mês"]]
    
    return df

##################################################################################################################################################################################################


st.subheader("Market Share Corretoras")
st.write("Baixe a planilha no [Link](https://docs.google.com/spreadsheets/d/1A81APA-rlsFABha9PjCR9-v9pJp9UZ0y/edit?gid=552196343#gid=552196343)")
uploaded_file = st.file_uploader("Insira o Arquivo de mkt_share_corretoras.xlsx", type=["xlsx"])
if uploaded_file is not None:
    df = processar_planilha(uploaded_file)
    df_BMF = df[df["Ativo"] == "BM&F TOTAL"]
    df_BOV = df[df["Ativo"] == "BOVESPA TOTAL"]
    df = df[(df["Ativo"] != "BM&F TOTAL") & (df["Ativo"] != "BOVESPA TOTAL")]
    
    mercado = st.radio("Selecione o Mercado", ["BMF", "BOV"])
    if mercado == "BOV":
        df = df[["Ativo", "Posição", "Corretora", "Valor Financeiro", "Share %", "Ano", "Número do Mês"]]
        df = df[df["Ativo"] == "BOVESPA TOTAL"]
        df_mercado = df_BOV.groupby(["Número do Mês"])["Valor Financeiro"].sum().reset_index()
        df_ranking = df_BOV.groupby(["Corretora", "Número do Mês"])["Valor Financeiro"].sum().reset_index().sort_values(by="Valor Financeiro", ascending=False)
        
    elif mercado == "BMF":
        df = df[["Ativo", "Posição", "Corretora",   "Nº Contratos",   "Share %", "Ano", "Número do Mês"]]
        df = df[df["Ativo"] != "BOVESPA TOTAL"]
        df_mercado = df_BMF.groupby(["Número do Mês"])["Nº Contratos"].sum().reset_index()
        df_ranking = df_BMF.groupby(["Corretora", "Número do Mês"])["Nº Contratos"].sum().reset_index().sort_values(by="Nº Contratos", ascending=False)
    
    st.write(f"Como está o mercado de {mercado} em 2025?")
    col1,col2 = st.columns(2)
    with col1:
        chart = alt.Chart(df_mercado).mark_bar(color="#C7452D").encode(
            x='Número do Mês',
            y=alt.Y(df_mercado.columns[1])
            ,tooltip=[alt.Tooltip(df_mercado.columns[1], format=',.2f')]
        ).properties(
            height=400,
            width=800,
            title=f"{df_mercado.columns[1]} por Mês"
        )
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dx=5, 
            dy=-5   
        ).encode(
            text=alt.Text(df_mercado.columns[1], format=',.2f'),
            color=alt.value('white')
        )
        final_chart = (chart.encode(
            y=alt.Y(df_mercado.columns[1], sort='-x', axis=None)
        ) + text)
        st.altair_chart(final_chart, use_container_width=True)    

    with col2:
        mes = st.selectbox("Selecione o Mês", ["Todos"]+df["Número do Mês"].unique().tolist(), key="mes")
        if mes == "Todos":
            df_ranking = df_ranking.groupby("Corretora")[df_ranking.columns[2]].sum().reset_index().sort_values(by=df_ranking.columns[2], ascending=False)
        else:
            df_ranking = df_ranking[df_ranking["Número do Mês"] == mes]
        
        col1,col2 = st.columns(2)
        with col1:            
            df_ranking["Posição"] = df_ranking[df.columns[3]].rank(ascending=False)
            total_mercado = df_ranking[df.columns[3]].sum()
            df_ranking["Share %"] = round(((df_ranking[df.columns[3]])/(total_mercado)*100),2)
            df_ranking = df_ranking[["Posição", "Corretora", df.columns[3], "Share %"]]
            df_ranking = df_ranking.sort_values('Share %', ascending=False)
            st.dataframe(df_ranking, hide_index = True)
        with col2:
            df_rena = df_ranking[df_ranking["Corretora"] == "RENASCENCA"]
            st.dataframe(df_rena, hide_index = True)
            chart = alt.Chart(df_ranking).mark_arc().encode(
                theta=alt.Theta("Share %:Q", stack=True),
                color=alt.Color(
                    "Corretora:N", 
                    scale=alt.Scale(
                        domain=df_ranking['Corretora'].tolist(),
                        range=color_scale_assets[:len(df_ranking)]
                    )
                ),
                order=alt.Order("Share %:Q", sort="descending"),
                tooltip=["Corretora", "Share %"]
            )
            st.altair_chart(chart, use_container_width=True)
    
    
    
    if mercado == "BMF":
        col1, col2 = st.columns(2)
        with col1:
            ativo = st.selectbox("Selecione o Ativo", df["Ativo"].unique())
            df = df[df["Ativo"] == ativo]
    
        with col2:
            # corretora = st.selectbox("Selecione a Corretora", ["Todas"]+df["Corretora"].unique().tolist())
            # if corretora != "Todas":
            #     df = df[df["Corretora"] == corretora]
            mes1 = st.selectbox("Selecione o Mês", ["Todos"]+df["Número do Mês"].unique().tolist(), key="mes1")     
            if mes1 != "Todos":
                df = df[df["Número do Mês"] == mes1]

        col1,col2 = st.columns(2)
        with col1:
            df_ativo = df.groupby(["Número do Mês"])["Nº Contratos"].sum().reset_index()
            
            chart = alt.Chart(df_ativo).mark_bar(color="#C7452D").encode(
                x='Número do Mês',
                y=alt.Y(df_ativo.columns[1])
                ,tooltip=[alt.Tooltip(df_ativo.columns[1], format=',.2f')]
            )
        
            st.altair_chart(chart, use_container_width=True)        
        
        with col2:
            df_ranking_ativo = df.groupby(['Corretora'])["Nº Contratos"].sum().reset_index()
            df_ranking_ativo["Posição"] = df_ranking_ativo["Nº Contratos"].rank(ascending=False)
            total_mercado_ativo = df_ranking_ativo["Nº Contratos"].sum()
            df_ranking_ativo["Share %"] = round(((df_ranking_ativo["Nº Contratos"])/(total_mercado_ativo)*100),2)
            df_ranking_ativo = df_ranking_ativo[['Posição', 'Corretora','Nº Contratos', "Share %"]].sort_values(by="Posição", ascending=True)
            st.dataframe(df_ranking_ativo, hide_index = True)   
        
        df = processar_planilha(uploaded_file)
        df_corretoras = df[(df["Ativo"] != "BM&F TOTAL") & (df["Ativo"] != "BOVESPA TOTAL")]
        df_corretoras = df_corretoras.groupby(["Corretora", "Ativo"])["Nº Contratos"].sum().reset_index()
        df_corretoras['Total Contratos por Ativo'] = df_corretoras.groupby("Ativo")["Nº Contratos"].transform('sum')
        df_corretoras['Share %'] = df_corretoras['Nº Contratos'] / df_corretoras['Total Contratos por Ativo'] * 100
        df_corretoras['Posição'] = df_corretoras.groupby("Ativo")["Nº Contratos"].rank(method='dense', ascending=False).astype(int)
        df_corretoras['Share %'] = df_corretoras['Share %'].round(2)
        
        df_corretoras = df_corretoras[["Posição","Corretora", "Ativo", "Nº Contratos", "Share %"]]

        # Ordenar para melhor visualização
        df_corretoras = df_corretoras.sort_values(['Ativo', 'Nº Contratos'], ascending=[True, False])

        corretora = st.selectbox("Selecione a Corretora", ["Todas"]+df["Corretora"].unique().tolist())
        if corretora != "Todas":
            df_corretoras = df_corretoras[df_corretoras["Corretora"] == corretora]
        
        st.dataframe(df_corretoras.sort_values(by="Nº Contratos", ascending=False), hide_index=True)
    
    
    
    
    
    # df_contratos_mercado = df.groupby(["Ativo"])["Nº Contratos"].sum().reset_index()
    # df_bovespa_total = df.groupby(["Ativo"])["Valor Financeiro"].sum().reset_index()