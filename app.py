import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Empanadas Familiares", layout="wide")

# JS para bajar el teclado al presionar Enter
components.html(
    """
    <script>
    const inputs = window.parent.document.querySelectorAll('input[type="number"]');
    window.parent.document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            window.parent.document.activeElement.blur();
        }
    });
    </script>
    """,
    height=0,
)

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #fdf2e9; }
    [data-testid="stHeaderActionElements"] { display: none; }
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a { display: none; }
    input[type=number] { font-size: 1.2rem !important; }
    </style>
""", unsafe_allow_html=True)

if 'sabores' not in st.session_state:
    st.session_state.sabores = [
        "Caprese", "Carne Picante", "Carne Suave", "Cebolla y Queso",
        "Choclo y Queso", "Espinaca y Mozzarella", "Jamón y Queso", "Pollo",
        "Queso y Cebolla Verdeo", "Queso y Tomate", "Sfijas", "Ternera"
    ]

if 'personas' not in st.session_state:
    st.session_state.personas = {}

def agregar_persona():
    nombre = st.session_state.nuevo_nombre.strip()
    if nombre and nombre not in st.session_state.personas:
        st.session_state.personas[nombre] = {sabor: 0 for sabor in st.session_state.sabores}
        st.session_state.nuevo_nombre = ""

def agregar_sabor():
    nuevo_s = st.session_state.nuevo_sabor_input.strip()
    if nuevo_s and nuevo_s not in st.session_state.sabores:
        st.session_state.sabores.append(nuevo_s)
        for p in st.session_state.personas:
            st.session_state.personas[p][nuevo_s] = 0
        st.session_state.nuevo_sabor_input = ""

st.title("🥟 Empanadas Familiares")

col_in1, col_in2 = st.columns(2)
with col_in1:
    st.text_input("Nombre de la persona:", key="nuevo_nombre", on_change=agregar_persona)
    st.button("➕ Agregar Persona", on_click=agregar_persona)
with col_in2:
    st.text_input("¿Nuevo sabor?", key="nuevo_sabor_input", on_change=agregar_sabor)
    st.button("➕ Agregar Sabor", on_click=agregar_sabor)

st.divider()

for nombre in list(st.session_state.personas.keys()):
    st.markdown(f"### 👤 {nombre}")
    cols = st.columns(4)
    for idx, sabor in enumerate(st.session_state.sabores):
        with cols[idx % 4]:
            # Al cambiar el número, Streamlit procesa y el JS quita el foco
            val = st.number_input(
                label=sabor,
                min_value=0,
                step=1,
                value=st.session_state.personas[nombre][sabor],
                key=f"input_{nombre}_{sabor}"
            )
            st.session_state.personas[nombre][sabor] = val
    
    if st.button(f"🗑️ Quitar a {nombre}", key=f"del_{nombre}"):
        del st.session_state.personas[nombre]
        st.rerun()
    st.divider()

# --- RESUMEN ---
st.header("📊 Resumen del Pedido")
totales = {}
total_gral = 0
for p_pedidos in st.session_state.personas.values():
    for sabor, cant in p_pedidos.items():
        if cant > 0:
            totales[sabor] = totales.get(sabor, 0) + cant
            total_gral += cant

if totales:
    resumen_cols = st.columns(2)
    with resumen_cols:
        for s, c in sorted(totales.items(), key=lambda x: x, reverse=True):
            st.write(f"✅ **{c}** {s}")
    with resumen_cols:
        docenas = total_gral // 12
        sueltas = total_gral % 12
        st.metric("Total Empanadas", total_gral)
        st.write(f"📦 **{docenas} docenas + {sueltas} unidades**")
else:
    st.info("Agregá a alguien para empezar el conteo.")

