""" Abstracción de la API de Binance."""
from typing import List, Generator
from datetime import datetime

from binance.um_futures import UMFutures

from general_utils.coins import SymbolPairsEnum, IntervalKLineEnum
from cripto_trading.kline import KLine
from general_utils.time_utc import get_timestamp_now, get_datetime, validate_time_ms

from binance_extras.searchs import SearchKLines
from binance_extras.utils import get_um_futures_client

class BinanceManager:
    def __init__(self, **kwargs):
        self._um = get_um_futures_client(**kwargs)

    @property
    def um(self) -> UMFutures:
        return self._um
    
    def mark_price_klines(self, search_klines: SearchKLines, keep_current_kline: bool = False) -> List[KLine]:
        """
        - BUG: Hay 9 segundos de diferencia entre la API de binance y el reloj UTC de python. Problemón.

        Notas:
        - Las velas se distinguen unívocamente por el `symbol`, `interval` y `time_open`.
        - La API de Binance hace el search usando `time_open`
        - Si no encuentra valores, retorna una lista vacía.
        - Si `time_open > time_open_last_kline` -> Siempre retorna vacío, para cualquier tiempo.
        - El último KLine siempre tiene `time_close > datetime.now(tz=UTC)`.
        """
        klines = [KLine.from_binance(kline) for kline in self.um.mark_price_klines(**search_klines.model_dump())]
        if not keep_current_kline:
            # Vamos a poner que cualquier KLine con time_close `<1m` lo deletee.
            is_safe = False
            while len(klines) > 0 and not is_safe:
                t_now = get_timestamp_now()
                t_close_last_kline = klines[-1].time_close

                # Esto es por que la vela actual se actualiza.
                is_current_kline = t_now <= t_close_last_kline
                # Esto es por que la API de Binance tiene retraso.
                is_unsafe_kline = abs(t_now - t_close_last_kline) < 60000
                if is_current_kline or is_unsafe_kline:
                    klines.pop(-1)
                else:
                    is_safe = True
            return klines
        else:
            raise NotImplementedError("Este caso hay que manejarlo con cuidado.")

    def iter_mark_price_klines(
            self,
            symbol: SymbolPairsEnum,
            interval: IntervalKLineEnum,
            limit: int,
            start_time: int | datetime,
            end_time: int | datetime,
        ) -> Generator[List[KLine], None, None]:
        iter_searchs = self.iter_search_klines(
            symbol = symbol,
            interval = interval,
            limit = limit,
            start_time = start_time,
            end_time = end_time
        )
        for search_klines in iter_searchs:
            yield self.mark_price_klines(search_klines)

    def iter_search_klines(
            self,
            symbol: SymbolPairsEnum,
            interval: IntervalKLineEnum,
            limit: int,
            start_time: int | datetime,
            end_time: int | datetime,
        ) -> Generator[SearchKLines, None, None]:
        """ Realiza la búsqueda de atrás para adelante en el rango de fecha especificado."""
        ms_interval = IntervalKLineEnum(interval).miliseconds
        start_time = validate_time_ms(start_time)
        end_time = validate_time_ms(end_time)

        i = 0
        start_time_aux = start_time
        while start_time_aux < end_time:
            search_klines = SearchKLines(
                symbol = symbol,
                interval = interval,
                limit = limit,
                start_time = start_time_aux
            )
            yield search_klines

            i += 1
            start_time_aux = start_time + i*ms_interval*limit

    def timestamp_first_data(self, symbol: SymbolPairsEnum) -> int:
        """ Busca desde el tiempo UNIX todos los intervalos. Se queda con el de menor `time_open`."""
        klines: List[KLine] = []
        for interval in IntervalKLineEnum:
            s = SearchKLines(
                symbol = symbol,
                interval = interval,
                limit = 1,
                start_time = 1  # Tiempo 0 de UNIX.
            )
            klines.extend(self.mark_price_klines(s))
        klines.sort(key=lambda kline: kline.time_open)
        return klines[0].time_open
