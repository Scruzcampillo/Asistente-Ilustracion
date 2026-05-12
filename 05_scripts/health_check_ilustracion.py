#!/usr/bin/env python3
"""Health checks for Asistente Ilustracion protocols."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "06_desarrollo" / "backups_protocolos"

FILES = {
    "agents": ROOT / "AGENTS.MD",
    "rol": ROOT / "00_system" / "rol_base.md",
    "health": ROOT / "00_system" / "nucleo_salud.md",
    "skills_readme": ROOT / "01_skills" / "README.md",
    "ia_skill": ROOT / "01_skills" / "skill_ia_ilustracion.md",
    "docs": ROOT / "02_conocimiento" / "Documentacion_IA_Ilustracion.md",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def ok(name: str, cond: bool, detail: str = "") -> tuple[bool, str]:
    status = "OK" if cond else "FAIL"
    msg = f"{status}: {name}"
    if detail:
        msg += f" - {detail}"
    return cond, msg


def backup() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / stamp
    dest.mkdir(parents=True, exist_ok=False)
    for path in FILES.values():
        if path.exists():
            rel = path.relative_to(ROOT)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    return dest


def checks() -> list[tuple[bool, str]]:
    out: list[tuple[bool, str]] = []
    for name, path in FILES.items():
        out.append(ok(f"file exists: {name}", path.exists(), str(path.relative_to(ROOT))))

    if not all(path.exists() for path in FILES.values()):
        return out

    agents = read(FILES["agents"])
    rol = read(FILES["rol"])
    health = read(FILES["health"])
    readme = read(FILES["skills_readme"])
    skill = read(FILES["ia_skill"])
    docs = read(FILES["docs"])

    combined = "\n".join([agents, rol, health, skill, docs])
    out.append(ok("hardware limit declared", "8 GB" in combined and "3060 Ti" in combined))
    out.append(ok("flux constrained", "Flux" in combined and ("GGUF" in combined or "NF4" in combined)))
    out.append(ok("sdxl workflow declared", "SDXL" in combined and "FaceDetailer" in combined and "Upscale" in combined))
    out.append(ok("health check referenced", "health_check_ilustracion.py" in health))
    out.append(ok("readme routes maintenance to Desarrollo", "skill_creacion_skills.md" in readme))
    out.append(ok("external repo boundary declared", "No modificar repos externos" in health))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backup", action="store_true")
    args = ap.parse_args()
    if args.backup:
        print(f"backup: {backup()}")

    failed = False
    for passed, msg in checks():
        print(msg)
        failed = failed or not passed
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

