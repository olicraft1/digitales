import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# PARÁMETROS CONFIGURABLES POR EL USUARIO
# -------------------------------------------------------------------
# Modifica los siguientes valores según las características de tu circuito.

# --- Parámetros para la CARGA del capacitor ---
Vf = 12.0      # Tensión final o de la fuente (en Voltios)
Vi = 0.0       # Tensión inicial del capacitor al empezar la carga (en Voltios)
R_carga = 10000.0  # Resistencia de carga (en Ohmios, ej: 10k = 10000)
C_carga = 0.0001   # Capacitancia (en Faradios, ej: 100uF = 0.0001)

# --- Parámetros para la DESCARGA del capacitor ---
V_descarga = 12.0  # Tensión inicial del capacitor al empezar la descarga (normalmente = Vf)
R_descarga = 20000.0 # Resistencia de descarga (en Ohmios, ej: 20k = 20000)
C_descarga = 0.0001  # Capacitancia (en Faradios, ej: 100uF = 0.0001)


# -------------------------------------------------------------------
# CÁLCULOS (No es necesario modificar esta parte)
# -------------------------------------------------------------------

# --- Cálculo para la CARGA ---
T_carga = R_carga * C_carga
t_carga = np.linspace(0, 5 * T_carga, 500)
vc_carga = Vf + (Vi - Vf) * np.exp(-t_carga / T_carga)
ic_carga = ((Vf - Vi) / R_carga) * np.exp(-t_carga / T_carga)

# --- Cálculo para la DESCARGA ---
T_descarga = R_descarga * C_descarga
t_descarga = np.linspace(0, 5 * T_descarga, 500)
vc_descarga = V_descarga * np.exp(-t_descarga / T_descarga)
# ===== FÓRMULA CORREGIDA SEGÚN PETICIÓN =====
# La corriente de descarga es negativa porque fluye en dirección opuesta.
ic_descarga = -(V_descarga / R_descarga) * np.exp(-t_descarga / T_descarga)


# -------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS (EN VENTANAS SEPARADAS)
# -------------------------------------------------------------------

# --- Gráfico 1: Proceso de Carga ---
fig_carga, ax_carga = plt.subplots(figsize=(10, 6))
fig_carga.canvas.manager.set_window_title('Gráfico de Carga del Capacitor')

ax_carga.set_title(f'Carga (R={R_carga}Ω, C={C_carga}F, T={T_carga:.2f}s)')
ax_carga.set_xlabel('Tiempo (s)')
ax_carga.set_ylabel('Tensión (V)', color='blue')
line1 = ax_carga.plot(t_carga, vc_carga, 'b-', label='Tensión (vc)')
ax_carga.tick_params(axis='y', labelcolor='blue')
ax_carga.grid(True)
ax_carga.set_ylim(bottom=0, top=Vf * 1.1) # Forzar eje Y de tensión a empezar en 0

ax_carga_twin = ax_carga.twinx()
ax_carga_twin.set_ylabel('Corriente (A)', color='red')
line2 = ax_carga_twin.plot(t_carga, ic_carga, 'r-', label='Corriente (ic)')
ax_carga_twin.tick_params(axis='y', labelcolor='red')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax_carga.legend(lines, labels, loc='best')
fig_carga.tight_layout()


# --- Gráfico 2: Proceso de Descarga ---
fig_descarga, ax_descarga = plt.subplots(figsize=(10, 6))
fig_descarga.canvas.manager.set_window_title('Gráfico de Descarga del Capacitor')

ax_descarga.set_title(f'Descarga (R={R_descarga}Ω, C={C_descarga}F, T={T_descarga:.2f}s)')
ax_descarga.set_xlabel('Tiempo (s)')
ax_descarga.set_ylabel('Tensión (V)', color='blue')
line3 = ax_descarga.plot(t_descarga, vc_descarga, 'b-', label='Tensión (vc)')
ax_descarga.tick_params(axis='y', labelcolor='blue')
ax_descarga.grid(True)
ax_descarga.set_ylim(bottom=0, top=V_descarga * 1.1) # Forzar eje Y de tensión a empezar en 0

ax_descarga_twin = ax_descarga.twinx()
ax_descarga_twin.set_ylabel('Corriente (A)', color='red')
line4 = ax_descarga_twin.plot(t_descarga, ic_descarga, 'r-', label='Corriente (ic)')
ax_descarga_twin.tick_params(axis='y', labelcolor='red')

# =====> LÍNEAS MODIFICADAS <=====
# Hacemos el eje Y de la corriente simétrico para ver la parte negativa.
# 1. Calculamos la corriente máxima (en valor absoluto) que se alcanza en t=0.
max_abs_current = V_descarga / R_descarga
# 2. Establecemos los límites del eje Y con un margen del 10%.
current_limit = max_abs_current * 1.1
ax_descarga_twin.set_ylim(-current_limit, current_limit)

lines2 = line3 + line4
labels2 = [l.get_label() for l in lines2]
ax_descarga.legend(lines2, labels2, loc='best')
fig_descarga.tight_layout()


# Muestra AMBAS ventanas de gráficos
plt.show()