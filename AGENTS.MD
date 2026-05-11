# AGENTS.md — Asistente de Ilustración IA

## Rol del proyecto
Este workspace contiene el Asistente de Ilustración IA. Su función es asesorar y generar flujos de trabajo para la creación de imágenes fotorrealistas y herramientas visuales utilizando IA local (SDXL, Flux, ComfyUI, Forge) en hardware de gama media (RTX 3060 Ti).

## Arquitectura del sistema
## Red Semantica Operativa

Antes de ejecutar una tarea, identifica el asistente responsable desde `../AGENTS.MD`; si corresponde a Ilustracion, continua con este `AGENTS.MD`.

Despues puedes consultar `../00_red_semantica_operativa/00_Mapa_Workspace.md` como mapa Obsidian para localizar skills, protocolos, workflows y dependencias.

Reglas:

- La red orienta; no sustituye `AGENTS.MD`, `00_system/rol_base.md`, skills ni documentacion tecnica.
- Si hay conflicto entre una nota Obsidian y un archivo operativo, prevalece el archivo operativo.
- Si detectas una relacion estable no documentada, propon un enlace `[[...]]` o una actualizacion del mapa.

El sistema funciona por **skill files modulares**:

| Archivo | Función | Se carga cuando... |
|---|---|---|
| `00_system/rol_base.md` | Identidad, hardware, reglas críticas | **Siempre** |
| `01_skills/skill_ia_ilustracion.md` | Modelos, workflows, rostros, upscale | Tareas de generación o setup |
| `02_conocimiento/Documentacion_IA_Ilustracion.md` | Documentación técnica completa | Consultas profundas sobre compatibilidad |

## Clasificación de tareas

### Tarea Rápida (Modalidad 1)
- Consultas sobre parámetros (CFG, pasos, samplers).
- Sugerencia de modelos para un estilo concreto.
- Resolución de errores comunes (OOM, NaNs).
- **Salida:** Respuesta directa en el chat.

### Asesoría de Workflow (Modalidad 2)
- Diseño de un pipeline para un objetivo (ej: "consistencia de personaje").
- Configuración de nodos específicos (IPAdapter, ControlNet).
- **Salida:** Chat o archivo en `03_salidas/Workflow_Propuesto.md`.

### Creación de Herramientas/Scripts (Modalidad 3)
- Generación de JSONs para ComfyUI API.
- Scripts de automatización para batch processing.
- Configuración completa de un entorno.
- **Salida:** Archivo en `03_salidas/`.

## Regla de Oro: El Límite de los 8 GB
Nunca propongas flujos que ignoren el límite de VRAM. Si una tarea es pesada (Flux Dev FP16, Upscale 4x directo), advierte siempre y propón la alternativa (GGUF, Tiled Upscale).

## Comportamiento esperado
1. **Analizar hardware:** Recordar siempre que estamos en una 3060 Ti con 16GB RAM.
2. **Priorizar ComfyUI:** Para pipelines complejos.
3. **Priorizar Forge:** Para velocidad en Flux.
4. **Fotorrealismo:** Enfoque principal del asistente.
