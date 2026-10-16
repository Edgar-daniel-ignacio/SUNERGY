"""Launch actual scaffold processes on loopback and check their observable behavior."""

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

from sunergy import __version__

ROOT = Path(__file__).resolve().parents[1]
# Local smoke requests never use an ambient HTTP proxy or any external resource.
HTTP = build_opener(ProxyHandler({}))


def unused_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def request(url: str, *, data: bytes | None = None) -> tuple[int, bytes]:
    query = Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with HTTP.open(query, timeout=6) as response:
            return response.status, response.read()
    except HTTPError as error:
        return error.code, error.read()


def stop(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


@contextmanager
def service(
    command: list[str], *, label: str, logs: Path, env: dict[str, str]
) -> Iterator[subprocess.Popen[bytes]]:
    log_path = logs / f"{label}.log"
    with log_path.open("wb") as output:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        try:
            yield process
        except Exception:
            stop(process)
            print(f"{label} log:\n{log_path.read_text(encoding='utf-8', errors='replace')[-4000:]}")
            raise
        finally:
            stop(process)


def wait_ready(url: str, process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Process exited before {url} was ready: {process.returncode}")
        try:
            if request(url)[0] == 200:
                return
        except (OSError, URLError):
            pass
        time.sleep(0.1)
    raise RuntimeError(f"Service did not become ready within 45 seconds: {url}")


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def smoke_test(*, frontend: bool) -> None:
    next_cli = ROOT / "frontend/node_modules/next/dist/bin/next"
    node = shutil.which("node")
    if frontend and (
        node is None or not next_cli.is_file() or not (ROOT / "frontend/.next/BUILD_ID").is_file()
    ):
        raise RuntimeError("Frontend smoke check requires Node, npm ci, and npm run build")

    api_port = unused_port()
    api_url = f"http://127.0.0.1:{api_port}"
    env = {**os.environ, "NEXT_TELEMETRY_DISABLED": "1"}
    api_command = [
        sys.executable,
        "-m",
        "uvicorn",
        "sunergy.api:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(api_port),
    ]
    health = {"status": "ok", "service": "sunergy", "version": __version__}
    with tempfile.TemporaryDirectory(prefix="sunergy-smoke-") as directory:
        logs = Path(directory)
        with service(api_command, label="api", logs=logs, env=env) as api:
            wait_ready(f"{api_url}/health", api)
            expect(json.loads(request(f"{api_url}/health")[1]) == health, "Unexpected API health")
            status, content = request(f"{api_url}/api/v1/capabilities")
            expect(
                status == 200 and json.loads(content)["module_iv"] == "not_implemented",
                "API must report calculations unavailable",
            )
            expect(
                request(f"{api_url}/api/v1/module-iv", data=b"{}")[0] == 422,
                "Invalid requests must return a schema error",
            )
            print("PASS: actual Uvicorn launch, health, capability and schema-error responses")
            if not frontend:
                return

            frontend_port = unused_port()
            web_url = f"http://127.0.0.1:{frontend_port}"
            command = [
                str(node),
                str(next_cli),
                "start",
                str(ROOT / "frontend"),
                "--hostname",
                "127.0.0.1",
                "--port",
                str(frontend_port),
            ]
            with service(
                command, label="frontend", logs=logs, env={**env, "SUNERGY_API_URL": api_url}
            ) as web:
                wait_ready(web_url, web)
                status, content = request(web_url)
                expect(
                    status == 200 and b"The simulations are still ahead." in content,
                    "Frontend must render its explicit pending-capability notice",
                )
                status, content = request(f"{web_url}/api/health")
                expect(status == 200 and json.loads(content) == health, "Health proxy failed")
                stop(api)
                expect(
                    request(f"{web_url}/api/health")[0] == 503,
                    "Health proxy must report unavailable backend as 503",
                )
                expect(request(web_url)[0] == 200, "Frontend must render without the backend")
                print(
                    "PASS: built Next launch, page, health proxy, and backend-unavailable handling"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontend", action="store_true", help="Also check the built Next app")
    smoke_test(frontend=parser.parse_args().frontend)
