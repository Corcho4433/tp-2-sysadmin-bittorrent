import time
import os
import sys
import select
import termios
import tty
import libtorrent as lt


def getch():
    """Leer un solo caracter sin bloqueo de stdin (Linux/macOS)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        if select.select([sys.stdin], [], [], 0.1)[0]:
            ch = sys.stdin.read(1)
            return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def download_torrent(torrent_path_or_magnet, download_dir):
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

    print("Configurando la sesión libtorrent...")

    params = lt.add_torrent_params()
    params.save_path = download_dir

    if download_dir == '.':
        print("Los archivos se descargarán en el directorio actual.")
    else:
        print(f"Los archivos se descargarán en '{download_dir}'.")

    if torrent_path_or_magnet.startswith("magnet:"):
        print(f"Agregando magnet link: {torrent_path_or_magnet}")
        params.url = torrent_path_or_magnet
    elif os.path.exists(torrent_path_or_magnet):
        print(f"Agregando archivo .torrent: {torrent_path_or_magnet}")
        try:
            e = lt.bdecode(open(torrent_path_or_magnet, 'rb').read())
            info = lt.torrent_info(e)
            params.ti = info
        except Exception as e:
            print(f"Error al leer el archivo torrent: {e}")
            return
    else:
        print(
            f"Error: No se encontró el archivo .torrent o el magnet link es inválido: {torrent_path_or_magnet}")
        return

    h = ses.add_torrent(params)
    print(f"Torrent '{h.status().name}' agregado. Esperando metadatos...")

    while not h.status().has_metadata:
        print("Esperando metadatos...")
        time.sleep(1)

    print(f"Metadatos obtenidos para '{h.status().name}'")

    state_str = ['queued', 'checking', 'downloading metadata', 'downloading',
                 'finished', 'seeding', 'allocating', 'checking fastresume']

    try:
        while True:
            s = h.status()
            clear_screen()

            print("Iniciando descarga. Presiona 'p' para pausar, 'r' para reanudar, 'c' para cancelar, 's' para estado, 'q' para salir.")

            print(f"\rEstado: {state_str[s.state]:<22} | Progreso: {s.progress * 100:5.2f}% | "
                  f"Descargado: {s.total_payload_download / 1000:8.2f} kB | Vel. Descarga: {s.download_rate / 1000:7.2f} kB/s | "
                  f"Seeds: {s.num_seeds:3d} | Pares: {s.num_peers:3d}  ", end='')

            char = getch()
            if char:
                char = char.lower()
                if char == 'p':
                    h.pause()
                    print("\nDescarga pausada.")
                    time.sleep(2)
                elif char == 'r':
                    h.resume()
                    print("\nDescarga reanudada.")
                    time.sleep(2)
                elif char == 'c':
                    print("\nCancelando descarga...")
                    ses.remove_torrent(h)
                    print("Descarga cancelada.")
                    break
                elif char == 's':
                    print("\n--- Estado Actual ---")
                    print(f"Estado: {state_str[s.state]}")
                    print(f"Progreso: {s.progress * 100:.2f}%")
                    print(
                        f"Descargado: {s.total_payload_download / 1000:.2f} kB")
                    print(f"Subido: {s.total_payload_upload / 1000:.2f} kB")
                    print(f"Vel. Descarga: {s.download_rate / 1000:.2f} kB/s")
                    print(f"Vel. Subida: {s.upload_rate / 1000:.2f} kB/s")
                    print(f"Seeds: {s.num_seeds}")
                    print(f"Pares: {s.num_peers}")
                    print("---------------------")
                    time.sleep(2)  # Pausa para que el usuario pueda leer
                elif char == 'q':
                    print("\nSaliendo...")
                    break

            if s.is_finished:
                print("\nDescarga completada!")
                break

    except KeyboardInterrupt:
        clear_screen()
        print("\nDescarga interrumpida por el usuario.")

    print("Cerrando sesión libtorrent...")
    print("Sesión libtorrent cerrada.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Uso: python main.py '<ruta_al_torrent_o_magnet>' '[ruta_de_descarga]'")
        sys.exit(1)

    torrent_param = sys.argv[1]
    save_path = sys.argv[2] if len(sys.argv) >= 3 else '.'

    download_torrent(torrent_param, save_path)
