import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración premium de la interfaz de usuario
st.set_page_config(
    page_title="Servirines Professional Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ARQUITECTURA DE DISEÑO CORPORATIVO AVANZADO (CSS PERSONALIZADO)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }
    
    /* Títulos y Encabezados */
    .studio-title {
        font-size: 32px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.75px;
        margin-bottom: 4px;
    }
    .studio-subtitle {
        font-size: 15px;
        color: #64748B;
        margin-bottom: 28px;
    }
    
    /* Tarjetas FinTech para impedir el clipping/truncado de datos */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        margin: 0 0 6px 0;
    }
    .metric-value {
        font-size: 25px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
        margin: 0;
        white-space: nowrap;
    }
    .metric-footer {
        font-size: 12px;
        font-weight: 500;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Contenedores de Clientes CRM */
    .crm-card {
        background: #FFFFFF;
        border-left: 5px solid #EF4444;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 0 12px 12px 0;
        padding: 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.01);
    }
    
    /* Estilización de Inputs nativos para verse modernos */
    div[data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.02) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MA VADEMÉCUM AUTOMOTRIZ: BASE DE DATOS FILTRADA DE MARCAS Y MODELOS
# -----------------------------------------------------------------------------
CATALOGO_AUTOMOTRIZ = {
    "Mercedes Benz": ["Clase A", "Clase C", "Clase E", "CLA Coupe", "GLA SUV", "GLB SUV", "GLC SUV", "GLE SUV", "Clase G", "AMG A35"],
    "BMW": ["Serie 1", "Serie 3 (320i)", "Serie 4", "Serie 5", "X1", "X3", "X4", "X5", "X6", "iX3 (Eléctrico)"],
    "Audi": ["A3 Sedan", "A4 Sedan", "A6 Sedan", "Q2", "Q3 Sportback", "Q5 SUV", "Q7", "Q8", "e-tron GT"],
    "BYD": ["Seagull", "Dolphin", "Yuan Plus", "Song Plus DM-i", "Seal", "Han EV", "Tang EV"],
    "Ford": ["Fiesta", "EcoSport", "Escape Hybrid", "Edge", "Explorer", "Ranger", "F-150 Lariat", "Mustang Mach-E"],
    "Toyota": ["Yaris", "Corolla Cross", "Rav4", "4Runner", "Fortuner SW4", "Land Cruiser Prado", "Land Cruiser 300", "Hilux"],
    "Volkswagen": ["Polo", "Virtus", "Nivus", "T-Cross", "Taos", "Tiguan", "Teramont", "Amarok"],
    "Renault": ["Kwid", "Sandero Stepway", "Logan", "Duster", "Oroch", "Captur", "Koleos", "Kardian"],
    "Mazda": ["Mazda 2", "Mazda 3", "CX-30", "CX-5", "CX-50", "CX-60", "CX-90"]
}

# -----------------------------------------------------------------------------
# PERSISTENCIA DE DATOS CON LOS CAMPOS EXACTOS DE TUS EXCELS
# -----------------------------------------------------------------------------
if 'db_initialized' not in st.session_state:
    st.session_state.sedes = pd.DataFrame([
        {"Sede": "M&M Morato", "Ciudad": "Bogotá", "Meta_Dinero": 60000000},
        {"Sede": "M&M Cll 183", "Ciudad": "Bogotá", "Meta_Dinero": 60000000},
        {"Sede": "M&M Chia", "Ciudad": "Chía", "Meta_Dinero": 60000000},
        {"Sede": "M&M Pereira", "Ciudad": "Pereira", "Meta_Dinero": 60000000},
        {"Sede": "Autoniza Starniza", "Ciudad": "Bogotá", "Meta_Dinero": 60000000},
        {"Sede": "Autoniza Ford", "Ciudad": "Bogotá", "Meta_Dinero": 50000000},
        {"Sede": "Llanogrande", "Ciudad": "Rionegro", "Meta_Dinero": 40000000},
        {"Sede": "Arigri", "Ciudad": "Medellín", "Meta_Dinero": 30000000}
    ])
    
    # Datos iniciales mapeando de manera exhaustiva las 20 columnas reales identificadas
    st.session_state.ventas = pd.DataFrame([
        {
            "Marca_Temporal": "2026-06-01 10:15:22", "Sede": "M&M Pereira", "Asesor": "Juan Esteban", "Tecnico": "Andrés Cabrera",
            "Placa": "PER123", "Marca": "Mercedes Benz", "Modelo": "GLC SUV", "Fecha": "2026-06-01", 
            "Factura_Servirines": "10425", "Valor_Total": 1450000, "Orden_Trabajo_Sede": "MM-8541", "Año": 2026, "Mes": 6,
            "Qty_Combo": 1, "Qty_Alineacion": 1, "Qty_Balanceo": 1, "Qty_Matrizado": 2, "Qty_Diamantado": 2, "Qty_Pintura": 0, "Qty_TPMS": 0
        },
        {
            "Marca_Temporal": "2026-06-02 16:44:11", "Sede": "Autoniza Starniza", "Asesor": "Alejandro Díaz", "Tecnico": "Santiago Trujillo",
            "Placa": "FIQ664", "Marca": "BMW", "Modelo": "X3", "Fecha": "2026-06-02", 
            "Factura_Servirines": "10426", "Valor_Total": 650000, "Orden_Trabajo_Sede": "ST-9632", "Año": 2026, "Mes": 6,
            "Qty_Combo": 0, "Qty_Alineacion": 0, "Qty_Balanceo": 0, "Qty_Matrizado": 0, "Qty_Diamantado": 0, "Qty_Pintura": 2, "Qty_TPMS": 4
        }
    ])

    # Bitácora operativa de tráfico y prospección en piso
    st.session_state.bitacora = pd.DataFrame([
        {
            "Fecha": "2026-06-01", "Sede": "M&M Pereira", "Vehiculos_Ingresados": 3, "Combos_Autorizados": 1, 
            "Rines_Cotizados": 4, "Rines_Autorizados": 0, "Rines_No_Autorizados": 4, "Placas_No_Autorizadas": "PER123",
            "Marca": "Mercedes Benz", "Asesor": "Juan Esteban", "Estado_Seguimiento": "Pendiente", "Ultimo_Contacto": "N/A"
        },
        {
            "Fecha": "2026-06-02", "Sede": "Autoniza Starniza", "Vehiculos_Ingresados": 2, "Combos_Autorizados": 1, 
            "Rines_Cotizados": 4, "Rines_Autorizados": 0, "Rines_No_Autorizados": 4, "Placas_No_Autorizadas": "FIQ664",
            "Marca": "BMW", "Asesor": "Alejandro Díaz", "Estado_Seguimiento": "Contactado", "Ultimo_Contacto": "2026-06-04"
        }
    ])
    st.session_state.db_initialized = True

# -----------------------------------------------------------------------------
# MENÚ NAVEGACIÓN LATERAL PREMIUM
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
    <div style='padding: 10px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 20px;'>
        <h3 style='margin:0; color:#0F172A; font-weight:800; font-size:20px; letter-spacing:-0.5px;'>SERVIRINES</h3>
        <p style='margin:2px 0 0 0; color:#3B82F6; font-size:12px; font-weight:600; text-transform:uppercase;'>Studio Pro ERP</p>
    </div>
""", unsafe_allow_html=True)

modulo = st.sidebar.radio(
    "Navegación Principal",
    ["📊 Dashboard de Control", "📝 Registro Técnico Integral", "🎯 CRM de Recuperación Activa", "⚙️ Metas de Sede"]
)

# -----------------------------------------------------------------------------
# MÓDULO 1: DASHBOARD DE CONTROL (TARJETAS INDESTRUCTIBLES AL TAMAÑO)
# -----------------------------------------------------------------------------
if modulo == "📊 Dashboard de Control":
    st.markdown("<div class='studio-title'>Dashboard de Gestión de Operaciones</div>", unsafe_allow_html=True)
    st.markdown("<div class='studio-subtitle'>Monitoreo unificado de ingresos, efectividad de cierre en piso e indicadores comerciales.</div>", unsafe_allow_html=True)
    
    # Cálculos y agrupaciones directas de la base de datos interna
    facturacion_total = st.session_state.ventas["Valor_Total"].sum()
    meta_dinero_global = st.session_state.sedes["Meta_Dinero"].sum()
    cumplimiento_porcentaje = (facturacion_total / meta_dinero_global * 100) if meta_dinero_global > 0 else 0
    
    total_cotizados_rines = st.session_state.bitacora["Rines_Cotizados"].sum()
    total_autorizados_rines = st.session_state.bitacora["Rines_Autorizados"].sum()
    tasa_conversion = (total_autorizados_rines / total_cotizados_rines * 100) if total_cotizados_rines > 0 else 0
    
    # Implementación de las tarjetas HTML para evitar que los números se rompan
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class='metric-card'>
                <p class='metric-label'>Ventas Consolidadas</p>
                <h3 class='metric-value'>${facturacion_total:,.0f}</h3>
                <p class='metric-footer' style='color:#10B981;'>↑ Monitoreo en Vivo (COP)</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class='metric-card'>
                <p class='metric-label'>Meta Financiera</p>
                <h3 class='metric-value'>${meta_dinero_global:,.0f}</h3>
                <p class='metric-footer' style='color:#64748B;'>Presupuesto General</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class='metric-card'>
                <p class='metric-label'>% Cumplimiento Global</p>
                <h3 class='metric-value'>{cumplimiento_porcentaje:.2f}%</h3>
                <p class='metric-footer' style='color:#F59E0B;'>Meta esperada actual: 75%</p>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class='metric-card'>
                <p class='metric-label'>Conversión en Rines</p>
                <h3 class='metric-value'>{tasa_conversion:.1f}%</h3>
                <p class='metric-footer' style='color:#EF4444;'>Objetivo de Piso: >45%</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Sección gráfica avanzada
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.subheader("Desempeño Financiero Comercial vs Metas")
        ventas_sede = st.session_state.ventas.groupby("Sede")["Valor_Total"].sum().reset_index()
        chart_data = pd.merge(st.session_state.sedes, ventas_sede, on="Sede", how="left").fillna(0)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=chart_data["Sede"], y=chart_data["Meta_Dinero"], name="Presupuesto Asignado", marker_color='#E2E8F0', cliponaxis=False))
        fig.add_trace(go.Bar(x=chart_data["Sede"], y=chart_data["Valor_Total"], name="Venta Consolidada Real", marker_color='#2563EB', cliponaxis=False))
        fig.update_layout(barmode='group', height=330, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with g_col2:
        st.subheader("Pérdida Bruta de Oportunidad por Rines Caídos")
        total_caidos = st.session_state.bitacora["Rines_No_Autorizados"].sum()
        
        fig_funnel = go.Figure(go.Funnel(
            y = ["Rines Cotizados", "Rines Autorizados en Taller", "Rines Rechazados (Lead CRM)"],
            x = [total_cotizados_rines, total_autorizados_rines, total_caidos],
            textinfo = "value+percent initial",
            marker = {"color": ["#1E293B", "#10B981", "#EF4444"]}
        ))
        fig_funnel.update_layout(height=330, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_funnel, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 2: REGISTRO TÉCNICO INTEGRAL (REEMPLAZO COMPLETO DE EXCEL Y GOOGLE FORMS)
# -----------------------------------------------------------------------------
elif modulo == "📝 Registro Técnico Integral":
    st.markdown("<div class='studio-title'>Registro Unificado de Operaciones</div>", unsafe_allow_html=True)
    st.markdown("<div class='studio-subtitle'>Formulario único obligatorio para el ingreso de vehículos, desglose de facturas y control de rines.</div>", unsafe_allow_html=True)
    
    with st.form("registro_formulario_exhaustivo", clear_on_submit=True):
        st.markdown("<p style='color:#2563EB; font-weight:700; font-size:16px; margin-bottom:15px;'>1. Información Obligatoria de Taller y Vehículo</p>", unsafe_allow_html=True)
        
        row1_1, row1_2, row1_3 = st.columns(3)
        with row1_1:
            sede_f = st.selectbox("Sede Operativa *", st.session_state.sedes["Sede"].tolist())
            fecha_f = st.date_input("Fecha de Operación", datetime.now())
            placa_f = st.text_input("Placa del Vehículo *", placeholder="Ej: QWR787").upper()
        with row1_2:
            asesor_f = st.text_input("Asesor de Servicio *", placeholder="Ej: Alejandro Díaz")
            tecnico_f = st.text_input("Técnico Especialista asignado", placeholder="Ej: Santiago Trujillo")
            
            # --- ORDEN AMARRADO: SELECCIÓN DE MARCA PRIMERO ---
            marca_lista = list(CATALOGO_AUTOMOTRIZ.keys())
            marca_f = st.selectbox("Marca del Vehículo *", marca_lista)
        with row1_3:
            # --- FILTRADO DINÁMICO DE MODELOS BASADO EN LA MARCA SELECCIONADA ---
            modelos_disponibles = CATALOGO_AUTOMOTRIZ[marca_f]
            modelo_f = st.selectbox("Modelo del Vehículo *", modelos_disponibles)
            
            factura_f = st.text_input("Número Factura Servirines", placeholder="Ej: 10427")
            ot_f = st.text_input("Orden de Trabajo de Sede (Autoniza / M&M)", placeholder="Ej: AT-1124")

        st.markdown("<hr style='border-color:#E2E8F0; margin:25px 0;'/>", unsafe_allow_html=True)
        st.markdown("<p style='color:#2563EB; font-weight:700; font-size:16px; margin-bottom:15px;'>2. Control de Flujo de Entrada y Diagnóstico de Rines</p>", unsafe_allow_html=True)
        
        row2_1, row2_2, row2_3, row2_4 = st.columns(4)
        with row2_1:
            entradas_f = st.number_input("Vehículos Ingresados / Entradas", min_value=1, value=1)
        with row2_2:
            combos_f = st.number_input("Combos Alineación Balanceo Autorizados", min_value=0, value=0)
        with row2_3:
            cotizados_f = st.number_input("Rines Cotizados en Piso", min_value=0, value=0)
        with row2_4:
            autorizados_f = st.number_input("Rines Autorizados / Reparados", min_value=0, value=0)

        st.markdown("<hr style='border-color:#E2E8F0; margin:25px 0;'/>", unsafe_allow_html=True)
        st.markdown("<p style='color:#2563EB; font-weight:700; font-size:16px; margin-bottom:15px;'>3. Desglose de Servicios Concedidos (Cantidades)</p>", unsafe_allow_html=True)
        
        row3_1, row3_2, row3_3, row3_4 = st.columns(4)
        with row3_1:
            q_combo = st.number_input("Cant: Combo Alineación y Balanceo", min_value=0, value=0)
            q_alin = st.number_input("Cant: Alineación Individual", min_value=0, value=0)
        with row3_2:
            q_bal = st.number_input("Cant: Balanceo Individual", min_value=0, value=0)
            q_matrizado = st.number_input("Cant: Matrizado en Frío - Rectificación", min_value=0, value=0)
        with row3_3:
            q_diamante = st.number_input("Cant: Diamantado y Rectificación", min_value=0, value=0)
            q_pintura = st.number_input("Cant: Pintura y Rectificación", min_value=0, value=0)
        with row3_4:
            q_tpms = st.number_input("Cant: Instalación de Sensores TPMS", min_value=0, value=0)
            valor_total_f = st.number_input("Valor Facturado Total ($ COP) *", min_value=0, value=0, step=100000)

        st.markdown("<br/>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("⚡ Compilar y Validar Registro Operativo")
        
        if submit_button:
            if not placa_f or not asesor_f:
                st.error("❌ Error de Validación: Los campos Placa, Asesor y Datos de Vehículo son obligatorios para evitar la fragmentación del histórico.")
            else:
                rines_caidos_calc = max(0, cotizados_f - autorizados_f)
                dt_instance = datetime.combine(fecha_f, datetime.min.time())
                
                # Inyección directa a la tabla unificada de Ventas (20 campos consolidados)
                venta_data_row = {
                    "Marca_Temporal": str(datetime.now()), "Sede": sede_f, "Asesor": asesor_f, "Tecnico": tecnico_f,
                    "Placa": placa_f, "Marca": marca_f, "Modelo": modelo_f, "Fecha": str(fecha_f), 
                    "Factura_Servirines": factura_f, "Valor_Total": valor_total_f, "Orden_Trabajo_Sede": ot_f, 
                    "Año": dt_instance.year, "Mes": dt_instance.month, "Qty_Combo": q_combo, "Qty_Alineacion": q_alin, 
                    "Qty_Balanceo": q_bal, "Qty_Matrizado": q_matrizado, "Qty_Diamantado": q_diamante, 
                    "Qty_Pintura": q_pintura, "Qty_TPMS": q_tpms
                }
                st.session_state.ventas = pd.concat([st.session_state.ventas, pd.DataFrame([venta_data_row])], ignore_index=True)
                
                # Inyección directa a la Bitácora de Tráfico de Piso para alimentar el CRM
                bitacora_data_row = {
                    "Fecha": str(fecha_f), "Sede": sede_f, "Vehiculos_Ingresados": entradas_f, "Combos_Autorizados": combos_f, 
                    "Rines_Cotizados": cotizados_f, "Rines_Autorizados": autorizados_f, "Rines_No_Autorizados": rines_caidos_calc, 
                    "Placas_No_Autorizadas": placa_f, "Marca": marca_f, "Asesor": asesor_f, 
                    "Estado_Seguimiento": "Pendiente" if rines_caidos_calc > 0 else "N/A", "Ultimo_Contacto": "N/A"
                }
                st.session_state.bitacora = pd.concat([st.session_state.bitacora, pd.DataFrame([bitacora_data_row])], ignore_index=True)
                
                st.success(f"💾 Éxito: Datos consolidados para el vehículo {placa_f}. Se recalcularon las proyecciones de venta de la sede {sede_f}.")

# -----------------------------------------------------------------------------
# MÓDULO 3: CRM DE RECUPERACIÓN ACTIVA (REMARKETING SMART)
# -----------------------------------------------------------------------------
elif modulo == "🎯 CRM de Recuperación Activa":
    st.markdown("<div class='studio-title'>Centro de Recuperación de Ingresos</div>", unsafe_allow_html=True)
    st.markdown("<div class='studio-subtitle'>Segmentación de leads calientes basada en rines rechazados en piso. Incrementa la conversión de taller.</div>", unsafe_allow_html=True)
    
    leads = st.session_state.bitacora[st.session_state.bitacora["Rines_No_Autorizados"] > 0]
    
    if leads.empty:
        st.info("No se registran oportunidades de rines caídos pendientes por procesar.")
    else:
        st.markdown(f"Se localizan **{len(leads)} órdenes caídas** disponibles para remarketing inmediato:")
        
        for idx, row in leads.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class='crm-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <span style='background:#FEE2E2; color:#EF4444; font-size:11px; font-weight:700; padding:4px 8px; border-radius:6px;'>ALERTA DE DESVÍO</span>
                                <h4 style='margin:10px 0 4px 0; color:#0F172A; font-size:18px;'>Placa: <b>{row['Placas_No_Autorizadas']}</b> ({row['Marca']})</h4>
                                <p style='margin:0; font-size:13px; color:#64748B;'>Sede: {row['Sede']} | Registrado por Asesor: {row['Asesor']} | Fecha: {row['Fecha']}</p>
                            </div>
                            <div style='text-align:right;'>
                                <p style='margin:0; font-size:12px; color:#64748B; font-weight:600;'>RINES RECHAZADOS</p>
                                <h3 style='margin:2px 0 0 0; color:#EF4444; font-size:26px; font-weight:800;'>{row['Rines_No_Autorizados']} Uds</h3>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Texto comercial optimizado de alto impacto
                mensaje_comercial = (
                    f"Estimado usuario, le contactamos de Servirines {row['Sede']}. "
                    f"Recordamos el diagnóstico técnico de su vehículo {row['Marca']} de placa {row['Placas_No_Autorizadas']}. "
                    f"Durante la inspección evidenciamos que {row['Rines_No_Autorizados']} de sus rines presentan desviaciones de geometría (requieren rectificación urgente). "
                    f"Para cuidar la vida útil de sus llantas, le habilitamos un bono del 10% de descuento en mano de obra. ¿Le reservamos una cita de atención esta semana?"
                )
                
                col_c1, col_c2, col_c3 = st.columns([2, 2, 4])
                with col_c1:
                    estado_crm = st.selectbox(f"Acción CRM ({row['Placas_No_Autorizadas']})", ["Pendiente", "Contactado", "Vendido / Recuperado"], key=f"crm_opt_{idx}")
                with col_c2:
                    if st.button("💾 Registrar Gestión", key=f"crm_btn_{idx}"):
                        st.session_state.bitacora.at[idx, "Estado_Seguimiento"] = estado_crm
                        if estado_crm == "Contactado":
                            st.session_state.bitacora.at[idx, "Ultimo_Contacto"] = str(datetime.now().date())
                        st.rerun()
                with col_c3:
                    encoded_message = mensaje_comercial.replace(' ', '%20')
                    wa_link = f"https://web.whatsapp.com/send?text={encoded_message}"
                    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; width:100%; height:38px; border-radius:8px; font-weight:700; cursor:pointer;">💬 Lanzar WhatsApp Corporativo</button></a>', unsafe_allow_html=True)
                st.markdown("<br/>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 4: CONFIGURACIÓN GENERAL DE METAS DE SEDE
# -----------------------------------------------------------------------------
elif modulo == "⚙️ Metas de Sede":
    st.markdown("<div class='studio-title'>Configuración Global de Presupuestos</div>", unsafe_allow_html=True)
    st.markdown("<div class='studio-subtitle'>Ajuste y parametrización de las metas financieras mensuales por cada unidad de negocio establecida.</div>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns([3, 2])
    with col_v1:
        st.subheader("Tablero de Presupuestos Mensuales")
        st.dataframe(st.session_state.sedes, use_container_width=True, hide_index=True)
        
    with col_v2:
        st.subheader("Actualizar Parámetros Comerciales")
        with st.form("formulario_metas_config"):
            target_sede = st.selectbox("Seleccionar Sede a Modificar", st.session_state.sedes["Sede"].tolist())
            update_money = st.number_input("Nuevo Presupuesto Mensual ($ COP)", min_value=0, step=5000000, value=60000000)
            
            meta_submit = st.form_submit_button("🔄 Reconfigurar Valores de Sede")
            if meta_submit:
                idx_target = st.session_state.sedes[st.session_state.sedes["Sede"] == target_sede].index[0]
                st.session_state.sedes.at[idx_target, "Meta_Dinero"] = update_money
                st.success(f"Ajuste completado para {target_sede}. Valores sincronizados con el Dashboard Ejecutivo.")
                st.rerun()
