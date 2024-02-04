import dearpygui.dearpygui as dpg

if __name__ == "__main__":
    # TODO: Esto es lo que se conoce como el "entry-point" de un programa de Python.
    # Es lo que indica a otros programadores donde empieza el flujo de ejecución de tu programa.
    # Moverse a la raiz del proyecto, activar el entorno virtual y ejecutar "python3 run_ui.py".
    
    # Este es el hello world de DearPyGui: https://dearpygui.readthedocs.io/en/latest/tutorials/first-steps.html
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()