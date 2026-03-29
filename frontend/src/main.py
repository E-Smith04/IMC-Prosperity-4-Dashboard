import streamlit as st
from app.core.session_state import init_session_state

init_session_state()

historical_page = st.Page("app/pages/historical.py", title="Historical", icon=":material/analytics:")
logs_page = st.Page("app/pages/logs.py", title="Logs", icon=":material/notes:")

pg = st.navigation([historical_page, logs_page])
st.set_page_config(page_title="IMC Prosperity 4 Dashboard", layout="wide")
pg.run()
