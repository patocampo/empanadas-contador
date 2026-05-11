import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Empanadas Familiares", layout="wide")

# ==================== JAVASCRIPT MEJORADO ====================
components.html(
    """
    <script>
    function blurActiveInput() {
        const active = window.parent.document.activeElement;
        if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA')) {
            active.blur();
        }
    }

    // Capturar botón "Sig." y Enter
    window.parent.document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.keyCode === 13) {
            e.preventDefault();
            setTimeout(blurActiveInput, 10);
        }
    }, true);

    window.parent.document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' || e.keyCode === 13) {
            e.preventDefault();
            setTimeout(blurActiveInput, 10);
        }
    }, true);

    // Observador para nuevos inputs
    const observer = new MutationObserver(() => {
        const inputs = window.parent.document.querySelectorAll('input[type="number"], input[type="text"]');
        inputs.forEach(input => {
            if (input.dataset.keyboardFixed) return;
            input.dataset.keyboardFixed = 'true';

            // Al cambiar valor → cerrar teclado
            input.addEventListener('change', () => {
                setTimeout(blurActiveInput, 100);
            });

            // Al soltar el dedo (importante en móviles)
            input.addEventListener('touchend', () => {
                setTimeout(blurActiveInput, 150);
            });

            // Doble toque también puede ayudar
            input.addEventListener('blur', () => {
                // Por si el usuario toca fuera
            });
        });
    });

    observer.observe(window.parent.document.body, { 
        childList: true, 
        subtree: true 
    });

    // Click fuera también cierra
    window.parent.document.addEventListener('touchend', function(e) {
        if (!e.target.closest('input')) {
            setTimeout(blurActiveInput, 80);
        }
    }, { passive: true });
    </script>
    """,
    height=0,
)

# ==================== ESTILOS ====================
st.markdown("""
    <style>
    .main { background-color: #fdf2e9; }
    [data-testid="stHeaderActionElements"] { display: none; }
    
    /* Inputs grandes y cómodos en celular */
    .stNumberInput input {
        font-size: 1.3rem !important;
        height: 3.4rem !important;
        padding: 0.6rem !important;
    }
    
    /* NO usar tabindex -1 porque bloquea el teclado */
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
if 'sabores' not in st.session_state:
    st.session_state.sabores = [
        "Caprese", "Carne Picante", "Carne Suave", "Cebolla y Queso",
        "Choclo y Queso", "Espinaca y Mozzarella", "Jamón y Queso", "Pollo",
        "Queso y Cebolla Verdeo", "Queso y Tomate", "Sfijas", "Ternera"
    ]

if 'personas' not in st.session_state:
    st.session_state.personas = {}

def agregar_persona():
    nombre = st.session_state.get("nuevo_nombre", "").strip()
    if nombre and nombre not in st.session_state.personas:
        st.session_state.personas[nombre] = {sabor: 0 for sabor in st.session_state.sabores}
        st.session_state.nuevo_nombre = ""

def agregar_sabor():
    nuevo_s = st.session_state.get("nuevo_sabor_input", "").strip()
    if nuevo_s and nuevo_s not in st.session_state.sabores:
        st.session_state.sabores.append(nuevo_s)
        for p in st.session_state.personas:
            st.session_state.personas[p][nuevo_s] = 0
        st.session_state.nuevo_sabor_input = ""

# --- INTERFAZ ---
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
    with resumen_cols[0]: 
        for s, c in sorted(totales.items(), key=lambda x: x[1], reverse=True):
            st.write(f"✅ **{c}** {s}")
    
    with resumen_cols[1]:
        docenas = total_gral // 12
        sueltas = total_gral % 12
        st.metric("Total", f"{total_gral} unidades")
        st.write(f"📦 {docenas} doc. + {sueltas} sueltas")
else:
    st.info("No hay pedidos.")
