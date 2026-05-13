---
Creada: 2026-05-12
Actualizada: 2026-05-12T09:27
---
# Nucleo de salud - Asistente de Ilustracion

## Proposito

Mantener verificables los contratos de workflows de IA visual local.

## Fuentes de verdad

1. `AGENTS.MD`: arquitectura, modalidades y limite de hardware.
2. `00_system/rol_base.md`: identidad, hardware y reglas criticas.
3. `00_system/nucleo_salud.md`: contratos de salud.
4. `01_skills/skill_ia_ilustracion.md`: modelos, workflows, rostros y upscale.
5. `02_conocimiento/Documentacion_IA_Ilustracion.md`: documentacion tecnica profunda.
6. `05_scripts/health_check_ilustracion.py`: check tecnico minimo.

## Contratos

- Nunca ignorar el limite de 8 GB de VRAM.
- Priorizar workflows ejecutables en RTX 3060 Ti y 16 GB RAM.
- SDXL es la base segura; Flux debe ir cuantizado o con offload claro.
- FaceDetailer y upscaling por tiles son parte del flujo editorial recomendado.
- No recomendar modelos, nodos o flags inexistentes sin verificar.
- El mantenimiento de skills se rige por Desarrollo y `skill_creacion_skills.md`.
- Todo cambio de skills debe aplicar concision, activacion clara, progressive disclosure, referencias a un nivel, scripts reutilizables cuando proceda y validacion realista.
- Todo cambio de protocolos, scripts, skills o flujos debe registrarse en `../00_red_semantica_operativa/02_Historico_Desarrollos.md`.
- No modificar repos externos de modelos o herramientas; solo documentar, instalar o crear fork propio si Santiago lo pide.

## Backup

Antes de cambiar protocolos o scripts:

```powershell
py "05_scripts\health_check_ilustracion.py" --backup
```

Despues:

```powershell
py "05_scripts\health_check_ilustracion.py"
```
