# Como compilar este proyecto

## Requisitos

- Python 3
- Pip

## Instalación

1. Abre una terminal en el directorio del proyecto.
2. Es recomendable crear un virtual environment para el proyecto con `python -m venv venv`.
3. Accede al virtual environment con `source venv/bin/activate`.
4. Instala las dependencias del proyecto con `pip install -r requirements.txt`.

# Como usar este proyecto

1. Para usar el programa, en la terminal ejecuta `python main.py <archivo_torrent / magnet_link> <directorio_destino>`.
    - El primer parámetro es el archivo `.torrent` o el magnet link del archivo `.torrent` que deseas descargar.
    - El segundo parámetro es el directorio en el que deseas guardar los archivos descargados.
    - Si no se especifica el segundo parámetro, los archivos se descargarán en el directorio actual.

2. Los controles del programa son:
    - `p`: Pausar la descarga.
    - `r`: Reanudar la descarga.
    - `c`: Cancelar la descarga.
    - `s`: Mostrar el estado actual de la descarga.
    - `q`: Salir del programa.

## Ejemplo de uso

Para ejecutar el programa con un archivo `.torrent` local, ejecuta `python main.py "ruta_al_archivo.torrent" "ruta_destino"`.
Es importante que tanto la ruta o el magnet y la ruta de descarga esten entre comillas ya que el programa podría funcionar mal si no lo hacen.
