import dearpygui.dearpygui as dpg
import random
from time import sleep

# Inicializa DPG
dpg.create_context()



def update_plot():
    # Simula la recepción de un nuevo precio (deberías reemplazar esto con tu lógica de datos en tiempo real)
    new_price = random.randint(1, 100)
    
    # Obtiene los datos actuales de la serie
    series_data = dpg.get_value(random.random())
    
    # Añade el nuevo punto al final (simulando un nuevo punto de datos en el tiempo)
    series_data[0].append(len(series_data[0]) + 1)  # Simula el paso del tiempo
    series_data[1].append(new_price)  # Añade el nuevo precio
    
    # Actualiza la serie con los nuevos datos
    dpg.set_value(series_tag, series_data)




with dpg.window(label="Real-Time Crypto Price Plot"):
    # Crea el gráfico
    with dpg.plot(label="Crypto Price", height=400, width=400):
        # Añade ejes al gráfico
        dpg.add_plot_axis(dpg.mvXAxis, label="Time")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price", tag="y_axis")
        
        # Inicializa la serie con datos vacíos
        series_tag = dpg.add_line_series([], [], parent=y_axis, tag="price_series")

# Configura un temporizador en DPG para actualizar el gráfico regularmente
dpg.set_frame_callback
dpg.add_timer_callback(update_plot, 1000, user_data=None)

dpg.create_viewport(title='Dear PyGui Demo', width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
