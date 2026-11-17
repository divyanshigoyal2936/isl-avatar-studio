import os
import sys
import time
import socket
import webbrowser
import threading

# Add backend directory to Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

def find_free_port(candidate_ports=[8000, 8080, 8001, 8002, 5000]):
    for port in candidate_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return 8080

def auto_open_browser(url):
    time.sleep(1.8)
    print(f"\n[Browser] Opening {url} ...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[Browser] Could not auto-launch browser ({e}). Please open {url} manually.")

if __name__ == "__main__":
    port = find_free_port()
    url = f"http://127.0.0.1:{port}/"

    print("=" * 64)
    print("  ISL AVATAR STUDIO — Speech to Indian Sign Language")
    print(f"  Live Server URL: {url}")
    print("=" * 64)
    print(f"Selected Port: {port} (free & ready)")
    print("Launching web interface in your default browser...")

    threading.Thread(target=auto_open_browser, args=(url,), daemon=True).start()

    try:
        import uvicorn
        from app.main import app
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
    except Exception as e:
        print(f"\n[Error] Server error: {e}")
        input("\nPress Enter to exit...")
