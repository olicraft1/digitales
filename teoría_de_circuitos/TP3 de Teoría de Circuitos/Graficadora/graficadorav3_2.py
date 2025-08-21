import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# PARÁMETROS CONFIGURABLES POR EL USUARIO
# -------------------------------------------------------------------

# --- Parámetros Generales del Circuito ---
Vf = 22.0      # Tensión de la fuente de carga (en Voltios)
Vi = 0.0       # Tensión inicial del capacitor al empezar el ciclo (en Voltios)
C = 56/1000000     # Capacitancia (en Faradios, ej: 100uF = 0.0001)

# --- Parámetros de la FASE DE CARGA ---
R_carga = 4700.0  # Resistencia de carga (en Ohmios, ej: 10k = 10000)

# --- Parámetros de la FASE DE DESCARGA ---
R_descarga = 4700.0 # Resistencia de descarga (en Ohmios, ej: 5k = 5000)

# --- Parámetro de Transición ---
t_cambio = 1.0 # Tiempo en segundos en el que el circuito cambia de carga a descarga

# -------------------------------------------------------------------
# CÁLCULOS DEL CICLO COMPLETO
# -------------------------------------------------------------------

# 1. Constantes de tiempo para cada fase
T_carga = R_carga * C
T_descarga = R_descarga * C

# 2. Crear un eje de tiempo total
# El tiempo total cubrirá la carga (hasta t_cambio) y una descarga completa (5*T_descarga)
t_final = t_cambio + 5 * T_descarga
t = np.linspace(0, t_final, 1500) # Usamos más puntos para una curva suave

# 3. Calcular la condición inicial para la descarga
# El voltaje inicial de la descarga es el voltaje final de la carga en t_cambio.
V_descarga_inicial = Vf + (Vi - Vf) * np.exp(-t_cambio / T_carga)

# 4. Calcular el voltaje (vc) para todo el ciclo usando np.where
# Sintaxis: np.where(condición, valor_si_es_cierto, valor_si_es_falso)
# Fase de carga (t <= t_cambio)
vc_fase_carga = Vf + (Vi - Vf) * np.exp(-t / T_carga)
# Fase de descarga (t > t_cambio), el tiempo se desplaza a (t - t_cambio)
vc_fase_descarga = V_descarga_inicial * np.exp(-(t - t_cambio) / T_descarga)

vc_total = np.where(t <= t_cambio, vc_fase_carga, vc_fase_descarga)

# 5. Calcular la corriente (ic) para todo el ciclo
# Fase de carga
ic_fase_carga = ((Vf - Vi) / R_carga) * np.exp(-t / T_carga)
# Fase de descarga
ic_fase_descarga = -(V_descarga_inicial / R_descarga) * np.exp(-(t - t_cambio) / T_descarga)

ic_total = np.where(t <= t_cambio, ic_fase_carga, ic_fase_descarga)


# -------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS (EN VENTANAS SEPARADAS)
# -------------------------------------------------------------------

# --- Ventana 1: Gráfico de Tensión ---
fig_vc, ax_vc = plt.subplots(figsize=(12, 6))
fig_vc.canvas.manager.set_window_title('Ciclo Completo de Tensión (vc)')

ax_vc.plot(t, vc_total, 'b-', label='Tensión en el Capacitor (vc)')
ax_vc.set_title('Ciclo de Carga y Descarga del Capacitor - Tensión')
ax_vc.set_xlabel('Tiempo (s)')
ax_vc.set_ylabel('Tensión (V)')
ax_vc.grid(True)
ax_vc.set_ylim(bottom=0) # El voltaje del capacitor no será negativo
ax_vc.set_xlim(left=0)

# Añadir una línea vertical para marcar el cambio de estado
ax_vc.axvline(x=t_cambio, color='grey', linestyle='--', label=f'Cambio a descarga (t={t_cambio}s)')
ax_vc.legend()
fig_vc.tight_layout()


# --- Ventana 2: Gráfico de Corriente ---
fig_ic, ax_ic = plt.subplots(figsize=(12, 6))
fig_ic.canvas.manager.set_window_title('Ciclo Completo de Corriente (ic)')

ax_ic.plot(t, ic_total, 'r-', label='Corriente en el Capacitor (ic)')
ax_ic.set_title('Ciclo de Carga y Descarga del Capacitor - Corriente')
ax_ic.set_xlabel('Tiempo (s)')
ax_ic.set_ylabel('Corriente (A)')
ax_ic.grid(True)
ax_ic.set_xlim(left=0)

# Añadir una línea horizontal en y=0 para mejor referencia
ax_ic.axhline(y=0, color='black', linewidth=0.5)
# Añadir la línea vertical del cambio de estado
ax_ic.axvline(x=t_cambio, color='grey', linestyle='--', label=f'Cambio a descarga (t={t_cambio}s)')
ax_ic.legend()
fig_ic.tight_layout()

# Mostrar ambas ventanas
plt.show()