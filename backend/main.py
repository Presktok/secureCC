from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import compiler.analyzer as compiler_analyzer

analyze = compiler_analyzer.analyze


def format_compile_success_output(program_stdout_stderr: str, exit_code: int) -> str:
    text = (program_stdout_stderr or "").replace("\r\n", "\n").rstrip("\n")
    parts: list[str] = []
    if text:
        parts.append(text)
        parts.append("")
    parts.append("✔ Compilation successful")
    parts.append(f"Exit code: {exit_code}")
    return "\n".join(parts)


def resolve_gcc() -> str | None:
    gcc_on_path = which("gcc")
    if gcc_on_path:
        return gcc_on_path

    candidates = [
        Path("C:/msys64/mingw64/bin/gcc.exe"),
        Path("C:/MinGW/bin/gcc.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None

app = FastAPI(title="SecureCC API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return Response(status_code=200)

BUILD_DIR = PROJECT_ROOT / "frontend/build"
if (BUILD_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(BUILD_DIR / "static")), name="static")

class AnalyzeRequest(BaseModel):
    code: str


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/backend/ping", response_class=PlainTextResponse)
def backend_ping():
    return "Backend is running"


@app.post("/compile")
@app.post("/api/compile")
def compile_code(payload: AnalyzeRequest):
    code = payload.code
    findings = analyze(code)


    high_risk = any(f["severity"] == "HIGH" for f in findings)

    if high_risk:
        return {
            "status": "blocked",
            "message": f"{len(findings)} vulnerabilities detected",
            "findings": findings,
        }

    gcc_executable = resolve_gcc()

    if not gcc_executable:
        return {
            "status": "error",
            "output": "GCC not installed. Install MinGW or GCC.",
        }

    with TemporaryDirectory(prefix="securecc_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        src_path = tmp_path / "temp.c"
        binary_name = "temp.exe" if os.name == "nt" else "temp.out"
        binary_path = tmp_path / binary_name
        src_path.write_text(code, encoding="utf-8")

        try:
            result = subprocess.run(
                [gcc_executable, str(src_path), "-o", str(binary_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except FileNotFoundError:
            return {
                "status": "error",
                "output": "GCC not installed. Install MinGW or GCC.",
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "output": "Compilation timed out.",
            }

        if result.returncode != 0:
            return {
                "status": "error",
                "output": result.stderr
            }

        try:
            run_result = subprocess.run(
                [str(binary_path)],
                capture_output=True,
                text=True,
                timeout=5,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "compiled",
                "output": (
                    "✔ Compilation successful\n"
                    "Exit code: (program did not finish - timed out, likely waiting for input or infinite loop)"
                ),
                "exit_code": None,
                "findings": findings,
            }
        except Exception as exc:
            return {
                "status": "compiled",
                "output": (
                    "✔ Compilation successful\n"
                    f"Exit code: (run failed - {exc})"
                ),
                "exit_code": None,
                "findings": findings,
            }

        combined = (run_result.stdout or "") + (run_result.stderr or "")
        exit_code = int(run_result.returncode)
        output = format_compile_success_output(combined, exit_code)

    return {
        "status": "compiled",
        "output": output,
        "exit_code": exit_code,
        "findings": findings,
    }


@app.get("/")
def read_root():
    index_path = BUILD_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "SecureCC API is running. Build frontend to serve UI from here."}


@app.get("/{path:path}")
def serve_spa(path: str):
    file_path = BUILD_DIR / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    
    index_path = BUILD_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
        
    return {"error": "Not Found", "detail": f"Path '{path}' not found and build directory is missing."}
