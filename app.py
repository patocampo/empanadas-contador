import streamlit as st

st.set_page_config(page_title="Empanadas Familiares", layout="wide")

# Estilo para mejorar la visualización y "limpiar" los ceros visualmente
st.markdown("""
    <style>
    /* Oculta los eslabones/vínculos al lado de los títulos */
    .viewerBadge_container__1QS1n, .st-emotion-cache-15zrgzn e16p96971 {
        display: none;
    }
    /* Esta es la forma más efectiva de quitar el icono del ancla */
    [data-testid="stHeaderActionElements"] {
        display: none;
    }
    a.viewerBadge_link__1S137 {
        display: none;
    }
    /* Quita el icono de enlace específicamente en los encabezados */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DE LA APP ---
if 'sabores' not in st.session_state:
    st.session_state.sabores = [
        "Caprese", "Carne Picante", "Carne Suave", "Cebolla y Queso",
        "Choclo y Queso", "Espinaca y Mozzarella", "Jamón y Queso", "Pollo",
        "Queso y Cebolla Verdeo", "Queso y Tomate", "Sfijas", "Ternera"
    ]

if 'personas' not in st.session_state:
    st.session_state.personas = {}

# --- FUNCIONES ---
def agregar_persona():
    nombre = st.session_state.nuevo_nombre.strip()
    if nombre and nombre not in st.session_state.personas:
        st.session_state.personas[nombre] = {sabor: 0 for sabor in st.session_state.sabores}
        st.session_state.nuevo_nombre = ""

def agregar_sabor():
    nuevo_s = st.session_state.nuevo_sabor_input.strip()
    if nuevo_s and nuevo_s not in st.session_state.sabores:
        st.session_state.sabores.append(nuevo_s)
        # Actualizar a las personas existentes con el nuevo sabor en 0
        for p in st.session_state.personas:
            st.session_state.personas[p][nuevo_s] = 0
        st.session_state.nuevo_sabor_input = ""

# --- INTERFAZ ---
st.title("🥟 Empanadas Familiares")

# Sección de entradas (Nombre y Sabores)
col_in1, col_in2 = st.columns(2)
with col_in1:
    st.subheader("👥 Personas")
    st.text_input("Nombre de la persona:", key="nuevo_nombre", on_change=agregar_persona, placeholder="Ej: Juan")
    st.button("➕ Agregar Persona", on_click=agregar_persona)

with col_in2:
    st.subheader("✨ Sabores")
    st.text_input("¿Nuevo sabor?", key="nuevo_sabor_input", on_change=agregar_sabor, placeholder="Ej: Roquefort")
    st.button("➕ Agregar Sabor", on_click=agregar_sabor)

st.divider()

# --- GRILLA DE CONTEO ---
for nombre in list(st.session_state.personas.keys()):
    with st.container():
        st.markdown(f"### 👤 {nombre}")
        cols = st.columns(4)
        
        for idx, sabor in enumerate(st.session_state.sabores):
            with cols[idx % 4]:
                # Para solucionar el "04", el truco en Streamlit es usar value=None 
                # pero number_input prefiere números. 
                # La mejor forma es que al hacer click el usuario borre, 
                # o usar un valor por defecto 0 pero que se limpie.
                val = st.session_state.personas[nombre].get(sabor, 0)
                
                nuevo_val = st.number_input(
                    label=sabor,
                    min_value=0,
                    step=1,
                    value=val,
                    key=f"input_{nombre}_{sabor}"
                )
                st.session_state.personas[nombre][sabor] = nuevo_val
        
        st.button(f"🗑️ Quitar a {nombre}", key=f"del_{nombre}", type="secondary")
        st.markdown("---")

# --- RESUMEN FINAL ---
st.header("📊 Resumen del Pedido")
totales = {}
total_gral = 0

for p_pedidos in st.session_state.personas.values():
    for sabor, cant in p_pedidos.items():
        if cant > 0:
            totales[sabor] = totales.get(sabor, 0) + cant
            total_gral += cant

if totales:
    c1, c2 = st.columns(2)
    with c1:
        for s, c in sorted(totales.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"⭐ **{c}** - {s}")
    
    with c2:
        docenas = total_gral // 12
        sueltas = total_gral % 12
        st.metric("Total de Empanadas", total_gral)
        st.info(f"Son **{docenas} docenas** y **{sueltas} sobrantes**")
else:
    st.warning("No hay pedidos registrados.")
