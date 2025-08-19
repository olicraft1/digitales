import numpy as np
import matplotlib.pyplot as plt
import sys

# -------------------------------------------------------------------
# PARÁMETROS CONFIGURABLES POR EL USUARIO
# -------------------------------------------------------------------

# --- Parámetros Generales del Circuito ---
Vf = 12.0      # Tensión de la fuente de carga (en Voltios)
Vi = 0.0       # Tensión inicial del capacitor al empezar el ciclo (en Voltios)
C = 0.0001     # Capacitancia (en Faradios, ej: 100uF = 0.0001)

# --- Parámetros de la FASE DE CARGA ---
R_carga = 10000.0  # Resistencia de carga (en Ohmios, ej: 10k = 10000)

# --- Parámetros de la FASE DE DESCARGA ---
R_descarga = 20000.0 # Resistencia de descarga (en Ohmios, ej: 20k = 20000)

# --- Parámetros de Transición (TIEMPOS) ---
# 1. Fin de la carga: el capacitor queda en circuito abierto (flotando)
t_fin_carga = 1.5   # Tiempo en segundos para terminar la carga.
# 2. Inicio de la descarga: el capacitor se conecta a la resistencia de descarga.
t_inicio_descarga = 2.5 # Tiempo en segundos para empezar la descarga.

# --- Validación de Tiempos ---
if t_fin_carga > t_inicio_descarga:
    print("Error: El tiempo de fin de carga no puede ser mayor que el tiempo de inicio de descarga.")
    sys.exit() # Termina el script si los tiempos son ilógicos.


# -------------------------------------------------------------------
# CÁLCULOS DEL CICLO COMPLETO
# -------------------------------------------------------------------

# 1. Constantes de tiempo para cada fase activa
T_carga = R_carga * C
T_descarga = R_descarga * C

# 2. Crear un eje de tiempo total que abarque todo el proceso
t_final = t_inicio_descarga + 5 * T_descarga
t = np.linspace(0, t_final, 2000) # Más puntos para mayor precisión en las transiciones

# 3. Calcular el voltaje al final de la fase de carga. Este será el voltaje de flotación
# y la condición inicial para la descarga.
V_fin_carga = Vf + (Vi - Vf) * np.exp(-t_fin_carga / T_carga)

# 4. Calcular el VOLTAJE (vc) para las 3 fases usando np.where anidado
# Fase 1: Carga (t <= t_fin_carga)
vc_fase_carga = Vf + (Vi - Vf) * np.exp(-t / T_carga)
# Fase 2: Flotación (constante)
vc_fase_float = V_fin_carga
# Fase 3: Descarga (el tiempo se desplaza a (t - t_inicio_descarga))
vc_fase_descarga = V_fin_carga * np.exp(-(t - t_inicio_descarga) / T_descarga)

# Combinar las fases:
# si (t <= t_fin_carga), usa fórmula de carga,
# sino, si (t <= t_inicio_descarga), usa el valor constante de flotación,
# sino, usa la fórmula de descarga.
vc_total = np.where(t <= t_fin_carga, vc_fase_carga,
                    np.where(t <= t_inicio_descarga, vc_fase_float, vc_fase_descarga))

# 5. Calcular la CORRIENTE (ic) para las 3 fases
# Fase 1: Carga
ic_fase_carga = ((Vf - Vi) / R_carga) * np.exp(-t / T_carga)
# Fase 2: Flotación (corriente es CERO)
ic_fase_float = 0.0
# Fase 3: Descarga
ic_fase_descarga = -(V_fin_carga / R_descarga) * np.exp(-(t - t_inicio_descarga) / T_descarga)

# Combinar las fases con la misma lógica
ic_total = np.where(t <= t_fin_carga, ic_fase_carga,
                    np.where(t <= t_inicio_descarga, ic_fase_float, ic_fase_descarga))


# -------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS (EN VENTANAS SEPARADAS)
# -------------------------------------------------------------------

# --- Ventana 1: Gráfico de Tensión ---
fig_vc, ax_vc = plt.subplots(figsize=(12, 6))
fig_vc.canvas.manager.set_window_title('Ciclo Completo de Tensión (vc)')

ax_vc.plot(t, vc_total, 'b-', label='Tensión en el Capacitor (vc)')
ax_vc.set_title('Ciclo Carga-Flotación-Descarga del Capacitor - Tensión')
ax_vc.set_xlabel('Tiempo (s)')
ax_vc.set_ylabel('Tensión (V)')
ax_vc.grid(True)
ax_vc.set_ylim(bottom=0, top=Vf * 1.1)
ax_vc.set_xlim(left=0)

# Añadir líneas verticales para marcar las transiciones
ax_vc.axvline(x=t_fin_carga, color='green', linestyle='--', label=f'Fin Carga (t={t_fin_carga}s)')
ax_vc.axvline(x=t_inicio_descarga, color='orange', linestyle='--', label=f'Inicio Descarga (t={t_inicio_descarga}s)')
ax_vc.legend()
fig_vc.tight_layout()


# --- Ventana 2: Gráfico de Corriente ---
fig_ic, ax_ic = plt.subplots(figsize=(12, 6))
fig_ic.canvas.manager.set_window_title('Ciclo Completo de Corriente (ic)')

ax_ic.plot(t, ic_total, 'r-', label='Corriente en el Capacitor (ic)')
ax_ic.set_title('Ciclo Carga-Flotación-Descarga del Capacitor - Corriente')
ax_ic.set_xlabel('Tiempo (s)')
ax_ic.set_ylabel('Corriente (A)')
ax_ic.grid(True)
ax_ic.set_xlim(left=0)

# Añadir una línea horizontal en y=0 para mejor referencia
ax_ic.axhline(y=0, color='black', linewidth=0.5)
# Añadir las líneas verticales de transición
ax_ic.axvline(x=t_fin_carga, color='green', linestyle='--', label=f'Fin Carga (t={t_fin_carga}s)')
ax_ic.axvline(x=t_inicio_descarga, color='orange', linestyle='--', label=f'Inicio Descarga (t={t_inicio_descarga}s)')
ax_ic.legend()
fig_ic.tight_layout()

# Mostrar ambas ventanas
plt.show()