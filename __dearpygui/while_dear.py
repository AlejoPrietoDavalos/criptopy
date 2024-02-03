import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")

dpg.show_viewport()

# below replaces, start_dearpygui()
import time

t_i = time.time()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    print("this will run every frame")
    dt = time.time() - t_i
    if dt > 10:
        """
        dates = df['date'].to_numpy()
        min_dates = min(dates)
        max_dates = max(dates)
        opens = df['open'].to_numpy()
        highs = df['high'].to_numpy()
        max_highs = max(highs)
        lows = df['low'].to_numpy()
        min_lows = min(lows)
        closes = df['close'].to_numpy()
        """
        #dpg.add_candle_series()
        #dpg.add_candle_series(
        #    dates = dates, opens = opens,
        #    highs = highs, lows = lows,
        #    closes = closes, parent = last_item(),
        #    label = "Candlesticks"
        #)
        dpg.stop_dearpygui()
    dpg.render_dearpygui_frame()

dpg.destroy_context()