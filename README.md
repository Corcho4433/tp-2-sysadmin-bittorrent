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
En caso de usar un magnet, simplemente pegar el magnet de la siguiente manera `python main.py "magnet" "ruta_destino"`.
Es importante que tanto la ruta o el magnet y la ruta de descarga esten entre comillas ya que el programa podría funcionar mal si no lo hacen.

# Funcionamiento del proyecto

**Inicialización y configuración**:

   - Los argumentos proporcionados por el usuario (archivo `.torrent` o enlace magnet, y la ruta de descarga) se pasan a la función `download_torrent()`.

   - Se crea una sesión de `libtorrent` con `lt.session()` que escucha en el puerto `6881`.
   
   - Se configuran los parámetros del torrent usando `add_torrent_params`, incluyendo la ruta de guardado (`save_path`).

**Carga del torrent**:

   - Si el parámetro es un enlace magnet, se asigna directamente a `params.url`.
   
   - Si es un archivo `.torrent`, se abre y decodifica usando `lt.bdecode()` y `lt.torrent_info()`.
   
   - Luego se agrega el torrent a la sesión con `add_torrent()`.

**Esperando metadatos**:
   
   - Se entra en un bucle `while` que espera a que el torrent obtenga sus metadatos (`has_metadata == True`).

**Descarga**:

   - Una vez obtenidos los metadatos, se inicia la descarga en un bucle principal (`while True`).

   - En cada iteración, se limpia la pantalla con `clear_screen()` y se imprime el estado actual de la descarga: progreso, velocidad, semillas, etc.


**Interacción del usuario**:

   - Se capturan teclas en tiempo real mediante la función `getch()`.

   - El usuario puede pausar (`p`), reanudar (`r`), cancelar (`c`), ver el estado (`s`) o salir (`q`) sin interrumpir el proceso principal.


**Finalización**:

   - Si la descarga finaliza (`s.is_finished`), se imprime un mensaje y se sale del bucle.

   - Si el usuario interrumpe el programa con `Ctrl+C`, se detecta con `KeyboardInterrupt` y se cierra limpiamente.

   - Al finalizar, se cierra la sesión de `libtorrent`.

# Funcionamiento de la librería

**bdecode()** - Función clave

 - Propósito: Decodifica los datos en formato `Bencode` (formato usado en archivos .torrent).
 - Detalles: Recibe un input de bytes crudos de un archivo `.torrent` y devuelve un diccionario con la estructura decodificada.

**torrent_info()** - Información del torrent

 - Propósito: Representa la metainformación de un torrent (nombre, tamaño, piezas, etc.).
 - Parámetros de construcción: Un diccionario decodificado con bdecode. También acepta rutas de archivo o magnet links.

**session()** - Núcleo de Libtorrent

 - Propósito: Maneja todas las operaciones de red y torrents.
 - Configuración: Se usa `listen_interfaces` para definir donde escucha conexiones entrantes. 

**add_torrent(params)** - Incio de descarga

 - Propósito: Iniciar la descarga del torrent
 - Retorna: Objeto `torrent_handle` para controlar el torrent. Este objeto controla la descarga y permite operaciones como `pause()`, `resume()` y `status`

**handler.status()**

 - Retorno: Objeto `torrent_status` con propiedades como:
    
    - `state`: Estado actual (enumeración).
    - `progress`: % descargado (0.0 a 1.0).
    - `total_payload_download`: Bytes totales útiles descargados.
    - `download_rate`: Velocidad actual (bytes/segundo).
    - `num_seeds`/`num_peers`: Seeds y peers conectados.
    - `has_metadata`: Metadatos descargados o no.
    - `is_finished`: Descarga completada o no.