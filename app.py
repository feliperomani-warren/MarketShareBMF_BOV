import streamlit as st

# --- PAGE SETUP ---
pagina_inicial = st.Page(
    "pages/main2.py",
    title="Dados",
    icon=":material/database:",
    default=True,
)

# pagina_resultados = st.Page(
#     "pages/Acompanhamento_Metas.py",
#     title="Acompanhamento Metas",
#     icon=":material/target:",
# )

# pagina_login = st.Page(
#     "pages/login.py",
#     title="Login",
#     icon=":material/contacts:",
# )

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation({
    "Dados": [pagina_inicial],
    # "Informações": [pagina_login],
})


# --- RUN NAVIGATION ---
pg.run()