# TODO: Esto lo extraje del código fuente de DearPyGui, es la función para plotear grafico de velas.
# TODO: Ver que nos sirve, en principio con ["dates", "opens", "closes", "lows", "highs"] creo que nos alcanza.
# Documentación: https://dearpygui.readthedocs.io/en/latest/reference/dearpygui.html?highlight=candle#dearpygui.dearpygui.add_candle_series
import dearpygui.dearpygui as dpg
dpg.add_candle_series   # Probar pasarle como parámetros columnas de un dataframe. Ver ejemplos en internet.


# def add_candle_series(dates : Union[List[float], Tuple[float, ...]], opens : Union[List[float], Tuple[float, ...]], closes : Union[List[float], Tuple[float, ...]], lows : Union[List[float], Tuple[float, ...]], highs : Union[List[float], Tuple[float, ...]], *, label: str =None, user_data: Any =None, use_internal_label: bool =True, tag: Union[int, str] =0, parent: Union[int, str] =0, before: Union[int, str] =0, source: Union[int, str] =0, show: bool =True, bull_color: Union[List[int], Tuple[int, ...]] =(0, 255, 113, 255), bear_color: Union[List[int], Tuple[int, ...]] =(218, 13, 79, 255), weight: float =0.25, tooltip: bool =True, time_unit: int =5, **kwargs) -> Union[int, str]:
# 	"""	 Adds a candle series to a plot.
# 
# 	Args:
# 		dates (Any): 
# 		opens (Any): 
# 		closes (Any): 
# 		lows (Any): 
# 		highs (Any): 
# 		label (str, optional): Overrides 'name' as label.
# 		user_data (Any, optional): User data for callbacks
# 		use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
# 		tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
# 		parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
# 		before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
# 		source (Union[int, str], optional): Overrides 'id' as value storage key.
# 		show (bool, optional): Attempt to render widget.
# 		bull_color (Union[List[int], Tuple[int, ...]], optional): 
# 		bear_color (Union[List[int], Tuple[int, ...]], optional): 
# 		weight (float, optional): 
# 		tooltip (bool, optional): 
# 		time_unit (int, optional): mvTimeUnit_* constants. Default mvTimeUnit_Day.
# 		id (Union[int, str], optional): (deprecated) 
# 	Returns:
# 		Union[int, str]
# 	"""