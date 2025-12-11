import streamlit as st
import requests
import pandas as pd
import altair as alt
import time
from datetime import date
import requests.exceptions

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Gimnasio Inteligente",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS ---
def local_css():
    st.markdown("""
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        /* Fondo y base */
        body, .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e5e7eb;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #020617 0%, #1e293b 100%);
            border-right: 1px solid #334155;
        }
        
        /* Pestañas de Login/Registro */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: #94a3b8;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(34, 211, 238, 0.1);
            color: #22d3ee;
            border-bottom: 2px solid #22d3ee;
        }

        /* Métricas */
        div[data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.6);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #334155;
            backdrop-filter: blur(10px);
        }
        
        /* Contenedores */
        .stContainer {
            border-radius: 12px !important;
            border: 1px solid #334155 !important;
            background: rgba(15, 23, 42, 0.5) !important;
        }
        
        h1 { color: #22d3ee; font-weight: 700; letter-spacing: -1px; }
        h2, h3 { color: #e5e7eb; }
        
        /* Botones */
        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(34, 211, 238, 0.3);
        }
        
        /* INPUTS NORMALES */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input,
        .stPasswordInput > div > div > input {
            border-radius: 8px !important;
            border: 2px solid #475569 !important;
            background: #334155 !important;
            color: #e5e7eb !important;
        }
        
        /* === FIX VISIBILIDAD INPUTS DESHABILITADOS (PERFIL) === */
        .stTextInput > div > div > input:disabled {
            background-color: #1e293b !important;
            color: #ffffff !important; /* Texto blanco brillante */
            -webkit-text-fill-color: #ffffff !important; /* Fix para navegadores Webkit */
            opacity: 1 !important; /* Evitar transparencia */
            border-color: #334155 !important;
            font-weight: 500 !important;
        }
        
        hr { border-color: #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Configuración de la API
API_URL = "http://backend:8000"

def header_section(title, icon, subtitle):
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='display: flex; align-items: center; gap: 1rem; color: #22d3ee;'>
            {icon} {title}
        </h1>
        <p style='color: #94a3b8; font-size: 1rem; margin-top: 0.5rem;'>{subtitle}</p>
        <div style='height: 2px; background: linear-gradient(90deg, #22d3ee, transparent); margin-top: 1rem;'></div>
    </div>
    """, unsafe_allow_html=True)

# --- CALLBACKS (PARA SOLUCIONAR EL DOBLE CLIC) ---
# Estas funciones se ejecutan ANTES de recargar la página.

def callback_reservar(clase_id, headers):
    try:
        resp = requests.post(f"{API_URL}/reservas", json={"clase_id": clase_id}, headers=headers)
        if resp.status_code == 201:
            st.toast("✅ Reserva confirmada correctamente", icon="🎉")
        else:
            msg = resp.json().get('detail', 'Error desconocido')
            st.toast(f"❌ {msg}", icon="⚠️")
    except:
        st.toast("❌ Error de conexión", icon="🔥")

def callback_cancelar(clase_id, headers):
    try:
        resp = requests.delete(f"{API_URL}/reservas/{clase_id}", headers=headers)
        if resp.status_code == 200:
            st.toast("🗑️ Reserva cancelada", icon="✅")
        else:
            st.toast("❌ Error al cancelar", icon="⚠️")
    except:
        st.toast("❌ Error de conexión", icon="🔥")

def callback_asignar_rutina(rutina_id, headers):
    try:
        resp = requests.post(f"{API_URL}/rutinas/{rutina_id}/asignar", headers=headers)
        if resp.status_code == 200:
            st.toast("💪 Rutina asignada a tu plan", icon="🔥")
        else:
            st.toast("❌ Error al asignar", icon="⚠️")
    except:
        st.toast("❌ Error de conexión", icon="🔥")

def callback_simular_iot(headers):
    try:
        # Simulamos un dispositivo llamado "pulsera-web"
        resp = requests.post(f"{API_URL}/iot/sincronizar/pulsera-web", headers=headers)
        
        if resp.status_code == 200:
            datos = resp.json().get("datos_recibidos", {})
            st.toast(f"⌚ Datos recibidos: {datos.get('pulsaciones', 0)} bpm, {datos.get('calorias', 0)} kcal", icon="📡") 
            
        else:
            msg = resp.json().get('detail', 'Error desconocido del servidor')
            st.toast(f"❌ Error sincronizando: {msg}", icon="⚠️")
            
    except requests.exceptions.ConnectionError:
        # Esto captura la desconexión dentro del contenedor Docker
        st.toast("❌ Error de conexión con el Backend (Docker). Inténtalo de nuevo.", icon="🔥")
    except Exception as e:
        # Esto captura cualquier otro error de procesamiento (ej: JSON inválido)
        st.toast(f"❌ Error inesperado: {e}", icon="⚠️")

# --- SISTEMA DE AUTENTICACIÓN ---
def auth_system():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse"])
        
        # LOGIN
        with tab_login:
            with st.container(border=True):
                st.markdown("<h3 style='text-align: center;'>Bienvenido de nuevo</h3>", unsafe_allow_html=True)
                email = st.text_input("Email", key="login_email", placeholder="usuario@ejemplo.com")
                password = st.text_input("Contraseña", type="password", key="login_pass", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Entrar 🚀", type="primary", key="btn_login"):
                    with st.spinner("Verificando..."):
                        try:
                            response = requests.post(f"{API_URL}/token", data={"username": email, "password": password})
                            if response.status_code == 200:
                                st.session_state['token'] = response.json()['access_token']
                                st.toast("¡Conexión exitosa!", icon="✅")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("Credenciales incorrectas")
                        except requests.exceptions.ConnectionError:
                            st.error("❌ No se puede conectar con el Backend")

        # REGISTRO
        with tab_register:
            with st.container(border=True):
                st.markdown("<h3 style='text-align: center;'>Únete al Gimnasio</h3>", unsafe_allow_html=True)
                reg_nombre = st.text_input("Nombre Completo", placeholder="Ej: Álvaro Pérez")
                reg_email = st.text_input("Email", key="reg_email", placeholder="tu@email.com")
                reg_pass = st.text_input("Contraseña", type="password", key="reg_pass")
                
                c1, c2 = st.columns(2)
                with c1:
                    reg_fecha = st.date_input("Fecha de Nacimiento", 
                                            min_value=date(1950, 1, 1), 
                                            max_value=date(2010, 12, 31),
                                            value=date(2000, 1, 1))
                with c2:
                    reg_nivel = st.selectbox("Nivel", ["principiante", "intermedio", "avanzado"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Crear Cuenta ✨", type="primary", key="btn_register"):
                    if not reg_nombre or not reg_email or not reg_pass:
                        st.warning("Por favor, rellena todos los campos obligatorios.")
                    else:
                        with st.spinner("Creando tu perfil..."):
                            payload = {
                                "nombre": reg_nombre,
                                "email": reg_email,
                                "fecha_nacimiento": str(reg_fecha),
                                "nivel": reg_nivel,
                                "password": reg_pass
                            }
                            try:
                                res = requests.post(f"{API_URL}/socios", json=payload)
                                if res.status_code == 201:
                                    st.success("¡Cuenta creada con éxito! Ahora puedes iniciar sesión.")
                                    st.balloons()
                                else:
                                    error_msg = res.json().get('detail', 'Error desconocido')
                                    st.error(f"Error: {error_msg}")
                            except Exception as e:
                                st.error(f"Error de conexión: {e}")

# --- MÓDULOS DE LA APP ---

def render_perfil(headers):
    header_section("Mi Perfil", "👤", "Gestiona tu información personal y membresía")
    
    try:
        res = requests.get(f"{API_URL}/socios/me", headers=headers)
        if res.status_code == 200:
            user = res.json()
            
            with st.container(border=True):
                col_avatar, col_info = st.columns([1, 3])
                with col_avatar:
                    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=120)
                
                with col_info:
                    st.markdown(f"### Hola, {user['nombre']} 👋")
                    st.caption(f"ID Socio: `{user['id']}`")
                    st.markdown("---")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Nivel", user['nivel'].upper(), "⭐")
                    m2.metric("Puntos", "1,250", "🏆")
                    m3.metric("Estado", "Activo", "🟢")
            
            st.markdown("### 📋 Información de Cuenta")
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.text_input("Nombre Completo", value=user['nombre'], disabled=True)
                st.text_input("Email Registrado", value=user['email'], disabled=True)
            
            with col_right:
                st.text_input("Membresía", value="Premium Mensual", disabled=True)
                st.text_input("Fecha Nacimiento", value=user.get('fecha_nacimiento', 'No consta'), disabled=True)
            
            st.markdown("---")
            
            # --- BOTONES DE ACCIÓN (Corregido: Sin duplicados) ---
            c_acceso, c_logout = st.columns([1, 1])
            
            with c_acceso:
                # Simula pasar el torno
                if st.button("📲 Simular Entrada (QR)", type="primary"):
                    try:
                        resp = requests.post(f"{API_URL}/accesos", headers=headers)
                        if resp.status_code == 200:
                            detalle = resp.json().get('detalle', 'Acceso OK')
                            st.toast(f"✅ {detalle}", icon="🚪")
                            time.sleep(1)
                        else:
                            st.error("Error al registrar acceso")
                    except:
                        st.error("Error de conexión")
            
            with c_logout:
                # Botón de Logout con KEY ÚNICA para evitar conflictos
                if st.button("🚪 Cerrar Sesión", type="secondary", key="btn_logout_perfil"):
                    st.session_state.clear()
                    st.rerun()
                    
        else:
            st.error("❌ Tu sesión ha expirado. Por favor, entra de nuevo.")
            st.session_state.clear()
            time.sleep(2)
            st.rerun()
    except requests.exceptions.ConnectionError:
        st.error("❌ No hay conexión con el servidor.")

def render_clases(headers):
    header_section("Clases y Reservas", "📅", "Reserva tu plaza en las mejores sesiones")
    
    try:
        res = requests.get(f"{API_URL}/clases")
        if res.status_code == 200:
            clases = res.json()
            if not clases:
                st.info("No hay clases disponibles en este momento.")
            else:
                cols = st.columns(2)
                for i, clase in enumerate(clases):
                    with cols[i % 2]:
                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"### 🏃 {clase['nombre']}")
                            with col2:
                                st.markdown(f"<span style='color: #22d3ee; font-weight: bold;'>{clase['horario']}</span>", unsafe_allow_html=True)
                            
                            st.markdown("---")
                            plazas_totales = clase['aforo']
                            # Usamos .get para evitar errores si el campo no llega
                            libres = clase.get('plazas_disponibles', 0)
                            ocupadas = plazas_totales - libres
                            ocupacion = ocupadas / plazas_totales if plazas_totales > 0 else 0
                            st.progress(ocupacion)
                            
                            c_info1, c_info2 = st.columns(2)
                            c_info1.metric("Libres", libres)
                            c_info2.metric("Aforo", plazas_totales)
                            
                            col_btn_res, col_btn_can = st.columns(2)
                            with col_btn_res:
                                # USAMOS CALLBACK PARA EVITAR DOBLE CLIC
                                st.button(
                                    "Reservar", 
                                    key=f"res_{clase['id']}", 
                                    type="primary",
                                    on_click=callback_reservar,
                                    args=(clase['id'], headers)
                                )
                            with col_btn_can:
                                st.button(
                                    "Cancelar", 
                                    key=f"can_{clase['id']}", 
                                    type="secondary",
                                    on_click=callback_cancelar,
                                    args=(clase['id'], headers)
                                )
        else:
            st.error("Error de conexión con el servicio de clases.")
    except:
        st.error("Error al cargar clases.")

def render_rutinas(headers):
    header_section("Rutinas", "💪", "Planes de entrenamiento personalizados")
    
    # Creamos dos pestañas para organizar mejor la vista
    tab_catalogo, tab_mis_rutinas = st.tabs(["📚 Catálogo Completo", "👤 Mis Rutinas"])
    
    # --- PESTAÑA 1: CATÁLOGO (Lo que ya tenías) ---
    with tab_catalogo:
        try:
            res = requests.get(f"{API_URL}/rutinas")
            if res.status_code == 200:
                rutinas = res.json()
                if not rutinas:
                    st.warning("No hay rutinas disponibles en el sistema.")
                else:
                    st.info("Explora y añade nuevas rutinas a tu plan.")
                    for rut in rutinas:
                        with st.expander(f"🏋️ {rut['nombre']} ({rut['dificultad']})"):
                            c1, c2 = st.columns([3, 1])
                            c1.write(f"⏱️ **{rut['duracion']} min**")
                            # Botón de asignar
                            c2.button("Asignar", key=f"cat_{rut['id']}", 
                                      on_click=callback_asignar_rutina, args=(rut['id'], headers))
            else:
                st.error("Error cargando el catálogo.")
        except:
            st.error("Error de conexión.")

    # --- PESTAÑA 2: MIS RUTINAS (¡NUEVO!) ---
    with tab_mis_rutinas:
        try:
            # Llamamos al nuevo endpoint que acabamos de crear
            res = requests.get(f"{API_URL}/rutinas/me", headers=headers)
            if res.status_code == 200:
                mis_rutinas = res.json()
                if not mis_rutinas:
                    st.info("Aún no te has asignado ninguna rutina. ¡Ve al catálogo y elige una!")
                else:
                    st.success(f"Tienes {len(mis_rutinas)} rutinas activas en tu plan.")
                    for rut in mis_rutinas:
                        # Mostramos las rutinas del usuario con un diseño diferente (tarjeta verde)
                        with st.container(border=True):
                            col_a, col_b = st.columns([3, 1])
                            col_a.markdown(f"### ✅ {rut['nombre']}")
                            col_a.caption(f"Nivel: {rut['dificultad'].upper()} | Duración: {rut['duracion']} min")
                            
                            # Botón decorativo "Iniciar" (Simulado)
                            if col_b.button("Empezar", key=f"start_{rut['id']}"):
                                st.toast(f"¡A darle duro a {rut['nombre']}!", icon="🔥")
            else:
                st.error("No se pudieron cargar tus rutinas.")
        except:
            st.error("Error conectando con tus datos.")
            
def render_iot(headers):
    header_section("IoT & Progreso", "⌚", "Monitorización en tiempo real")
    
    # --- BOTÓN DE SIMULACIÓN DE ACTIVIDAD (NUEVO) ---
    col_sim, col_info = st.columns([1, 2])
    with col_sim:
        st.markdown("##### 📡 Simulador")
        st.button(
            "🔄 Simular Actividad", 
            type="primary", 
            help="Genera datos falsos como si llevaras la pulsera",
            on_click=callback_simular_iot, 
            args=(headers,)
        )
    with col_info:
        st.info("Pulsa el botón para simular que tu pulsera envía datos nuevos al sistema.")
    st.markdown("---")
    # ------------------------------------------------

    try:
        res = requests.get(f"{API_URL}/progreso", headers=headers)
        if res.status_code == 200:
            historial = res.json()
        else:
            historial = []
    except:
        historial = []

    if not historial:
        st.info("⚠️ No hay datos registrados. ¡Usa el botón de simular arriba!")
        data = pd.DataFrame(columns=['fecha', 'peso', 'tiempo'])
        ultimo_peso = 0
        ultimo_tiempo = 0
        total_sesiones = 0
    else:
        data = pd.DataFrame(historial)
        data['fecha'] = pd.to_datetime(data['fecha']).dt.strftime('%H:%M %d/%m')
        ultimo_peso = data.iloc[-1]['peso']
        ultimo_tiempo = data.iloc[-1]['tiempo']
        total_sesiones = len(data)

    k1, k2, k3 = st.columns(3)
    k1.metric("🏋️ Último Peso", f"{ultimo_peso} Kg")
    k2.metric("⏱️ Tiempo Ejercicio", f"{ultimo_tiempo} min")
    k3.metric("📅 Total Sesiones", total_sesiones)
    
    st.markdown("### 📈 Tu Evolución")
    
    if not data.empty:
        chart = alt.Chart(data).mark_area(
            line={'color':'#22d3ee'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#22d3ee', offset=0),
                       alt.GradientStop(color='rgba(34, 211, 238, 0)', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x=alt.X('fecha', title='Sesión'),
            y=alt.Y('peso', title='Peso Levantado (Kg)'),
            tooltip=['fecha', 'peso', 'tiempo']
        ).properties(height=350, width='container').interactive()
        
        st.altair_chart(chart, use_container_width=True)
        
        with st.expander("Ver datos brutos"):
            st.dataframe(data, use_container_width=True)

# --- MAIN APP ---
def main():
    if 'token' not in st.session_state:
        auth_system()
        return

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #22d3ee;'>🏋️ Smart Gym</h2>", unsafe_allow_html=True)
        st.markdown("---")
        menu = st.radio("Navegación", ["Mi Perfil", "Clases", "Rutinas", "IoT & Progreso"])
        st.markdown("---")
        
        if st.button("Cerrar Sesión", key="logout_sidebar"):
            st.session_state.clear()
            st.rerun()

    if menu == "Mi Perfil":
        render_perfil(headers)
    elif menu == "Clases":
        render_clases(headers)
    elif menu == "Rutinas":
        render_rutinas(headers)
    elif menu == "IoT & Progreso":
        render_iot(headers)

if __name__ == "__main__":
    main()