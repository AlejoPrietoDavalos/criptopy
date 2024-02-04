from typing import Dict

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from cripto_db.utils import get_client_cripto_db, get_klines_cripto_db
from general_utils.coins import SymbolPairsEnum, IntervalKLineEnum


def nomenclatura_klines(symbol: SymbolPairsEnum, interval: IntervalKLineEnum):
    return f"{symbol.value}_{interval.value}"





class CollectionKLines:
    def __init__(self, collection: Collection):
        self._collection = collection
    
    @property
    def collection(self) -> Collection:
        return self._collection
    
    # TODO: Implementar lógica de búsqueda.



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

