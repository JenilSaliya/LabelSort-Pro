import os
import sys
import time
import socket
import argparse
import logging
import threading
import uvicorn

# Ensure the backend directory is in the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

logger = logging.getLogger("desktop_entry")


def find_free_port() -> int:
    """Finds an available ephemeral port on the loopback interface."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def is_pid_alive(pid: int) -> bool:
    """Checks if a process ID is still alive."""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        SYNCHRONIZE = 0x00100000
        kernel32 = ctypes.windll.kernel32

        # Try to open process handle
        handle = kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE,
            False,
            wintypes.DWORD(pid)
        )
        if not handle:
            return False

        try:
            # Check exit code
            exit_code = wintypes.DWORD()
            if kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                STILL_ACTIVE = 259
                return exit_code.value == STILL_ACTIVE
            return False
        finally:
            kernel32.CloseHandle(handle)
    else:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


def start_parent_watchdog(parent_pid: int) -> None:
    """
    Background daemon thread that monitors the parent (Tauri) process.
    If the parent process terminates or crashes, this sidecar exits immediately
    to guarantee zero zombie/orphaned processes in Windows Task Manager.
    """
    def _watchdog_loop():
        while True:
            time.sleep(1.5)
            if not is_pid_alive(parent_pid):
                logger.warning("Parent process %d terminated. Shutting down LabelSort sidecar...", parent_pid)
                os._exit(0)

    watchdog_thread = threading.Thread(target=_watchdog_loop, daemon=True, name="ParentWatchdog")
    watchdog_thread.start()


def main():
    parser = argparse.ArgumentParser(description="LabelSort Pro Desktop Engine Sidecar")
    parser.add_argument("--port", type=int, default=None, help="Port to bind the server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface to bind (default 127.0.0.1)")
    parser.add_argument("--parent-pid", type=int, default=None, help="Parent PID to monitor for lifecycle management")
    parser.add_argument("--log-level", type=str, default="warning", help="Log level (debug, info, warning, error)")
    args = parser.parse_args()

    # Determine port
    port = args.port if args.port is not None else find_free_port()

    # Determine parent PID to watch
    parent_pid = args.parent_pid if args.parent_pid is not None else os.getppid()
    if parent_pid and parent_pid > 1:
        start_parent_watchdog(parent_pid)

    # Output port marker for Tauri supervisor (unbuffered)
    print(f"LABELSORT_PORT:{port}", flush=True)
    sys.stdout.flush()

    # Launch Uvicorn
    uvicorn.run(
        app,
        host=args.host,
        port=port,
        log_level=args.log_level.lower(),
        access_log=False,
    )


if __name__ == "__main__":
    main()
