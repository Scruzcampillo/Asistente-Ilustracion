# SKILL — Workflows y Modelos de IA (3060 Ti)
> Guía operativa para la generación de imágenes y herramientas de trabajo.

## 1. Modelos Recomendados (8 GB VRAM)

### Stable Diffusion XL (SDXL) — El estándar de producción
- **Juggernaut XL v9:** Generalista fotorrealista.
- **RealVisXL V5.0:** Retrato ultrarrealista.
- **epiCRealism XL:** Estética editorial/beauty.
- **CyberRealistic XL:** Composiciones cinematográficas.

### Flux.1 — Calidad Superior (Solo cuantizado)
- **Flux.1 dev GGUF (Q4_0 / Q5_0):** ~7 GB. Requiere offload de T5 a RAM. Usar en ComfyUI con `ComfyUI-GGUF`.
- **Flux.1 dev NF4 v2:** ~6-7 GB. Usar en Forge para mayor velocidad.
- **Flux.1 schnell GGUF Q4:** 4 pasos. Ideal para iteración rápida.

## 2. Gestión de Rostros e Identidad

| Herramienta | Cuándo usar | Requisito |
|---|---|---|
| **IPAdapter FaceID Plus V2** | Personaje recurrente en SDXL | Modelos FaceID + LoRA FaceID |
| **PuLID-Flux** | Consistencia de personaje en Flux | ComfyUI-PuLID-Flux |
| **InstantID** | Misma pose y rostro (clonado) | Solo SDXL, pesado en VRAM |
| **ReActor** | Face-swap rápido (post-gen) | Modelo Inswapper-128 |
| **FaceDetailer** | **Obligatorio** para calidad final | Impact Pack (YOLOv8m + SAM) |

## 3. Control de Composición (ControlNet)
- **xinsir Union ProMax:** El modelo "todo en uno" para SDXL. Cubre Canny, OpenPose, Depth, etc.
- **Strength:** Usar entre 0.5 y 0.85.
- **Scheduling:** Empezar en 0.0 y terminar en 0.8 para permitir refinado final.

## 4. Upscaling Editorial
- **Ultimate SD Upscale:** Técnica de tiles para superar el límite de VRAM.
- **Modelos Pixel-space:** 4x-UltraSharp (favorito), 4x_NMKD-Siax_200k (piel).
- **Parámetros Denoise:** 0.2 a 0.35 para añadir detalle sin alucinaciones.

## 5. Configuración de Software (Pinokio/Windows)
- **ComfyUI:** Usar `--lowvram` para Flux GGUF. Instalar `ComfyUI-Manager` como primer paso.
- **Forge:** Mejor gestor de memoria para Flux NF4. Activar `--cuda-stream` para 3060 Ti.
- **VAEs:** Usar `sdxl_vae_fp16_fix` para evitar NaNs en SDXL.

## 6. Pipeline Óptimo Sugerido
1. Generar base 1024x1024 con SDXL (Juggernaut/RealVisXL).
2. Aplicar IPAdapter FaceID para identidad.
3. Pasar por FaceDetailer (Denoise 0.45).
4. Ultimate SD Upscale 2x con 4x-UltraSharp (Denoise 0.25).
