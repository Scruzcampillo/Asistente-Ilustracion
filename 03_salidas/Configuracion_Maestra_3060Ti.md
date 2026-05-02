# Configuración Maestra — RTX 3060 Ti (8 GB VRAM)
> Este documento resume la configuración optimizada para tu hardware en mayo de 2026.

## 1. Flags de Lanzamiento (Pinokio / Windows)
Edita tu `start.json` o acceso directo de ComfyUI/Forge con estos parámetros:

**Para ComfyUI (Uso General / Flux GGUF):**
```bash
--lowvram --highvram-size 1024 --cuda-malloc --pin-shared-memory
```

**Para Forge (Velocidad en Flux NF4):**
```bash
--cuda-stream --pin-shared-memory --always-offload-from-vram
```

## 2. Checkpoints "Must-Have"
Descarga estos modelos de CivitAI/HuggingFace:
1. **Fotorrealismo Base:** [Juggernaut XL v9](https://civitai.com/models/133005)
2. **Retratos:** [RealVisXL V5.0](https://civitai.com/models/139562)
3. **Flux Práctico:** [Flux.1 dev GGUF Q4_0](https://huggingface.co/city96/FLUX.1-dev-gguf)

## 3. Pipeline de Producción Editorial
Para obtener la mejor calidad sin errores de memoria:

1. **Fase 1 (Generación):** SDXL @ 1024x1024, 28 pasos, Sampler `dpmpp_2m_sde`, Scheduler `karras`.
2. **Fase 2 (Identidad):** Nodo `IPAdapter Unified Loader` con `FaceID Plus V2`.
3. **Fase 3 (Refinado):** `FaceDetailer` (Impact Pack). 
   - Detector: `face_yolov8m.pt`.
   - SAM: `sam_vit_b_01ec64.pth`.
   - Denoise: 0.4 - 0.5.
4. **Fase 4 (Upscale):** `Ultimate SD Upscale`.
   - Upscaler: `4x-UltraSharp`.
   - Denoise: 0.25.
   - Upscale by: 2.0.

## 4. Gestión de Memoria en 16 GB RAM
- Cierra navegadores (Chrome/Edge) durante el proceso de Flux.
- El offload del encoder T5 consumirá ~10-12 GB de RAM del sistema.
- Usa `t5-v1_1-xxl-encoder-Q4_K_M.gguf` para ahorrar RAM sin perder calidad.
