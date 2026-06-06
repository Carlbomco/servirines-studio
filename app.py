import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración inicial de la página de Streamlit
st.set_page_config(page_title="Servirines Studio", page_icon="🚗", layout="wide")

st.title("🚗 Servirines Studio - Sistema de Gestión")
st.markdown("Registre y consulte las operaciones diarias de todas las sedes en tiempo real.")

# 1. Establecer la conexión con Google Sheets mediante Secrets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error al establecer la conexión con Google Sheets: {e}")
    st.stop()

# Función optimizada con caché para leer datos sin sobrecargar la API
@st.cache_data(ttl=60)  # Los datos se refrescan automáticamente cada 60 segundos
def load_data(sheet_name):
    return conn.read(worksheet=sheet_name)

# Cargar los datos de las tres pestañas estructurales
try:
    df_sedes = load_data("Sedes")
    df_ventas = load_data("Ventas")
    df_bitacora = load_data("Bitacora")
except Exception as e:
    st.error(f"Error al leer las pestañas. Asegúrate de que los nombres en Google Sheets sean exactamente 'Sedes', 'Ventas' y 'Bitacora'. Detalle: {e}")
    st.stop()

# Crear pestañas de navegación en la interfaz de usuario
tab_registro, tab_bitacora_ui, tab_visualizacion = st.tabs(["📝 Registrar Venta", "📓 Bitácora Diaria", "📊 Visualizar Tablas"])

# =========================================================================
# PESTAÑA 1: REGISTRO DE VENTAS
# =========================================================================
with tab_registro:
    st.header("Formulario de Registro de Ventas")
    
    with st.form("form_venta", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Dropdown dinámico alimentado por la pestaña 'Sedes'
            opciones_sedes = df_sedes["Sede"].unique() if not df_sedes.empty else ["No hay sedes disponibles"]
            sede_sel = st.selectbox("Sede *", options=opciones_sedes)
            asesor = st.text_input("Nombre del Asesor *")
            tecnico = st.text_input("Nombre del Técnico *")
            placa = st.text_input("Placa del Vehículo * (Ej: ABC123)").upper()
            marca_vehiculo = st.text_input("Marca del Vehículo")
            modelo_vehiculo = st.text_input("Modelo (Año)")
        
        with col2:
            fecha_venta = st.date_input("Fecha de Operación", value=datetime.today())
            factura = st.text_input("Número Factura Servirines")
            valor_total = st.number_input("Valor Total Facturado ($)", min_value=0, step=5000)
            orden_sede = st.text_input("Orden de Trabajo de la Sede")
        
        st.markdown("<small>* Campos obligatorios</small>", unsafe_allow_html=True)
        submit_venta = st.form_submit_button("Guardar Registro de Venta")
        
        if submit_venta:
            if not asesor or not tecnico or not placa or sede_sel == "No hay sedes disponibles":
                st.error("Por favor completa los campos obligatorios (Sede, Asesor, Técnico y Placa).")
            else:
                # Crear la fila de datos respetando exactamente la estructura de columnas del archivo base
                nueva_venta = pd.DataFrame([{
                    "Marca_Temporal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Sede": sede_sel,
                    "Asesor": asesor,
                    "Tecnico": tecnico,
                    "Placa": placa,
                    "Marca": marca_vehiculo,
                    "Modelo": modelo_vehiculo,
                    "Fecha": fecha_venta.strftime("%Y-%m-%d"),
                    "Factura_Servirines": factura,
                    "Valor_Total": valor_total,
                    "Orden_Trabajo_Sede": orden_sede,
                    "Año": int(fecha_venta.year),
                    "Mes": int(fecha_venta.month)
                }])
                
                # Concatenar el registro nuevo al DataFrame existente
                df_ventas_actualizado = pd.concat([df_ventas, nueva_venta], ignore_index=True)
                
                try:
                    # Enviar los datos actualizados a la nube de Google
                    conn.update(worksheet="Ventas", data=df_ventas_actualizado)
                    st.success(f"¡Venta del vehículo con placas {placa} registrada exitosamente!")
                    st.cache_data.clear()  # Limpiar caché para forzar la actualización visual
                except Exception as e:
                    st.error(f"Error al escribir en Google Sheets: {e}")

# =========================================================================
# PESTAÑA 2: BITÁCORA DIARIA
# =========================================================================
with tab_bitacora_ui:
    st.header("Novedades y Entradas de Bitácora")
    
    with st.form("form_bitacora", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha_bitacora = st.date_input("Fecha del Reporte", value=datetime.today())
            sede_bitacora = st.selectbox("Sede Reportada", options=df_sedes["Sede"].unique() if not df_sedes.empty else ["No hay sedes"])
            vehiculos_ingresados = st.number_input("Total Vehículos Ingresados", min_value=0, step=1)
            rines_no_autorizados = st.number_input("Cantidad de Rines No Autorizados", min_value=0, step=1)
        
        with col2:
            placas_no_autorizadas = st.text_input("Placas No Autorizadas (Sepárelas por comas)")
            marca_bitacora = st.text_input("Observaciones / Marcas Predominantes")
            estado_seguimiento = st.selectbox("Estado de Seguimiento", ["Pendiente", "En Revisión", "Finalizado"])
            
        submit_bitacora = st.form_submit_button("Guardar en Bitácora")
        
        if submit_bitacora:
            # Estructurar datos para la pestaña de bitácora
            nuevo_log = pd.DataFrame([{
                "Fecha": fecha_bitacora.strftime("%Y-%m-%d"),
                "Sede": sede_bitacora,
                "Vehiculos_Ingresados": int(vehiculos_ingresados),
                "Rines_No_Autorizados": int(rines_no_autorizados),
                "Placas_No_Autorizadas": placas_no_autorizadas,
                "Marca": marca_bitacora,
                "Estado_Seguimiento": estado_seguimiento
            }])
            
            df_bitacora_actualizado = pd.concat([df_bitacora, nuevo_log], ignore_index=True)
            
            try:
                conn.update(worksheet="Bitacora", data=df_bitacora_actualizado)
                st.success("¡Bitácora diaria actualizada correctamente!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Error al guardar en la bitácora: {e}")

# =========================================================================
# PESTAÑA 3: VISUALIZACIÓN DE TABLAS
# =========================================================================
with tab_visualizacion:
    st.header("Monitoreo de Datos Almacenados")
    
    st.subheader("📋 Últimos 10 Registros de Ventas")
    if not df_ventas.empty:
        st.dataframe(df_ventas.tail(10), use_container_width=True)
    else:
        st.info("La pestaña de Ventas está vacía actualmente.")
        
    st.subheader("📓 Últimos 10 Registros en Bitácora")
    if not df_bitacora.empty:
        st.dataframe(df_bitacora.tail(10), use_container_width=True)
    else:
        st.info("La pestaña de Bitácora está vacía actualmente.")
        
    st.subheader("🏢 Estructura de Sedes Registradas")
    st.dataframe(df_sedes, use_container_width=True)
