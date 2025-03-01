""" Abstracción de la API de Binance."""
from typing import List, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

import pandas as pd
from binance.um_futures import UMFutures

from general_utils.coins import SymbolPairsEnum, IntervalKLineEnum
from cripto_trading.kline import KLine
from general_utils.time_utc import get_timestamp_now, get_datetime, validate_time_ms
from binance_extras.searchs import SearchKLines
from binance_extras.utils import get_um_futures_client

LIMIT_KLINES = 1500


def save_klines(path_out: Path, klines: List[KLine]) -> None:
    df_klines = pd.DataFrame([kline.model_dump() for kline in klines])
    df_klines.to_csv(path_out)


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

    def iter_all_mark_price_klines(
            self,
            symbol: SymbolPairsEnum,
            interval: IntervalKLineEnum
        ) -> Generator[List[KLine], None, None]:
        symbol = SymbolPairsEnum(symbol)
        interval = IntervalKLineEnum(interval)

        time_first = self.timestamp_first_data(symbol)
        time_end = get_timestamp_now()
        n_iters = ((time_end - time_first) // (LIMIT_KLINES*interval.miliseconds)) + 1

        _iter_klines = self.iter_mark_price_klines(
            symbol = symbol,
            interval = interval,
            limit = LIMIT_KLINES,
            start_time = time_first,
            end_time = time_end
        )
        for i, klines in enumerate(_iter_klines, start=1):
            yield klines
            print(f"{i}/{n_iters} - {symbol.value}_{interval.value}")

    def download_save_klines(
            self,
            path_data_klines: Path,
            symbol: SymbolPairsEnum,
            interval: IntervalKLineEnum,
            max_workers: int = 100
        ) -> None:
        path_klines_out = path_data_klines / f"{symbol.value}_{interval.value}"
        if not path_klines_out.exists():
            path_klines_out.mkdir(exist_ok=True)
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                iter_futures = (pool.submit(save_klines, path_klines_out / f"{i}.csv", klines)
                                for i, klines in enumerate(self.iter_all_mark_price_klines(symbol, interval)))
                for future in as_completed(iter_futures):
                    future.result()

