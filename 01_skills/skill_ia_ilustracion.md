---
Creada: 2026-05-04
Actualizada: 2026-05-13T11:14
tipo: skill
asistente: "[[Asistente Ilustracion]]"
estado: activo
convencion: hibrida
tags:
  - skill
  - ilustracion
  - ia
  - comfyui
  - flux
  - sdxl
relaciones:
  - "[[Asistente Ilustracion]]"
  - "[[Asistente de Desarrollo]]"
  - "[[skill_codigo]]"
tipo_tarea:
  - direccion_visual
  - investigacion_general
agentes_recomendados:
  - ChatGPT
  - Gemini (generalidades)
criterio_agente: ChatGPT estructura prompts y restricciones; Gemini puede ampliar referencias visuales generales.
---
# skill_ia_ilustracion.md - Workflows y modelos de IA local

## Mapa semantico

- Nodo propietario: [[Asistente Ilustracion]]
- Soporte tecnico: [[Asistente de Desarrollo]], [[skill_codigo]]
- Documentacion relacionada: `02_conocimiento/Documentacion_IA_Ilustracion.md`

## Cuando cargar este skill

Cargar cuando Santiago pida asesoramiento, configuracion o generacion de workflows visuales con IA local: SDXL, Flux, ComfyUI, Forge, Pinokio, consistencia de rostro, ControlNet, FaceDetailer o upscaling editorial.

No cargar para tareas editoriales de texto ni para modificar repos externos de modelos o herramientas. Si la tarea implica codigo o scripts propios, coordinar con Desarrollo.

## Proposito

Definir workflows ejecutables para produccion visual IA en hardware de gama media, priorizando calidad fotorrealista sin romper el limite de 8 GB de VRAM.

## Fuentes y dependencias

- `AGENTS.MD`: modalidades y regla de oro de 8 GB.
- `00_system/rol_base.md`: identidad, hardware y stack.
- `00_system/nucleo_salud.md`: contratos de salud y frontera externa.
- `02_conocimiento/Documentacion_IA_Ilustracion.md`: documentacion tecnica ampliada.
- Herramientas objetivo: ComfyUI, Forge y Pinokio.

## Flujo operativo

1. Identificar objetivo visual: retrato, identidad recurrente, composicion, upscale, batch o diagnostico.
2. Verificar restricciones de hardware: RTX 3060 Ti, 8 GB VRAM, 16 GB RAM.
3. Elegir base:
   - SDXL para flujo seguro y calidad editorial;
   - Flux solo cuantizado o con offload claro.
4. Definir control de identidad, composicion y mejora facial si aplica.
5. Definir upscaling por tiles si se necesita mas resolucion.
6. Advertir riesgos de OOM o lentitud cuando el flujo sea pesado.
7. Entregar pasos, parametros o JSON de workflow segun la modalidad.

## Reglas criticas

- Nunca proponer flujos que ignoren el limite de 8 GB de VRAM.
- No recomendar modelos, nodos o flags inexistentes sin verificar.
- No modificar repos externos de modelos o herramientas; instalar/documentar o crear fork solo si Santiago lo pide.
- Priorizar ComfyUI para pipelines complejos.
- Priorizar Forge para velocidad en Flux.
- En fotorrealismo, separar generacion, identidad, control de composicion y upscale.

## Modelos recomendados

### SDXL

- Juggernaut XL v9: generalista fotorrealista.
- RealVisXL V5.0: retrato ultrarrealista.
- epiCRealism XL: estetica editorial/beauty.
- CyberRealistic XL: composiciones cinematograficas.

### Flux cuantizado

- Flux.1 dev GGUF Q4/Q5: requiere offload de T5 a RAM y ComfyUI-GGUF.
- Flux.1 dev NF4 v2: usar en Forge para mejor velocidad.
- Flux.1 schnell GGUF Q4: iteracion rapida.

## Rostros e identidad

| Herramienta | Uso | Requisito |
|---|---|---|
| IPAdapter FaceID Plus V2 | Personaje recurrente en SDXL | Modelos FaceID + LoRA FaceID |
| PuLID-Flux | Consistencia de personaje en Flux | ComfyUI-PuLID-Flux |
| InstantID | Misma pose y rostro | Solo SDXL, pesado en VRAM |
| ReActor | Face-swap rapido post-gen | Modelo Inswapper-128 |
| FaceDetailer | Calidad final | Impact Pack |

## Control de composicion

- xinsir Union ProMax para SDXL: Canny, OpenPose, Depth y otros controles.
- Strength recomendado: 0.5 a 0.85.
- Scheduling recomendado: iniciar 0.0 y terminar 0.8 para permitir refinado final.

## Upscaling editorial

- Ultimate SD Upscale con tiles.
- Modelos favoritos: 4x-UltraSharp, 4x_NMKD-Siax_200k para piel.
- Denoise: 0.2 a 0.35 para detalle sin alucinacion.

## Pipeline sugerido

1. Generar base 1024x1024 con SDXL.
2. Aplicar IPAdapter FaceID si hay identidad recurrente.
3. Pasar por FaceDetailer.
4. Aplicar Ultimate SD Upscale 2x con denoise moderado.

## Validacion y cierre

Checklist:

- [ ] respeta 8 GB VRAM;
- [ ] indica modelo base;
- [ ] indica herramienta recomendada;
- [ ] advierte OOM si aplica;
- [ ] no inventa nodos, modelos ni rutas locales;
- [ ] separa generacion, identidad, composicion y upscale.

Si se modifica este skill:

```powershell
py "05_scripts\health_check_ilustracion.py"
```
