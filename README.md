# Objetivos
- asd

# Paquetes
- `cripto_trading:` Utilidades para manipular y analizar los precios de mercado.


# Quick-Start
##### Crear entorno virtual e instalar dependencias.
```bash
cd /path/to/the/project

python3 -m venv env                 # Crear entorno.

source env/bin/activate             # Activar entorno.

pip install -r requirements.txt     # Instalar dependencias en el entorno.
```

##### Establecer variables de entorno.
- Crear un archivo de texto llamado `.env` en la raiz del proyecto.
- Editarlo con las siguiente variables de entorno:
```bash
BINANCE_API_KEY="...."
BINANCE_SECRET_KEY="...."

MONGO_CRIPTO_USER="...."
MONGO_CRIPTO_PASSWORD="...."
MONGO_CRIPTO_CLUSTER_DOMAIN="...."
MONGO_CRIPTO_KLINES="klines"
```

##### Info sin revisar
- lumibot Strategy
- yahoo data backtesting
