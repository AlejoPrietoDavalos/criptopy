from typing import Dict, List

from pymongo import MongoClient, DESCENDING, ASCENDING, UpdateOne
from pymongo.cursor import Cursor
from pymongo.results import BulkWriteResult
from pymongo.database import Database
from pymongo.collection import Collection

from cripto_db.utils import get_client_cripto_db, get_klines_cripto_db
from cripto_trading.kline import KLine, TIME_OPEN
from general_utils.coins import SymbolPairsEnum, IntervalKLineEnum, iter_all_symbol_interval, get_collection_name


def filter_time_open(time_open: int) -> dict:
    return {TIME_OPEN: time_open}

def kline_to_update_one(kline: KLine) -> UpdateOne:
    """ Transforma el KLine en un UpdateOne para la subida a la DB."""
    return UpdateOne(
        filter_time_open(kline.time_open),           # Criterio de búsqueda por time_open
        {'$setOnInsert': kline.model_dump()},   # $setOnInsert solo actualiza en caso de insertar
        upsert = True                           # Realiza un insert si el documento no existe.
    )

class CollectionKLines:
    def __init__(self, db: Database, coll_name: str):
        self._collection = db[coll_name]
        self._coll_name = coll_name
    
    @property
    def collection(self) -> Collection:
        return self._collection
    
    @property
    def coll_name(self) -> str:
        return self._coll_name
    
    def insert_klines(self, klines: List[KLine]) -> BulkWriteResult:
        operations = [kline_to_update_one(kline) for kline in klines]
        result = self.collection.bulk_write(operations)
        return result

    def find_klines(self, direction=ASCENDING) -> Cursor:
        return self.collection.find().sort(TIME_OPEN, direction)


class DBKLines:
    def __init__(self):
        self._client = get_client_cripto_db()
        self._db = get_klines_cripto_db(self._client)
        self._collections: Dict[str, CollectionKLines] = {}
    
    @property
    def client(self) -> MongoClient:
        return self._client
    
    @property
    def db(self) -> Database:
        return self._db
    
    @property
    def collections(self) -> Dict[str, CollectionKLines]:
        return self._collections

    def get_collection(self, symbol: SymbolPairsEnum, interval: IntervalKLineEnum) -> CollectionKLines:
        symbol, interval = SymbolPairsEnum(symbol), IntervalKLineEnum(interval)
        coll_name = get_collection_name(symbol, interval)
        if coll_name not in self.collections:
            self.collections[coll_name] = CollectionKLines(db=self.db, coll_name=coll_name)
        return self.collections[coll_name]
    
    def set_unique_keys(self) -> None:
        for symbol, interval in iter_all_symbol_interval():
            coll_name = get_collection_name(symbol, interval)
            collection = self.get_collection(symbol, interval)
            collection.collection.create_index([(TIME_OPEN, ASCENDING)], unique=True)
            print(f"Creación de índice para: {coll_name}")

