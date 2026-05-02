# Guía de instalación: Workflow Face + Composition Swap

> **Objetivo:** Cambiar la persona de una escena fotográfica de referencia y modificar un elemento de la acción (ej: pipeta → microscopio) con fotorrealismo extremo y sin filtros de contenido.

---

## Resumen del flujo
`Foto escena base` + `Foto de la persona nueva` → ControlNet Depth (preserva composición) + IPAdapter FaceID (inyecta el rostro) → KSampler (genera la escena con la nueva persona y acción) → FaceDetailer (pule piel y ojos) → Imagen final.

---

## PASO 1 — Checkpoint (modelo base)

### RealVisXL V5.0 *(el más indicado para piel, ojos y realismo en retratos)*
- **Descarga:** https://civitai.com/models/139562/realvisxl-v50
- **Archivo:** `RealVisXL_V5.0.safetensors` (~6.5 GB)
- **Carpeta destino:** `ComfyUI/models/checkpoints/`
- **VAE incluido:** sí (baked-in, no necesitas VAE externo)

> ⚠️ Alternativa si quieres una estética más cinematográfica: **Juggernaut XL v9** (https://civitai.com/models/133005). En ese caso, descarga también `sdxl_vae_fp16_fix.safetensors` (ver más abajo).

---

## PASO 2 — VAE de seguridad (por si aparecen bandas o colores saturados)

### SDXL VAE FP16 Fix
- **Descarga:** https://huggingface.co/madebyollin/sdxl-vae-fp16-fix
- **Archivo:** `sdxl_vae_fp16_fix.safetensors` (~335 MB)
- **Carpeta destino:** `ComfyUI/models/vae/`

---

## PASO 3 — ControlNet (estructura de la escena)

### xinsir ControlNet Union SDXL ProMax *(un solo modelo para todo: depth, canny, pose, tile...)*
- **Descarga:** https://huggingface.co/xinsir/controlnet-union-sdxl-1.0
  - Archivo específico: `controlnet-union-sdxl-promax.safetensors` (~2.5 GB)
- **Carpeta destino:** `ComfyUI/models/controlnet/`

> El workflow usa este modelo en **modo depth** vía el nodo `SetUnionControlNetType`. Con un solo archivo cubres el 95% de casos futuros.

---

## PASO 4 — Modelos para IPAdapter FaceID Plus V2

Necesitas **cuatro archivos** de dos repositorios diferentes:

### 4a. Adapter + LoRA FaceID
- **Repositorio:** https://huggingface.co/h94/IP-Adapter-FaceID
- **Archivos necesarios:**
  - `ip-adapter-faceid-plusv2_sdxl.bin` (~700 MB) → `ComfyUI/models/ipadapter/`
  - `ip-adapter-faceid-plusv2_sdxl_lora.safetensors` (~150 MB) → `ComfyUI/models/loras/`

### 4b. CLIP Vision
- **Repositorio:** https://huggingface.co/h94/IP-Adapter
- **Archivo necesario:**
  - `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` (~2.5 GB) → `ComfyUI/models/clip_vision/`

### 4c. InsightFace (detector facial) — se descarga solo la primera vez
- Se descarga automáticamente a `ComfyUI/models/insightface/models/antelopev2/` en el primer uso.
- Si falla, descarga manualmente desde: https://drive.google.com/file/d/18wEUfMNohBJ4K3Ly5wpTejPfDzp-8fI8/view
- Descomprime y deja la carpeta `antelopev2/` en `ComfyUI/models/insightface/models/`

---

## PASO 5 — Modelos para FaceDetailer (Impact Pack)

### Detector de caras YOLOv8
- **Descarga:** https://huggingface.co/Ultralytics/assets/resolve/main/face_yolov8m.pt
- **Archivo:** `face_yolov8m.pt` (~50 MB)
- **Carpeta destino:** `ComfyUI/models/ultralytics/bbox/`

### SAM (Segment Anything) para máscara precisa
- **Descarga:** https://huggingface.co/segments-arnaud/sam_vit_b/resolve/main/sam_vit_b_01ec64.pth
- **Archivo:** `sam_vit_b_01ec64.pth` (~360 MB)
- **Carpeta destino:** `ComfyUI/models/sams/`

---

## PASO 6 — Custom nodes (vía ComfyUI Manager)

Instala en este orden desde **Manager → Custom Nodes Manager → buscar nombre → Install → Restart**:

| Nodo | Nombre exacto en el Manager | Para qué |
|---|---|---|
| **ComfyUI_IPAdapter_plus** | `ComfyUI_IPAdapter_plus` | Nodo IPAdapter FaceID |
| **comfyui_controlnet_aux** | `comfyui_controlnet_aux` | Preprocesador Depth |
| **ComfyUI-Impact-Pack** | `ComfyUI-Impact-Pack` | FaceDetailer |
| **ComfyUI-Impact-Subpack** | `ComfyUI-Impact-Subpack` | Detector YOLOv8 (requerido por Impact Pack desde v8) |

> Si ComfyUI Manager no está instalado: https://github.com/Comfy-Org/ComfyUI-Manager

---

## PASO 7 — Cómo usar el workflow

1. **Abre ComfyUI** y arrastra el archivo `workflow_face_composition_swap.json` al canvas.
2. En el nodo **"LoadImage" azul (1. BASE SCENE):** carga la foto del laboratorio (con la persona original).
3. En el nodo **"LoadImage" verde (2. FACE REFERENCE):** carga la foto de la persona nueva (solo el rostro, bien iluminado).
4. **Modifica el prompt positivo** (nodo verde grande): describe la acción nueva que quieres (ej: *"holding a microscope"* en lugar de *"holding a pipette"*).
5. En el nodo **CheckpointLoader:** asegúrate de que el nombre del archivo coincide exactamente con el que tienes descargado.
6. Dale a **Queue Prompt**.

---

## Ajustes finos recomendados

| Parámetro | Valor por defecto | Para más fidelidad a la escena | Para más libertad creativa |
|---|---|---|---|
| ControlNet strength | 0.65 | 0.80 | 0.45 |
| IPAdapter weight | 0.80 | 0.90 | 0.65 |
| FaceDetailer denoise | 0.45 | 0.35 | 0.55 |
| KSampler CFG | 6.5 | 5.0 | 7.5 |
| KSampler steps | 28 | 35 | 20 |

---

## Velocidades esperadas en RTX 3060 Ti

| Fase | Tiempo aproximado |
|---|---|
| KSampler (28 pasos, 1024×1024) | ~18-22 segundos |
| FaceDetailer (inpaint cara) | ~8-12 segundos |
| **Total por imagen** | **~30-35 segundos** |

---

## Notas importantes

- **Sin filtros de contenido:** ComfyUI no bloquea nada por defecto con estos checkpoints. El sistema es editorialmente libre.
- **Si la cara no se parece suficiente:** sube el IPAdapter weight a 0.90. Si empieza a perder la iluminación del laboratorio, bájalo.
- **Si la escena no respeta la composición:** sube el ControlNet strength a 0.75–0.80.
- **Si aparecen artefactos o manchas:** Reduce el FaceDetailer denoise a 0.35.
- **Si el modelo no detecta la cara** (raro con RealVisXL): Asegúrate de que `face_yolov8m.pt` está en la carpeta correcta y que `ComfyUI-Impact-Subpack` está instalado.

---

*Workflow creado: Mayo 2026 — RTX 3060 Ti 8GB — ComfyUI + SDXL*
