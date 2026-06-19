import socket
import multiprocessing
import os

def check_fd(fd, label):
    """Verifica se un FD è aperto nel processo corrente e se è un socket TCP."""
    try:
        os.fstat(fd)  # lancia OSError se il FD è chiuso
        try:
            s = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
            name = s.getsockname()
            s.detach()  # non chiudiamo il FD reale
            return f"APERTO — socket TCP su {name}"
        except OSError:
            return "APERTO — ma non è un socket TCP"
    except OSError:
        return "CHIUSO (non ereditato)"

def handle_child(conn, addr, srv_fd):
    print(f"\n[FIGLIO fork | PID {os.getpid()}]")
    print(f"  fd={srv_fd} (srv) nel figlio: {check_fd(srv_fd, 'srv')}")
    print(f"  fd={conn.fileno()} (conn) nel figlio: {check_fd(conn.fileno(), 'conn')}")
    print(f"  => fork copia TUTTA la FD table: il figlio vede srv anche se non gli è stato passato!")
    print(f"  => bug reale: il figlio potrebbe accettare nuove connessioni su srv per errore")
    conn.sendall(b"ok fork\n")
    conn.close()
    print(f"  conn chiusa", flush=True)

if __name__ == '__main__':
    multiprocessing.set_start_method('fork')

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('127.0.0.1', 9000))
    srv.listen(5)

    print(f"[PADRE fork | PID {os.getpid()}]")
    print(f"  srv fd={srv.fileno()} → {srv.getsockname()}")
    print(f"  in ascolto su 127.0.0.1:9000 — Ctrl+C per uscire\n")

    try:
        while True:
            conn, addr = srv.accept()
            print(f"[PADRE fork | PID {os.getpid()}] conn da {addr}, conn fd={conn.fileno()}")
            p = multiprocessing.Process(target=handle_child, args=(conn, addr, srv.fileno()))
            p.daemon = True
            p.start()
            conn.close()
            print(f"  copia padre chiusa, figlio PID={p.pid}\n")
    except KeyboardInterrupt:
        print("\n[PADRE] uscita")
    finally:
        srv.close()
