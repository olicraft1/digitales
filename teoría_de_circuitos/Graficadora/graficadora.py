import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# PARÁMETROS CONFIGURABLES POR EL USUARIO
# -------------------------------------------------------------------
# Modifica los siguientes valores según las características de tu circuito.

# --- Parámetros para la CARGA del capacitor ---
Vf = 80.0      # Tensión final o de la fuente (en Voltios)
Vi = 40.0       # Tensión inicial del capacitor al empezar la carga (en Voltios)
R_carga = 11000.0  # Resistencia de carga (en Ohmios, ej: 10k = 10000)
C_carga = 40.0/1000000   # Capacitancia (en Faradios, ej: 100uF = 0.0001)

# --- Parámetros para la DESCARGA del capacitor ---
V_descarga = 12.0  # Tensión inicial del capacitor al empezar la descarga (normalmente = Vf)
R_descarga = 10000.0 # Resistencia de descarga (en Ohmios, ej: 20k = 20000)
C_descarga = 100.0/1000000  # Capacitancia (en Faradios, ej: 100uF = 0.0001)


# -------------------------------------------------------------------
# CÁLCULOS (No es necesario modificar esta parte)
# -------------------------------------------------------------------

# --- Cálculo para la CARGA ---
# Constante de tiempo Tau (T)
T_carga = R_carga * C_carga
# Creamos un vector de tiempo (t) desde 0 hasta 5*T para ver el proceso completo
# Se usan 500 puntos para una curva suave.
t_carga = np.linspace(0, 5 * T_carga, 500)

# Fórmulas de carga
# vc(t) = Vf + (Vi - Vf) * e^(-t/T)
vc_carga = Vf + (Vi - Vf) * np.exp(-t_carga / T_carga)

# ic(t) = [(Vf - Vi) / R] * e^(-t/T)  (Se usa Vf como la tensión de la fuente 'V')
ic_carga = ((Vf - Vi) / R_carga) * np.exp(-t_carga / T_carga)


# --- Cálculo para la DESCARGA ---
# Constante de tiempo Tau (T)
T_descarga = R_descarga * C_descarga
# Creamos un vector de tiempo (t)
t_descarga = np.linspace(0, 5 * T_descarga, 500)

# Fórmulas de descarga
# vc(t) = V * e^(-t/T)
vc_descarga = V_descarga * np.exp(-t_descarga / T_descarga)

# ic(t) = -(V / R) * e^(-t/T)
# Nota: La corriente de descarga es negativa porque fluye en dirección opuesta a la de carga.
ic_descarga = -(V_descarga / R_descarga) * np.exp(-t_descarga / T_descarga)


# -------------------------------------------------------------------
# GENERACIÓN DE GRÁFICOS
# -------------------------------------------------------------------

# Creamos una figura con dos subplots (uno para carga, otro para descarga)
# figsize ajusta el tamaño de la ventana
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
fig.suptitle('Ejercicio 1: Gráfico', fontsize=16)

# --- Gráfico 1: Carga ---
ax1.set_title(f'Carga (R={R_carga}Ω, C={C_carga*1000000}µF, τ={T_carga:.2f}s)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Tensión (V)', color='blue')
# Graficamos vc(t) en el eje Y izquierdo
line1 = ax1.plot(t_carga, vc_carga, 'b-', label=f'Tensión (vc)')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Creamos un segundo eje Y para la corriente, compartiendo el mismo eje X
ax1_twin = ax1.twinx()
ax1_twin.set_ylabel('Corriente (A)', color='red')
# Graficamos ic(t) en el eje Y derecho
line2 = ax1_twin.plot(t_carga, ic_carga, 'r-', label=f'Corriente (ic)')
ax1_twin.tick_params(axis='y', labelcolor='red')

# Unimos las leyendas de ambos ejes en una sola caja
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='best')

# --- Gráfico 2: Descarga ---
ax2.set_title(f'Descarga (R={R_descarga}Ω, C={C_descarga*1000000}µF, τ={T_descarga:.2f}s)')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Tensión (V)', color='blue')
# Graficamos vc(t)
line3 = ax2.plot(t_descarga, vc_descarga, 'b-', label='Tensión (vc)')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.grid(True)

# Creamos el segundo eje Y para la corriente
ax2_twin = ax2.twinx()
ax2_twin.set_ylabel('Corriente (A)', color='red')
# Graficamos ic(t)
line4 = ax2_twin.plot(t_descarga, ic_descarga, 'r-', label='Corriente (ic)')
ax2_twin.tick_params(axis='y', labelcolor='red')

# Unimos las leyendas
lines2 = line3 + line4
labels2 = [l.get_label() for l in lines2]
ax2.legend(lines2, labels2, loc='best')


# Ajustamos el layout para que no se solapen los títulos y mostramos la gráfica
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.show()