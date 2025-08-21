import numpy as np
import matplotlib.pyplot as plt
import sys

# -------------------------------------------------------------------
# PARÁMETROS CONFIGURABLES POR EL USUARIO
# -------------------------------------------------------------------

# --- Parámetros Generales del Circuito ---
Vf = 30.0      # Tensión de la fuente de carga (en Voltios)
Vi = 0.0       # Tensión inicial del capacitor al empezar el ciclo (en Voltios)
C = 2.0/1000000     # Capacitancia (en Faradios, ej: 100uF = 0.0001)

# --- Parámetros de la FASE DE CARGA ---
R_carga = 5000.0  # Resistencia de carga (en Ohmios, ej: 10k = 10000)

# --- Parámetros de la FASE DE DESCARGA ---
R_descarga = 2000.0 # Resistencia de descarga (en Ohmios, ej: 20k = 20000)

# --- Parámetros de Transición (TIEMPOS) ---
t_fin_carga = 0.1   # Tiempo en segundos para terminar la carga.
t_inicio_descarga = 0.2 # Tiempo en segundos para empezar la descarga.

# --- Validación de Tiempos ---
if t_fin_carga > t_inicio_descarga:
    print("Error: El tiempo de fin de carga no puede ser mayor que el tiempo de inicio de descarga.")
    sys.exit()

# -------------------------------------------------------------------
# CÁLCULOS DEL CICLO COMPLETO
# -------------------------------------------------------------------

T_carga = R_carga * C
T_descarga = R_descarga * C
t_final = t_inicio_descarga + 5 * T_descarga
t = np.linspace(0, t_final, 2000)

V_fin_carga = Vf + (Vi - Vf) * np.exp(-t_fin_carga / T_carga)

# --- Cálculo de Tensión en Capacitor (vc) ---
vc_fase_carga = Vf + (Vi - Vf) * np.exp(-t / T_carga)
vc_fase_descarga = V_fin_carga * np.exp(-(t - t_inicio_descarga) / T_descarga)
vc_total = np.where(t <= t_fin_carga, vc_fase_carga,
                    np.where(t <= t_inicio_descarga, V_fin_carga, vc_fase_descarga))

# --- Cálculo de Corriente (ic) ---
ic_fase_carga = ((Vf - Vi) / R_carga) * np.exp(-t / T_carga)
ic_fase_descarga = -(V_fin_carga / R_descarga) * np.exp(-(t - t_inicio_descarga) / T_descarga)
ic_total = np.where(t <= t_fin_carga, ic_fase_carga,
                    np.where(t <= t_inicio_descarga, 0.0, ic_fase_descarga))

# --- NUEVO: Cálculo de Tensión en Resistor (vr) ---
# Fase de Carga: Vr = R * I = (Vf - Vi) * exp(-t/T)
vr_fase_carga = (Vf - Vi) * np.exp(-t / T_carga)
# Fase de Flotación: I = 0, por lo tanto Vr = 0
vr_fase_float = 0.0
# Fase de Descarga: Vr = -Vc
vr_fase_descarga = -vc_fase_descarga # Usamos el vc_fase_descarga ya calculado
# Combinar las fases
vr_total = np.where(t <= t_fin_carga, vr_fase_carga,
                    np.where(t <= t_inicio_descarga, vr_fase_float, vr_fase_descarga))


# -------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS (3 VENTANAS SEPARADAS)
# -------------------------------------------------------------------

# --- Ventana 1: Gráfico de Tensión en Capacitor (vc) ---
fig_vc, ax_vc = plt.subplots(figsize=(12, 6))
fig_vc.canvas.manager.set_window_title('Ciclo Completo - Tensión en Capacitor (vc)')
ax_vc.plot(t, vc_total, 'b-', label='Tensión en Capacitor (vc)')
ax_vc.set_title('Tensión en Capacitor (vc)')
ax_vc.set_xlabel('Tiempo (s)'); ax_vc.set_ylabel('Tensión (V)')
ax_vc.grid(True); ax_vc.set_ylim(bottom=0, top=Vf * 1.1); ax_vc.set_xlim(left=0)
ax_vc.axvline(x=t_fin_carga, color='green', linestyle='--', label=f'Fin Carga (t={t_fin_carga}s)')
ax_vc.axvline(x=t_inicio_descarga, color='orange', linestyle='--', label=f'Inicio Descarga (t={t_inicio_descarga}s)')
ax_vc.legend(); fig_vc.tight_layout()

# --- Ventana 2: Gráfico de Corriente (ic) ---
fig_ic, ax_ic = plt.subplots(figsize=(12, 6))
fig_ic.canvas.manager.set_window_title('Ciclo Completo - Corriente (ic)')
ax_ic.plot(t, ic_total, 'r-', label='Corriente (ic)')
ax_ic.set_title('Corriente en el Circuito (ic)')
ax_ic.set_xlabel('Tiempo (s)'); ax_ic.set_ylabel('Corriente (A)')
ax_ic.grid(True); ax_ic.set_xlim(left=0)
ax_ic.axhline(y=0, color='black', linewidth=0.5)
ax_ic.axvline(x=t_fin_carga, color='green', linestyle='--', label=f'Fin Carga (t={t_fin_carga}s)')
ax_ic.axvline(x=t_inicio_descarga, color='orange', linestyle='--', label=f'Inicio Descarga (t={t_inicio_descarga}s)')
ax_ic.legend(); fig_ic.tight_layout()

# --- NUEVO: Ventana 3: Gráfico de Tensión en Resistor (vr) ---
fig_vr, ax_vr = plt.subplots(figsize=(12, 6))
fig_vr.canvas.manager.set_window_title('Ciclo Completo - Tensión en Resistor (vr)')
ax_vr.plot(t, vr_total, 'g-', label='Tensión en Resistor (vr)')
ax_vr.set_title('Tensión en Resistor (vr)')
ax_vr.set_xlabel('Tiempo (s)'); ax_vr.set_ylabel('Tensión (V)')
ax_vr.grid(True); ax_vr.set_xlim(left=0)

# Ajustar eje Y para que sea simétrico y muestre valores positivos y negativos
max_vr_abs = max(abs(vr_total.min()), abs(vr_total.max()))
ax_vr.set_ylim(-max_vr_abs * 1.1, max_vr_abs * 1.1)

ax_vr.axhline(y=0, color='black', linewidth=0.5)
ax_vr.axvline(x=t_fin_carga, color='green', linestyle='--', label=f'Fin Carga (t={t_fin_carga}s)')
ax_vr.axvline(x=t_inicio_descarga, color='orange', linestyle='--', label=f'Inicio Descarga (t={t_inicio_descarga}s)')
ax_vr.legend(); fig_vr.tight_layout()

# Mostrar las tres ventanas
plt.show()