""" Para gestionar la DB.
- TODO: Hacer esto correctamente.
"""
import sys

from cripto_db.db_klines import DBKLines

def set_unique_keys():
    db_klines = DBKLines()
    db_klines.set_unique_keys()

if __name__ == "__main__":
    try:
        flag = str(sys.argv[1])
        if flag == "--set-unique-keys":
            set_unique_keys()
    except Exception as e:
        print("~"*40)
        print("---> Insertar la flag.")
        print("~"*40)