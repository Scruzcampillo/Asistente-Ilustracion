---
Creada: 2026-05-08T13:50
Actualizada: 2026-05-13T10:01
---
# Skills - Asistente Ilustracion

Fuente canonica: `skill_ia_ilustracion.md`.

## Responsabilidad

Definir modelos, workflows y decisiones tecnicas para produccion visual IA.

## Areas

| Area | Responsabilidad |
|---|---|
| Modelos | Elegir SDXL o Flux cuantizado segun objetivo y VRAM |
| Rostros | IPAdapter, PuLID, InstantID, ReActor y FaceDetailer |
| Composicion | ControlNet y condicionamiento visual |
| Upscale | Tiled upscale y preparacion editorial |
| Software | Pinokio, Windows, ComfyUI y Forge |

## Regla

La calidad visual no justifica romper el limite del equipo. Diseñar flujos que puedan ejecutarse.

## Mantenimiento de skills

La creacion, mejora o actualizacion de estos skills se gobierna desde `../../Asistente de Desarrollo/01_skills/skill_creacion_skills.md`. Antes de cambiar workflows visuales, entrar por Desarrollo y validar que las recomendaciones siguen siendo ejecutables en el equipo disponible.

Todo cambio debe aplicar el estandar obligatorio de buenas practicas de skills definido por Desarrollo: concision, activacion clara, progressive disclosure, referencias a un nivel, scripts reutilizables cuando proceda, validacion realista y registro en `../../00_red_semantica_operativa/02_Historico_Desarrollos.md`.

Convencion hibrida: los `skill_*.md` conservan su nombre y anaden frontmatter semantico para Obsidian (`tipo`, `asistente`, `tags`, `relaciones`) mas `Mapa semantico` con wikilinks visibles.
