from typing import Tuple

import dearpygui.dearpygui as dpg
import pandas as pd
from pandas import DataFrame

TIME_OPEN = "time_open"
PRICE_OPEN = "price_open"
PRICE_HIGH = "price_high"
PRICE_LOW = "price_low"
PRICE_CLOSE = "price_close"


if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)

    #with dpg.window(label="Example Window"):
    #    dpg.add_text("Hello, world")
    #    dpg.add_button(label="Save")
    #    dpg.add_input_text(label="string", default_value="Quick brown fox")
    #    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    def on_mouse_drag(sender, app_data, user_data):
        # user_data contiene x_axis_id, y_axis_id
        x_axis_id, _ = user_data
        
        print("~"*40)
        print(app_data)
        print("-"*40)
        print(user_data)
        print("~"*40)
        #print(drag_delta)
        min_x, max_x = dpg.get_axis_limits(x_axis_id)
        dx = max_x - min_x
        
        sign = 1 if app_data[1] >= 0 else -1
        drag_delta = sign*dx/100#app_data[1]*5000  # app_data[1] podría contener el delta del arrastre en X; ajusta según la documentación

        # Ajusta el delta según tu escala o preferencias
        new_min_x = min_x - drag_delta
        new_max_x = max_x - drag_delta
        
        # Establecer nuevos límites para simular el desplazamiento
        dpg.set_axis_limits(x_axis_id, new_min_x, new_max_x)



    def on_mouse_wheel(sender, app_data, x_axis_id, y_axis_id):
        # Ajusta estos valores según el scroll
        zoom_factor = 0.1  # Esto determinará qué tan rápido se hace zoom in/out
        min_x, max_x = dpg.get_axis_limits(x_axis_id)
        min_y, max_y = dpg.get_axis_limits(y_axis_id)

        if app_data > 0:  # Scroll hacia arriba, zoom in
            zoom_amount = (max_x - min_x) * zoom_factor
            dpg.set_axis_limits(x_axis_id, min_x + zoom_amount, max_x - zoom_amount)
        else:  # Scroll hacia abajo, zoom out
            zoom_amount = (max_x - min_x) * zoom_factor
            dpg.set_axis_limits(x_axis_id, max(min_x - zoom_amount, 0), max_x + zoom_amount)  # Asegúrate de no tener límites negativos


    def create_candle_series(win: int, df: DataFrame) -> Tuple[int, int, int]:
        dates = df[TIME_OPEN].to_numpy() / 1000
        min_dates = min(dates)
        max_dates = max(dates)
        opens = df[PRICE_OPEN].to_numpy()
        highs = df[PRICE_HIGH].to_numpy()
        max_highs = max(highs)
        lows = df[PRICE_LOW].to_numpy()
        min_lows = min(lows)
        closes = df[PRICE_CLOSE].to_numpy()
        with dpg.plot(label="Candles Plot", width=-1, height=-1) as plot_id:
            dpg.add_plot_legend()
            x_axis_id = dpg.add_plot_axis(dpg.mvXAxis, label="Dates", time=True)
            dpg.set_axis_limits(dpg.last_item(), min_dates, max_dates)
            y_axis_id = dpg.add_plot_axis(dpg.mvYAxis, label="Prices")
            dpg.set_axis_limits(dpg.last_item(), min_lows, max_highs)
            dpg.add_candle_series(
                dates = dates,
                opens = opens,
                highs = highs,
                lows = lows,
                closes = closes,
                label = "BTCUSDT_1d",
                parent = dpg.last_item()
            )
        return plot_id, x_axis_id, y_axis_id
    



    df = pd.read_csv("data/klines/BTCUSDT_1d.csv")
    with dpg.window(label="Trader", width=500, height=500, pos=[0, 0]) as main_window:
        plot_id, x_axis_id, y_axis_id = create_candle_series(main_window, df)
    
    with dpg.handler_registry():
        dpg.add_mouse_wheel_handler(callback=lambda sender, app_data: on_mouse_wheel(sender, app_data, x_axis_id, y_axis_id))

    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(callback=lambda sender, app_data: on_mouse_drag(sender, app_data, (x_axis_id, y_axis_id)))


    dpg.set_primary_window(main_window, True)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    print("asd")
    dpg.start_dearpygui()
    dpg.destroy_context()