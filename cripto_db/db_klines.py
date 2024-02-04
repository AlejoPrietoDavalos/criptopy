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

    def get_collection(self, symbol: SymbolPairsEnum, interval: IntervalKLineEnum) -> None:
        key_search = nomenclatura_klines(symbol, interval)
        if key_search not in self.collections:
            collection = self.db[key_search]
            self.collections[key_search] = CollectionKLines(collection=collection)
        return self.collections[key_search]