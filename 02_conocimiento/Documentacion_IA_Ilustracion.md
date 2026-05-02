# Investigación técnica: IA local de generación fotorrealista en RTX 3060 Ti (8 GB VRAM) con ComfyUI + Pinokio

**Resumen ejecutivo (qué se recomienda en tu hardware):** Con una RTX 3060 Ti de 8 GB, i7-12700F y 16 GB de RAM, el "punto dulce" en mayo de 2026 sigue siendo **SDXL fine-tunes fotorrealistas** (Juggernaut XL, RealVisXL, epiCRealism XL, CyberRealistic XL) ejecutados en **ComfyUI** o **Forge**. **Flux.1 dev** es viable pero solo en variantes cuantizadas: **GGUF Q4_0 / Q5_0 (≈7 GB)** o **NF4 v2 (≈6–7 GB)**, ambas con offload del encoder T5 a RAM. **Flux.1 schnell GGUF Q4** corre en 4 pasos y es la opción "Flux práctica" para 8 GB. Flux pro no es ejecutable localmente (solo API). Para consistencia de rostro, IPAdapter FaceID Plus V2 sobre SDXL es lo más ligero; **PuLID-Flux** y **InstantID** funcionan en 8 GB pero al límite. Las 16 GB de RAM del sistema son el principal cuello de botella secundario: la cuantización agresiva más Forge (mejor offloader) o ComfyUI con `--lowvram` son obligatorios para Flux. SDXL fluye sin trucos.

---

## 📑 Índice Rápido
- **[BLOQUE 1 — Arquitecturas y Modelos](#bloque-1--arquitecturas-y-modelos-principales)**
  - [1.1 Estado del arte](#11-estado-del-arte-en-mayo-2026) | [1.2 Checkpoints 8GB](#12-mejores-checkpoints-fotorrealistas-para-8-gb-todos-sdxl-salvo-indicación) | [1.5 Viabilidad Flux vs SDXL](#15-viabilidad-por-modelo-en-rtx-3060-ti-8-gb--16-gb-ram)
- **[BLOQUE 2 — ComfyUI a fondo](#bloque-2--comfyui-a-fondo)**
  - [2.2 Nodos centrales](#22-pipeline-canónico-txt2img-y-los-nodos-centrales) | [2.5 Custom nodes esenciales](#25-custom-nodes-esenciales-todos-instalables-vía-comfyui-manager) | [2.7 Workflows](#27-workflows-preconstruidos-para-fotorrealismo)
- **[BLOQUE 3 — Rostros y Consistencia](#bloque-3--gestión-de-rostros-y-consistencia)**
  - [3.1 IPAdapter+FaceID](#31-ipadapter--faceid) | [3.2 InstantID](#32-instantid) | [3.3 ReActor](#33-reactor-face-swap) | [3.4 FaceDetailer](#34-facedetailer-impact-pack) | [3.5 Comparativa](#35-comparativa-reactor-vs-ipadapter-faceid-vs-instantid-vs-pulid)
- **[BLOQUE 4 — ControlNet (SDXL y Flux)](#bloque-4--controlnet-y-control-de-composición)**
- **[BLOQUE 5 — Upscaling y post-procesado](#bloque-5--upscaling-y-post-procesado)**
  - [5.1 Ultimate SD Upscale](#51-ultimate-sd-upscale) | [5.2 Modelos Pixel-space](#52-modelos-de-upscale-pixel-space)
- **[BLOQUE 6 — Filtros de seguridad](#bloque-6--filtros-de-seguridad-y-control-editorial)**
- **[BLOQUE 7 — Software: Forge vs ComfyUI vs Pinokio](#bloque-7--otros-sistemas-y-alternativas)**
- **[BLOQUE 8 — Recursos y Documentación](#bloque-8--recursos-y-documentación)**
- **[🏁 Recomendación final para 3060 Ti](#recomendación-final-concreta-para-tu-setup)**

---

## BLOQUE 1 — Arquitecturas y modelos principales

### 1.1 Estado del arte en mayo 2026

Tres familias dominan el fotorrealismo de código abierto/peso abierto:

- **Stable Diffusion XL (SDXL 1.0)** — UNet de 3.5 B parámetros + refiner de 6.6 B, dos text encoders (CLIP-L + OpenCLIP-G), resolución nativa 1024×1024. Requisito oficial: 8 GB VRAM. Es el ecosistema **más grande con diferencia**: >50 000 LoRAs en CivitAI, todos los ControlNets imaginables, IPAdapter, InstantID, PuLID, ReActor. Para una 3060 Ti es la base lógica.
- **Flux.1 (Black Forest Labs, ex-Stability AI)** — Diffusion Transformer (DiT) de 12 B parámetros + text encoder T5-XXL (4.5 B) + CLIP-L. En FP16 puro pide ~33 GB; en FP8 unos 17 GB; en NF4 v2 unos 6–8 GB; en GGUF Q4_0 unos 7 GB de pesos del DiT más T5 ofloadable a CPU. Calidad de prompt-following y texto en imagen claramente superiores a SDXL. **Flux 2 Dev** apareció a finales de 2025 como sucesor con mejor calidad pero con requisitos similares o mayores; no se considera práctico para 8 GB salvo en ComfyUI con cuantización extrema.
- **Stable Diffusion 3.5 Large (Stability AI)** — MMDiT 2.5 B + triple text encoder (T5-XXL + CLIP-L + OpenCLIP-G ≈ 5.5 B). FP16 ≈ 18 GB; en FP8 ≈ 10 GB. Mejor texto y composición que SDXL pero ecosistema mucho menor que SDXL/Flux. En 8 GB se puede correr cuantizado, con velocidades modestas.

Otras arquitecturas que verás citadas pero **no recomendadas** para 8 GB de VRAM en producción fotorrealista: Qwen Image (Alibaba, 20 B DiT), HiDream-I1 (full 17 B; la versión NF4 corre en 16 GB), Hunyuan Image 3 (84 B MoE). **PixArt-Sigma** sí es viable a 12 GB+.

### 1.2 Mejores checkpoints fotorrealistas para 8 GB (todos SDXL salvo indicación)

Modelos que ejecutan sin offloading agresivo y tienen el mejor compromiso calidad/velocidad en una 3060 Ti:

| Modelo (versión actual) | Especialidad | Página |
|---|---|---|
| **Juggernaut XL v9 / Lightning v10** | Generalista fotográfico, retratos, escenas urbanas, full body | civitai.com/models/133005 |
| **RealVisXL V5.0** | Retrato ultrarrealista de personas, ojos, piel, animales reales | civitai.com/models/139562 |
| **epiCRealism XL ("Last FAME" / "Crystal Clear")** | Editorial, beauty, microexpresiones, piel | civitai.com/models/277058 |
| **CyberRealistic XL** | Composiciones difíciles, poses inusuales, cinematográfico | civitai.com/models/312530 |
| **Realism Engine SDXL v2.0** | Retratos limpios "estudio" (modelo más antiguo pero estable) | civitai.com/models/152525 |
| **NightVision XL (Photorealistic Portrait)** | Retrato con grano filmico | civitai.com/models/128607 |
| **DreamShaper XL Turbo / Lightning** | Sci-fi, fantasy con look fotográfico (8 pasos) | civitai.com/models/112902 |

Para la **versión SD 1.5** si quieres ahorrar VRAM y velocidad (4 GB suficientes):
- **Realistic Vision V5.1 / V6.0 B1** — sigue siendo el referente fotográfico a 512–768 px (civitai.com/models/4201).
- **epiCRealism Natural Sin** — versión 1.5 ligera y sin "look plástico".
- **CyberRealistic v9.0**.

Modelos fuera de fotorrealismo que conviene conocer pero no aplican al brief:
- **Pony Diffusion V6 XL / V7** — Furry/anime con score-tags, no fotográfico, gran ecosistema.
- **Illustrious XL** — anime, no fotográfico.
- **Animagine XL** — anime.

### 1.3 Modelos por nicho específico

- **Retratos ultrarrealistas:** RealVisXL V5.0 + Portrait Master (custom node `florestefano1975/comfyui-portrait-master`) + FaceDetailer + un IPAdapter FaceID. Para Flux: PuLID-Flux con un Flux GGUF Q5 y una LoRA de skin texture.
- **Imagen científica / laboratorio / médica:** SDXL base no está afinado a este dominio. Combinaciones recomendadas: **Juggernaut XL** + LoRAs específicas ("Scientific Illustration", "Microscopy", "Medical Photography" en CivitAI) + ControlNet Depth/Canny si tienes referencias. Flux dev es notablemente mejor al renderizar texto y diagramas; en ese caso usar Flux GGUF Q5 + LoRA "BFL_Medical" si la encuentras. Para microscopía pura, considerar **PixArt-Sigma** (mejor con prompts largos descriptivos).
- **Fotografía de producto / e-commerce:** RealVisXL V5.0 + ControlNet Canny + IPAdapter para coherencia de marca. **EcomXL inpaint/softedge ControlNets** existen específicamente para producto. Workflows en CivitAI con tag "product photography" (>1k descargas).
- **Escenas históricas:** Juggernaut XL + LoRAs históricas (CivitAI tag "historical period"), o Flux dev (mucho mejor compositor). Útil ControlNet OpenPose para coreografía.
- **Editorial / portada:** epiCRealism XL Crystal Clear + LoRA de "film grain" o "Kodak Portra"; FluxGuidance entre 2.5–3.5 si usas Flux. Ratios 832×1216 (3:4) y 1024×1024 son los nativos seguros en SDXL.

### 1.4 VAEs

- SDXL: VAE oficial **sdxl_vae.safetensors** (Stability AI, HuggingFace `stabilityai/sdxl-vae`). Algunos checkpoints incluyen "baked-in VAE" (Juggernaut, RealVis), entonces no necesitas cargar otro. Si ves saturación o bandas, usa el "fixed" `sdxl_vae_fp16_fix` (madebyollin/sdxl-vae-fp16-fix) que evita NaN en FP16.
- Flux: VAE = `ae.safetensors` (a veces llamado `flux_ae.safetensors`), distribuido por BFL en HuggingFace `black-forest-labs/FLUX.1-dev`. Va a `ComfyUI/models/vae/`.
- SD 1.5: `vae-ft-mse-840000-ema-pruned.safetensors` es el clásico.

### 1.5 Viabilidad por modelo en RTX 3060 Ti 8 GB / 16 GB RAM

| Modelo | Variante | VRAM real | Velocidad aprox 1024² | Veredicto 3060 Ti |
|---|---|---|---|---|
| SD 1.5 + checkpoint realista | FP16 | 3–4 GB | ~3–6 it/s | Muy fluido |
| SDXL fine-tune (Juggernaut, RealVisXL) | FP16 | 7–8 GB | ~1.3–1.8 it/s | Fluido, sin offload |
| SDXL + ControlNet + LoRA | FP16 | 8 GB justo | ~0.9–1.2 it/s | Funcional |
| SDXL + IPAdapter FaceID + ControlNet | FP16 | 8 GB+ | con offload menor | Funcional con --medvram |
| Flux.1 dev | FP16 | 23 GB+ | imposible | **Inviable** |
| Flux.1 dev | FP8 (Comfy-Org) | 11–13 GB | ~0.07–0.1 it/s con offload pesado | Inviable salvo offload masivo a RAM (lento) |
| Flux.1 dev | NF4 v2 (Forge) | 6–7 GB | ~1.5–2.5 s/step | **Sí, usar Forge** |
| Flux.1 dev | GGUF Q4_0 (city96) | 7 GB + T5 en RAM | ~2 s/step (3060 Ti) | **Sí, opción ComfyUI** |
| Flux.1 dev | GGUF Q5_1 / Q6 | 8–9 GB | T5 ofloadeado | Justo, viable con paciencia |
| Flux.1 dev | GGUF Q8 | 12–13 GB | offloading alto | Solo con CPU offload pesado (lento, ~5–10 min) |
| Flux.1 schnell | NF4 / Q4 | 6–7 GB | 4 pasos totales | **Excelente para iterar** |
| Flux.1 pro | API only | — | — | Imposible local |
| SD 3.5 Large | FP8 | 10–11 GB | con offload | Marginal |
| SD 3.5 Medium | FP16 | 8 GB | ~1 it/s | Viable |
| HiDream-I1 NF4 | NF4 | 16 GB | — | Inviable |
| Qwen Image | Q4 GGUF | 12–14 GB | — | Inviable |

Fuentes para descarga:
- HuggingFace `black-forest-labs/FLUX.1-dev` y `FLUX.1-schnell` (pesos oficiales).
- HuggingFace `city96/FLUX.1-dev-gguf` y `city96/FLUX.1-schnell-gguf` (GGUF Q2…Q8).
- HuggingFace `lllyasviel/FLUX.1-dev-bnb-nf4` (NF4 para Forge, archivo `flux1-dev-bnb-nf4-v2.safetensors`).
- HuggingFace `Comfy-Org/flux1-dev` y `Comfy-Org/flux1-schnell` (FP8 listos para ComfyUI).
- CivitAI: gran mayoría de fine-tunes SDXL.

---

## BLOQUE 2 — ComfyUI a fondo

### 2.1 Arquitectura interna

ComfyUI es un **GUI de grafo basado en LiteGraph** sobre un backend Python/PyTorch que ejecuta los workflows como un **DAG (grafo dirigido acíclico)**. La arquitectura es cliente-servidor: el frontend JavaScript edita el grafo y lo serializa como JSON ("prompt" en la jerga de la API), y el backend lo recibe vía REST/WebSocket, lo construye como `DynamicPrompt`, calcula el orden topológico (`ExecutionList`) y solo ejecuta los nodos cuyas salidas son necesarias y cuyas entradas han cambiado desde la última ejecución (lazy evaluation).

Tres mecanismos clave del motor:
1. **Cache jerárquica**: tres modos elegibles por línea de comandos: `Classic` (limpia agresivamente), `LRU` (`--cache-lru N`), y `Dependency-Aware` (limpia entradas cuando cambian dependencias). La firma de cache combina hash de inputs y `IS_CHANGED()` por nodo.
2. **Topological sorting con UX**: prioriza nodos de salida y nodos asíncronos primero, lo que permite mostrar previews antes de terminar.
3. **Subgraphs / Group Nodes**: encapsulación reutilizable. Subgraphs (modernos, mantenidos) usan blueprint registry; Group Nodes (legacy) serializan en el workflow.

Documentación oficial de la arquitectura: <https://docs.comfy.org/development/core-concepts/nodes> y el deepwiki <https://deepwiki.com/Comfy-Org/ComfyUI>.

### 2.2 Pipeline canónico txt2img y los nodos centrales

Un workflow mínimo SDXL contiene:

```
Load Checkpoint → CLIP Text Encode (positivo) ┐
                ↘ CLIP Text Encode (negativo) ┤→ KSampler → VAE Decode → Save Image
                ↘ Empty Latent Image ──────────┘
```

Categorías de nodos (Comfy Core):

- **Loaders**: `CheckpointLoaderSimple`, `UNETLoader` (para Flux/SD3 separados), `CLIPLoader`, `DualCLIPLoader` (Flux/SD3), `VAELoader`, `LoraLoader`, `LoraLoaderModelOnly`, `ControlNetLoader`, `IPAdapterUnifiedLoader`, `Unet Loader (GGUF)` del nodo `ComfyUI-GGUF`.
- **Conditioning / texto**: `CLIPTextEncode` (estándar), `CLIPTextEncodeSDXL` (encoder dual con scores estéticos), `CLIPTextEncodeFlux`, `FluxGuidance` (controla la influencia del prompt en Flux con un valor ~2.5–4.0; Flux **no usa CFG** clásico), `ConditioningCombine`, `ConditioningSetTimestepRange` (para regional / scheduling), `ConditioningSetMask`.
- **Sampling**: `KSampler` (todo en uno: model, positive, negative, latent, seed, steps, cfg, sampler_name, scheduler, denoise) y `KSamplerAdvanced` (separa add_noise, start_at_step, end_at_step, return_with_leftover_noise, ideal para refiner / hi-res). Samplers comunes: `dpmpp_2m`, `dpmpp_2m_sde`, `euler`, `euler_a`, `lcm`, `dpmpp_3m_sde_gpu`. Schedulers: `karras`, `normal`, `simple`, `sgm_uniform`, `beta`.
- **Latents**: `EmptyLatentImage` (txt2img), `EmptySD3LatentImage`, `VAEEncode` (img2img: imagen → latente), `VAEDecode` (latente → imagen), `LatentUpscale`, `LatentUpscaleBy`, `SetLatentNoiseMask` (inpainting), `RepeatLatentBatch`.
- **Imagen**: `LoadImage`, `SaveImage`, `PreviewImage`, `ImageScale`, `ImageInvert`, `ImagePadForOutpaint`, `ImageBlend`, `ImageCompositeMasked`.
- **ControlNet**: `ControlNetApply`, `ControlNetApplyAdvanced`, `SetUnionControlNetType` (para xinsir Union ProMax), preprocesadores en `ComfyUI's-ControlNet-Aux`.
- **Modelo / sampling avanzado**: `ModelSamplingDiscrete`, `ModelSamplingFlux`, `ModelSamplingSD3`, `RescaleCFG`, `FreeU_V2`, `PerturbedAttentionGuidance`.

Catálogo completo: <https://comfyui-wiki.com/en/comfyui-nodes>.

### 2.3 Estructura JSON del workflow

ComfyUI guarda dos formatos: el **workflow** (el grafo con posiciones, colores, vínculos) y el **prompt** (la representación que va al servidor). El JSON del workflow tiene la forma:

```json
{
  "last_node_id": 9,
  "last_link_id": 14,
  "nodes": [
    {"id": 4, "type": "CheckpointLoaderSimple", "pos": [-100, 200],
     "widgets_values": ["juggernautXL_v9.safetensors"],
     "outputs": [{"name":"MODEL","type":"MODEL","links":[1]}, ...]},
    ...
  ],
  "links": [[1, 4, 0, 3, 0, "MODEL"], ...],
  "groups": [...],
  "config": {},
  "extra": {},
  "version": 0.4
}
```

Cada `link` es una tupla `[link_id, from_node, from_slot, to_node, to_slot, type]`. Los workflows se **importan arrastrando** un PNG con metadatos o un JSON al canvas. Los PNG generados por ComfyUI llevan el workflow en sus metadatos PNGInfo (parámetro `workflow`), por eso al arrastrar una imagen reconstruye todo. Para deshabilitar embedding del workflow en imágenes ver `--no-metadata` o el flag de privacidad.

Exportar: `Workflow → Export` (JSON puro) o `Save (API Format)` para llamadas programáticas.

### 2.4 Sistema de colas y batch

- "Queue Prompt" añade el grafo a la cola del backend; varias entradas a la cola se procesan secuencialmente (no en paralelo, salvo con instancias separadas).
- Para batch: subir `batch_size` en `EmptyLatentImage` (genera N imágenes en paralelo en un solo paso —usa más VRAM— ) o iterar con incrementos de seed (`Seed (rgthree)` con modo `increment`).
- El nodo **Queue** del menú permite ver/cancelar/repetir.
- Para **batch sobre lista de imágenes**: `Image Loader (Batch)` de WAS Node Suite o el nodo `ImageBatchMultiple` de Impact Pack, combinado con `For Loop` de comfy-easy-use.
- API: enviar POST a `/prompt` con el prompt en formato API.

### 2.5 Custom nodes esenciales (todos instalables vía ComfyUI-Manager)

| Custom node | Repositorio | Para qué sirve |
|---|---|---|
| **ComfyUI-Manager** | <https://github.com/Comfy-Org/ComfyUI-Manager> | Gestor de nodos, snapshot, "Install Missing Nodes". Imprescindible. |
| **ComfyUI_IPAdapter_plus** (cubiq) | <https://github.com/cubiq/ComfyUI_IPAdapter_plus> | IPAdapter, FaceID, Plus, Composition (modo "1-image LoRA") |
| **ComfyUI_InstantID** (cubiq) | <https://github.com/cubiq/ComfyUI_InstantID> | InstantID nativo SDXL |
| **ComfyUI-PuLID-Flux** (balazik) y **ComfyUI_PuLID_Flux_ll** (lldacing) | balazik/ComfyUI-PuLID-Flux y lldacing/ComfyUI_PuLID_Flux_ll | PuLID para Flux |
| **comfyui_controlnet_aux** (Fannovel16) | <https://github.com/Fannovel16/comfyui_controlnet_aux> | Preprocesadores ControlNet (Canny, OpenPose DW, Depth Zoe/Midas, Lineart, MLSD, etc.) |
| **ComfyUI-Advanced-ControlNet** (Kosinkadink) | <https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet> | Scheduling, multi-ControlNet ponderado |
| **ComfyUI-Impact-Pack** (Dr.Lt.Data / ltdrdata) | <https://github.com/ltdrdata/ComfyUI-Impact-Pack> | **FaceDetailer**, SEGS, detection, iterative upscale, wildcards |
| **ComfyUI-Impact-Subpack** | <https://github.com/ltdrdata/ComfyUI-Impact-Subpack> | UltralyticsDetectorProvider (separado desde V8.0 del Impact Pack) |
| **ComfyUI-ReActor** (Gourieff) | <https://github.com/Gourieff/ComfyUI-ReActor> | Face swap (sucesor del antiguo `comfyui-reactor-node` que GitHub baneó) |
| **ComfyUI_UltimateSDUpscale** (ssitu) | <https://github.com/ssitu/ComfyUI_UltimateSDUpscale> | Tiled upscale |
| **WAS Node Suite** (WASasquatch) | <https://github.com/WASasquatch/was-node-suite-comfyui> | Cientos de nodos: filtros, máscaras, lógica, prompts, audio |
| **rgthree-comfy** | <https://github.com/rgthree/rgthree-comfy> | Reroute mejorado, Seed control, Power LoRA Loader, Context, Fast Muter, progress bar global |
| **ComfyUI-Custom-Scripts** (pythongosssss) | <https://github.com/pythongosssss/ComfyUI-Custom-Scripts> | QoL: autocomplete prompts, math, auto-arrange, notifications |
| **ComfyUI-GGUF** (city96) | <https://github.com/city96/ComfyUI-GGUF> | Carga de modelos GGUF (Flux, SD3, HiDream) |
| **ComfyUI-Easy-Use** (yolain) | <https://github.com/yolain/ComfyUI-Easy-Use> | Bundle de nodos "todo en uno" |
| **comfyui-portrait-master** (florestefano1975) | <https://github.com/florestefano1975/comfyui-portrait-master> | Generador de prompts para retratos |
| **ComfyUI-VideoHelperSuite** (Kosinkadink) | <https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite> | Carga/guarda video, batch frames |
| **facerestore_cf** (mav-rik) | <https://github.com/mav-rik/facerestore_cf> | Nodo CodeFormer/GFPGAN limpio |

### 2.6 Instalar custom nodes

Tres rutas, en orden de preferencia:

1. **ComfyUI-Manager → "Custom Nodes Manager" → buscar nombre → Install → Restart**. Es lo correcto en Pinokio porque respeta el entorno Python embebido.
2. **"Install via Git URL"** dentro del Manager — útil cuando el nodo no está aún registrado.
3. **Manual**: `cd ComfyUI/custom_nodes && git clone <url>`, luego instalar deps. En Pinokio el venv está en `pinokio/api/comfy.git/app/`. Para deps con el Python embebido portable: `..\..\..\python_embeded\python.exe -m pip install -r requirements.txt`. En Pinokio, después de `git clone`, hay que **abrir Terminal del app, hacer Stop y Run** para que Pinokio ejecute los `pip install` correctamente, según la wiki oficial <https://github.com/6Morpheus6/pinokio-wiki>.

### 2.7 Workflows preconstruidos para fotorrealismo

- **Templates oficiales** dentro de ComfyUI: menú `Workflow → Browse Templates` (Flux dev/schnell, SDXL básico, SD3.5, image-to-image, inpainting, upscale).
- **OpenArt** <https://openart.ai/workflows/home> — gran biblioteca con búsqueda; ojo: anuncian sunset el 18 de enero de 2026 (Pacific Time), exporta antes lo que necesites.
- **CivitAI workflows**: <https://civitai.com/articles> y filtrar por tipo "ComfyUI workflow", o tag "photorealistic".
- **RunComfy library** <https://www.runcomfy.com/comfyui-workflows> — workflows pulidos y comentados (pero requieren cuenta para descargar archivos completos).
- **comfyanonymous examples (oficiales)**: <https://comfyanonymous.github.io/ComfyUI_examples/> — aquí están los workflows canónicos (txt2img, img2img, inpaint, SDXL, Flux, controlnet, lora, hires fix, audio, video).
- **GitHub cubiq/ComfyUI_Workflows**: <https://github.com/cubiq/ComfyUI_Workflows> — workflows didácticos del autor de IPAdapter Plus (super recomendados, especialmente la sección upscale).
- **OpenModelDB**: <https://openmodeldb.info> — base de datos canónica de upscalers ESRGAN.

---

## BLOQUE 3 — Gestión de rostros y consistencia

### 3.1 IPAdapter + FaceID

**Cómo funciona**: el IPAdapter inyecta embeddings de imagen (vía un encoder CLIP-Vision o, en los modelos FaceID, vía InsightFace/ArcFace) directamente en las capas cross-attention del UNet. La variante **FaceID** usa el embedding facial (vector 512-d de ArcFace) como "1-image LoRA" + un LoRA cargable junto al embedding. Para mantener consistencia entre generaciones, se reutiliza la misma imagen de referencia y, opcionalmente, un batch de N imágenes del mismo sujeto promediadas.

**Modelos necesarios** (todos del repo `h94/IP-Adapter` y `h94/IP-Adapter-FaceID` en HuggingFace):

- `ip-adapter_sdxl_vit-h.safetensors` y `ip-adapter-plus_sdxl_vit-h.safetensors` → carpeta `ComfyUI/models/ipadapter/`
- `ip-adapter-faceid_sdxl.bin` y `ip-adapter-faceid-plusv2_sdxl.bin` → `models/ipadapter/`
- LoRA correspondiente **obligatoria**: `ip-adapter-faceid_sdxl_lora.safetensors`, `ip-adapter-faceid-plusv2_sdxl_lora.safetensors` → `models/loras/`
- CLIP-Vision: `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` → `models/clip_vision/`
- InsightFace **antelopev2** y **buffalo_l** se descargan automáticamente al primer uso a `models/insightface/` (FaceID Plus V2 prefiere buffalo_l/antelopev2 según versión).

**Uso del Unified Loader**: el nombre del archivo **debe coincidir exactamente** con la lista del README del repo. Workflow típico para SDXL FaceID v2:

```
LoadImage(face) → IPAdapter Unified Loader FaceID → IPAdapter Advanced (weight=0.8, weight_type="linear")
                                                          ↓ MODEL out → KSampler
```

**Configuración óptima en 8 GB VRAM**: weight 0.65–0.85; `weight_type="linear"` para preservar prompt, `"strong style"` para clonar; `start_at=0, end_at=1`; en SDXL combinar con resolución 832×1216 para retratos. La VRAM extra del IPAdapter en SDXL ronda los 600–800 MB. **Combinable con FaceDetailer al final** (la mejor combinación calidad/consistencia es: txt2img con IPAdapter FaceID Plus V2 → FaceDetailer con el mismo prompt).

**Importante (mayo 2026)**: el repo oficial de cubiq está en "maintenance only" desde 2025-04-14. Sigue funcional pero sin nuevas features.

### 3.2 InstantID

InstantID (Tencent) hace identity-preserving generation con **un único reference image**, combinando un IdentityEncoder (proyección del embedding ArcFace de antelopev2) y un **ControlNet de keypoints faciales**. La clave: aplica ~25% por el adapter y ~75% por el ControlNet, así que la pose del sujeto sigue al keypoint map de la referencia.

**Modelos** (todos en HuggingFace `InstantX/InstantID`):

- `ip-adapter.bin` (770 MB) → `ComfyUI/models/instantid/`
- `ControlNetModel/diffusion_pytorch_model.safetensors` (2.5 GB) → `ComfyUI/models/controlnet/` (renombrar a `instantid_control.safetensors`)
- InsightFace antelopev2 → `ComfyUI/models/insightface/models/antelopev2/`

Solo SDXL. Workflow: `Apply InstantID` necesita MODEL, conditioning, image (referencia), image_kps (opcional, para forzar otra pose), instantid (loader) y controlnet (loader).

**VRAM**: ~10–11 GB en FP16. En 3060 Ti necesitarás `--medvram` o usar checkpoint FP16 con VAE FP16 fixed. Alternativamente usar `--lowvram`. La página del repo recomienda **bajar el CFG a 4–5** y resolución no exactamente 1024×1024 (mejor 1016×1016) para evitar marcas de agua del training set.

### 3.3 ReActor (face swap)

ReActor es un faceswap **post-generación** basado en el modelo Inswapper (insightface) o, desde la versión "ReActor Core" 2025, con un núcleo independiente que **ya no requiere insightface ni Visual Studio Build Tools**. Repo activo: <https://github.com/Gourieff/ComfyUI-ReActor> (el antiguo `comfyui-reactor-node` fue baneado por GitHub Staff).

**Modelos**:
- `inswapper_128.onnx` (~530 MB) → `models/insightface/` (clásico)
- Alternativa SFW del autor: HyperSwap (`hyperswap_1a/1b/1c_256.onnx`) → `models/hyperswap/`
- ReSwapper (`reswapper_*.onnx`) → `models/reswapper/`
- Restoration: `GFPGANv1.4.pth`, `codeformer.pth`, `GPEN-BFR-512.onnx`, `RestoreFormer_Plus_Plus.onnx` → `models/facerestore_models/`
- Detection: `face_yolov8m.pt` → `models/ultralytics/bbox/`; SAM `sam_vit_b_01ec64.pth` → `models/sams/`

**Uso típico**:
```
KSampler → VAE Decode → ReActorFaceSwap(input_image, source_image, face_restore_model, face_restore_visibility, codeformer_weight, ...) → Save
```

**Limitaciones**: Inswapper-128 trabaja en 128×128 internamente, así que aunque restauras, el detalle máximo está limitado. Para retratos 4K es mejor: ReActor → FaceDetailer → Ultimate SD Upscale. Otra limitación importante: el Inswapper original **no es comercial** sin licencia. Por eso PuLID y FaceID son alternativas más limpias para uso editorial.

### 3.4 FaceDetailer (Impact Pack)

FaceDetailer es la combinación de un **detector** (BBOX `face_yolov8m.pt` o segmentation `face_yolov8s-seg.pt`) + **SAM segmenter** (`sam_vit_b_01ec64.pth` o `sam_vit_l`) + **inpainting** automático con un sampler. Detecta la cara, recorta, hace upscale del crop a una resolución que el modelo "entiende bien" (por defecto 768 o 1024), genera con denoise 0.4–0.5 reutilizando el mismo prompt/CLIP/MODEL, y vuelve a pegar con feathering.

Workflow mínimo (Impact Pack):

```
Generated Image → FaceDetailer(image, model, clip, vae, positive, negative,
                               bbox_detector, sam_model_opt,
                               guide_size=512, guide_size_for=true,
                               max_size=1024, seed, steps=20, cfg=7, sampler, scheduler,
                               denoise=0.5, feather=5, noise_mask=true,
                               force_inpaint=false, bbox_threshold=0.5, bbox_dilation=10,
                               bbox_crop_factor=3.0,
                               sam_detection_hint, sam_dilation, sam_threshold)
```

Conecta **BBOX_DETECTOR de UltralyticsDetectorProvider** (no SEGM_DETECTOR; eso da el error `'NO_SEGM_DETECTOR' object has no attribute 'detect'`).

Para múltiples caras: `SimpleDetector(SEGS) → SEGSOrderedFilter → DetailerForEachPipe`. Para escenas con multitud `bbox_dilation` ~12 y `crop_factor` ~3.

### 3.5 Comparativa Reactor vs IPAdapter FaceID vs InstantID vs PuLID

| Criterio | ReActor | IPAdapter FaceID Plus V2 | InstantID | PuLID (SDXL/Flux) |
|---|---|---|---|---|
| Mecanismo | Face-swap post-gen (ONNX) | Embedding inyectado en cross-attn + LoRA | ID encoder + ControlNet keypoints | Encoder híbrido (ArcFace+EVA-CLIP) |
| Control sobre pose final | Ninguno (sigue el txt2img) | Total (prompt manda) | Limitado: la pose del kps domina | Alto |
| Likeness | 8/10 (limitado por 128 px) | 7/10 | 9/10 (más pesado) | 8.5/10 |
| Coherencia de iluminación/skin | Media (post-pegado) | Alta | Alta | Muy alta (preserva estilo) |
| Modelos compatibles | Cualquier SD/SDXL/Flux (post) | SDXL, SD1.5 | **Solo SDXL** | SDXL, Flux dev/schnell, Flux 2 |
| VRAM extra | +1 GB | +700 MB | +2 GB | +1.5 GB (SDXL) / +2.5 GB (Flux) |
| Encaje en 8 GB VRAM | Excelente | Excelente | Justo | Bueno con GGUF Flux |
| Comercialmente limpio | **No** (Inswapper) | Depende (InsightFace no comercial) | InsightFace no comercial | Variantes con FaceNet (lldacing) sí |
| Mejor caso de uso | Reemplazo cara real → output | Mantener identidad estilizada coherente con prompt | Foto editorial fotográfica | Consistencia de personaje en serie |

**Cuándo usar cada uno**:
- Quieres **un personaje recurrente** en muchas escenas con prompts variados → IPAdapter FaceID Plus V2 (SDXL) o PuLID-Flux.
- Quieres **mismo rostro con misma pose** clonado de una foto → InstantID.
- Quieres tomar un render existente y poner la cara de alguien encima, sin reentrenar ni regenerar → ReActor.
- Pipeline editorial pro: combinación InstantID o IPAdapter al inicio + FaceDetailer al final + Ultimate SD Upscale.

### 3.6 Restauradores faciales

| Modelo | Fuerte en | Repositorio / archivo |
|---|---|---|
| **GFPGAN v1.4** | Restauración general suave, preserva expresión | `GFPGANv1.4.pth` (TencentARC) |
| **CodeFormer** | Restauración agresiva, configurable con `fidelity` (0–1) | `codeformer.pth` |
| **RestoreFormer++** | Detalles de piel, ojos | `RestoreFormer_Plus_Plus.onnx` |
| **GPEN-BFR-512 / 1024 / 2048** | Resolución alta, naturalidad | `GPEN-BFR-*.onnx` |

Todos van en `ComfyUI/models/facerestore_models/`. En ComfyUI los expone el nodo `FaceRestoreCFWithModel` del repo `mav-rik/facerestore_cf` y también ReActor internamente.

Reglas prácticas: GFPGAN para retoque ligero, **CodeFormer fidelity 0.5–0.7** para balance ID vs detalle, **GPEN-BFR-1024** para outputs 1024+. Si CodeFormer "endurece" demasiado los rasgos, baja fidelity.

---

## BLOQUE 4 — ControlNet y control de composición

### 4.1 Modelos ControlNet para SDXL (los que merecen estar en `models/controlnet/`)

Los **xinsir** ControlNets (Twitter @xinsir9, HuggingFace `xinsir/...`) son el estado del arte de junio 2024 y siguen siendo los más recomendados:

- **`xinsir/controlnet-union-sdxl-1.0` y `xinsir/controlnet-union-sdxl-promax`** — un solo modelo (~2.5 GB) que cubre Canny, OpenPose, Depth, Lineart, AnimeLineart, Seg, MLSD, Tile, Inpaint, mediante el nodo `SetUnionControlNetType`. Es lo más eficiente para 8 GB.
- `xinsir/controlnet-canny-sdxl-1.0`
- `xinsir/controlnet-openpose-sdxl-1.0`
- `xinsir/controlnet-depth-sdxl-1.0`
- `xinsir/controlnet-scribble-sdxl-1.0` y `controlnet-scribble-anime-sdxl-1.0`
- `xinsir/controlnet-tile-sdxl-1.0` (clave para upscaling por tiles)

Otros relevantes:
- **TTPLanet Tile Realistic** (`TTPLANET_Controlnet_Tile_realistic`) — la mejor opción de tile para fotos.
- **mistoLine** (`TheMistoAI/MistoLine`) — softedge SDXL, excelente para line-art-to-photo.
- **Stability AI Control-LoRAs** (`stabilityai/control-lora`) — versiones LoRA de canny/depth/recolor/sketch (300–700 MB cada una, ahorra VRAM).
- **Kohya-ss controlnet-lllite** — versiones ligeras (~46 MB) para SDXL pero con calidad menor.
- **BRIA AI** — canny, depth, openpose, recolor, fill (calidad alta, licencia distinta).

Cubierta de tareas: Canny (bordes), Lineart (dibujos), Depth (mapa de profundidad MiDaS/Zoe), OpenPose (DW-Pose moderno mejor que el clásico), MLSD (líneas rectas, arquitectura), Normal/NormalBae, Segment (SAM), Tile (preserva color, regenera detalle), Inpaint, Recolor (colorizar B/N), IP2P (instructpix2pix-style), Scribble (boceto a mano).

Listas vivas:
- <https://github.com/Mikubill/sd-webui-controlnet/wiki/Model-download>
- <https://education.civitai.com/civitai-guide-to-controlnet/>
- <https://stable-diffusion-art.com/controlnet-sdxl/>

### 4.2 ControlNet para Flux

Flux usa adaptadores específicos (no compatibles con los SDXL):
- **InstantX/FLUX.1-dev-Controlnet-Union** y **FLUX.1-dev-Controlnet-Union-Pro 2.0** — multi-tipo.
- **InstantX/FLUX.1-dev-Controlnet-Canny** y **Depth**.
- **XLabs-AI** colección: canny, depth, hed.
- **alimama-creative/FLUX.1-dev-Controlnet-Inpainting-Beta**.
- **Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro**.

Para 8 GB son aún más exigentes que SDXL+ControlNet; combinarlos con Flux GGUF Q4 deja poco margen.

### 4.3 Cómo usar ControlNet en ComfyUI

Workflow de Canny SDXL:

```
LoadImage(reference) → CannyEdgePreprocessor (de comfyui_controlnet_aux)
       ↓
ControlNetLoader("xinsir_canny_sdxl.safetensors")
       ↓ (control_net) ⎫
       (image)         ⎬→ ControlNetApplyAdvanced(positive, negative, strength=0.7,
                       ⎭   start_percent=0, end_percent=0.8)
                        → KSampler...
```

Para **xinsir Union**:
```
ControlNetLoader → SetUnionControlNetType(type="canny") → ControlNetApplyAdvanced
```

Buenas prácticas: `strength 0.5–0.85`; `start_percent 0` y `end_percent 0.8` para que los últimos pasos refinen detalle sin bloqueo del control; combinar 2 CNs con strengths bajas (0.4 + 0.4) suele ser mejor que uno fuerte.

### 4.4 IP-Adapter vs ControlNet

- **ControlNet** condiciona en **estructura espacial** (geometría, contornos, profundidad, pose).
- **IP-Adapter** condiciona en **estilo y semántica** del referente (qué hay en la imagen, qué paleta y atmósfera tiene). Es como añadir un prompt visual.
- Se combinan: ControlNet OpenPose para mantener pose + IPAdapter para mantener estilo + IPAdapter FaceID para mantener identidad. Es el típico stack triple.

### 4.5 T2I-Adapter (alternativa ligera)

T2I-Adapters (TencentARC) son adaptadores ~80 MB (vs los 1.5–2.5 GB de ControlNets). Calidad inferior pero útil cuando la VRAM es muy ajustada. SDXL: `TencentARC/t2i-adapter-canny-sdxl-1.0`, `t2i-adapter-depth-midas-sdxl-1.0`, `t2i-adapter-openpose-sdxl-1.0`, `t2i-adapter-lineart-sdxl-1.0`, `t2i-adapter-sketch-sdxl-1.0`. En ComfyUI se cargan con `ControlNetLoader` y se aplican con `T2IAdapterApply` o el mismo ControlNetApply.

---

## BLOQUE 5 — Upscaling y post-procesado

### 5.1 Ultimate SD Upscale

`ComfyUI_UltimateSDUpscale` (ssitu) replica el script Ultimate Upscale de A1111: **divide la imagen en tiles solapados, hace img2img sobre cada tile con denoise bajo (0.2–0.4) y los reensambla** con feathering. Permite escalar 2× a 4× sin OOM en 8 GB.

Repositorio: <https://github.com/ssitu/ComfyUI_UltimateSDUpscale>. Workflows ejemplo en `example_workflows/`.

Parámetros típicos: `upscale_by=2.0`, `tile_width=1024`, `tile_height=1024`, `mask_blur=8`, `tile_padding=32`, `seam_fix_mode="Half Tile"`, `denoise=0.25`. Combinarlo con un upscaler pixel-space y, opcionalmente, un Tile ControlNet de xinsir o TTPLanet para coherencia.

Workflow canónico:

```
KSampler → VAE Decode (imagen base 1024) →
   UltimateSDUpscale(upscale_model=4x-UltraSharp, model, positive, negative, vae,
                     upscale_by=2.0, denoise=0.25, ...) → Save Image
```

### 5.2 Modelos de upscale pixel-space

Todos van en `ComfyUI/models/upscale_models/` y se cargan con `UpscaleModelLoader`:

- **4x-UltraSharp** (lokCX) — el favorito para fotos generales. <https://huggingface.co/lokCX/4x-Ultrasharp/blob/main/4x-UltraSharp.pth>
- **4x_NMKD-Siax_200k** — texturas de piel, retratos.
- **4x_foolhardy_Remacri** — generalista, más limpio que UltraSharp.
- **4x-RealESRGAN-x4plus** y **4x-RealESRGAN-x4plus-anime-6B** — clásicos.
- **4x_NMKD-Superscale-SP_178000_G** — uso general.
- **8x_NMKD-Superscale_150000_G** — para 8× en un paso.
- **1x_DeJPG_OmniSR** — denoise/dejpg sin escalar.
- **4xLSDIRplusN_GAN** — fotos modernas, alta nitidez.

Catálogo curado: <https://openmodeldb.info>.

### 5.3 Tile ControlNet para upscaling coherente

Cuando se hace SD upscale con denoise alto, los tiles divergen y aparecen "alucinaciones" (caras donde había paredes). El **Tile ControlNet** ata cada tile a su contenido original, permitiendo `denoise 0.5–0.65` con coherencia.

Para SDXL: `xinsir/controlnet-tile-sdxl-1.0` o `TTPLANET_Controlnet_Tile_realistic`.
Para SD 1.5: `control_v11f1e_sd15_tile.pth` (ControlNet 1.1 oficial).
Para Flux: `Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro` (modo tile).

Workflow: en lugar de `UltimateSDUpscale` simple, se usa `Ultimate SD Upscale (no upscale)` o el mismo nodo con un ControlNetApply en el sampler interno (hay variantes). El workflow `cubiq/ComfyUI_Workflows/upscale/` muestra el método sin Ultimate, usando Tile CN + 2× nearest-exact + segundo KSampler con denoise 0.75.

### 5.4 Hires Fix vs Upscale externo

- **Hires Fix** (en SD WebUI) o el patrón "two-pass KSampler" en ComfyUI: el primer sampler genera a baja resolución, se hace `LatentUpscale` o `LatentUpscaleBy`, y un segundo `KSamplerAdvanced` con denoise 0.4–0.6 refina a alta resolución. Ventaja: una sola pasada, coherencia total. Desventaja: limitado a 1.5–2× antes de OOM en 8 GB.
- **Pixel-space upscale** (4x-UltraSharp) → muy rápido pero solo aumenta píxeles, no detalle generativo.
- **Ultimate SD Upscale + Tile CN**: la ruta para 4×–8× con detalle real. Lento pero la única que "añade" información plausible.

Regla práctica para 8 GB: hi-res fix latente para llegar a 1536–1920 px, después Ultimate SD Upscale 2× con Tile CN para 4K.

---

## BLOQUE 6 — Filtros de seguridad y control editorial

ComfyUI **no incluye un safety checker por defecto**: el comportamiento depende del checkpoint y los nodos del workflow. Esta es la diferencia más relevante con A1111/Forge, donde sí existe el flag `--disable-safe-unpickle` y un toggle en Settings → Stable Diffusion → "Disable NSFW filter".

Para entornos profesionales que **sí necesitan filtrado** (clientes, plataformas, revisión editorial), las opciones son:

1. **`ComfyUI-safety-checker` (42lux)** — <https://github.com/42lux/ComfyUI-safety-checker>. Nodo `Safety Checker` que usa el modelo CLIP de CompVis (`stable-diffusion-safety-checker`). Reemplaza la imagen detectada por un placeholder negro. Sensitivity:
   - `0.0` → desactivado
   - `0.5` → estándar (desnudez explícita)
   - `1.0` → estricto (bloquea hasta lencería)
   Salidas: image (negra si NSFW) y boolean `nsfw` que puedes encadenar a un Save Image alternativo, log, webhook o paso de revisión humana.
2. **`ComfyUI-YetAnotherSafetyChecker` (BetaDoggo)** — <https://github.com/BetaDoggo/ComfyUI-YetAnotherSafetyChecker>. Usa `AdamCodd/vit-base-nsfw-detector`, más rápido y con score continuo (típicamente >0.95 para nudity). Ofrece slider `threshold` (default 0.8) y toggle CUDA.
3. **`stable-diffusion-safety-checker` (CompVis original)** — modelo en HuggingFace, usado por defecto en pipelines `diffusers`.
4. **NudeNet ONNX** — clasificador por categorías (Female_Genitalia_Exposed, Buttocks_Exposed, etc.). Útil cuando necesitas reglas finas (p.ej. permitir lencería pero no desnudo). Hay nodos comunitarios envoltorios en ComfyUI Registry.

Para uso editorial profesional la arquitectura recomendada es: **encadenar el safety checker tras VAE Decode y, si retorna positivo, redirigir a un canal de revisión** en lugar de descartar (boolean output → Switch → "rejected" folder).

Notas sobre control:
- Algunos checkpoints distribuidos por Stability AI para SD 1.4/1.5 originales traían el safety checker incrustado (`safety_checker.py` en el pipeline diffusers). Eso **no aplica a los `.safetensors` que descargas de CivitAI**, que son solo pesos UNet/VAE.
- En Forge: Settings → Stable Diffusion → desmarcar "Enable Safety Check". En A1111: igual.
- La licencia CreativeML Open RAIL-M (SD 1.x/2.x) y la Stability AI Community License (SDXL) permiten uso comercial pero prohíben generación de CSAM, deepfakes no consentidos, y uso para dañar a terceros. Esto es independiente de si activas o no el filtro.

---

## BLOQUE 7 — Otros sistemas y alternativas

### 7.1 Comparativa real en RTX 3060 Ti 8 GB

| GUI | Velocidad SDXL (3060 Ti) | Soporte Flux | VRAM mgmt 8 GB | Curva aprendizaje | Mejor uso |
|---|---|---|---|---|---|
| **ComfyUI** | ~1.6 it/s; el más rápido en pipelines complejos | Excelente (FP8, GGUF, NF4) | Muy bueno con `--lowvram`/`--medvram` | Empinada (grafos) | Producción avanzada, automatización |
| **Forge (lllyasviel)** | ~1.7 it/s; ~30–75% más rápido que A1111; **el mejor para Flux NF4 en 8 GB** | Excelente nativo (NF4 v2 oficial) | El mejor: corre SDXL en 4 GB y SD 1.5 en 2 GB sin flags | Fácil (UI A1111) | Workflow rápido + Flux en VRAM baja |
| **Automatic1111 (A1111)** | ~0.7–1.0 it/s; lento | Limitado/extension | Necesita `--medvram-sdxl --xformers --no-half-vae`; OOM frecuente con XL+CN | Fácil | Extensiones legacy, ecosistema antiguo |
| **InvokeAI** | ~1.3 it/s | Sí | Bueno | Media | Canvas unificado, retoque tipo Photoshop, equipos creativos |
| **SwarmUI (mcmonkey)** | ~1.6 it/s (usa ComfyUI como backend) | Sí | Bueno | Fácil-Media | Frontend bonito sobre Comfy con multi-GPU futuro |
| **Fooocus / RuinedFooocus** | ~1.4 it/s | RuinedFooocus sí | Excelente | Trivial | Flujo "Midjourney-like", no editorial pro |
| **StabilityMatrix** | (es un launcher) | Sí | — | Trivial | Gestionar varios UIs y compartir modelos |

### 7.2 Forge para 8 GB

Forge es un fork de A1111 cuya principal contribución técnica es **reescribir la gestión de memoria** ("backend remove all WebUI's codes related to resource management and reworked everything"). Datos clave del propio README:

- Sin flags: SDXL corre en **4 GB** y SD 1.5 en **2 GB**.
- Soporte oficial **Flux.1 dev NF4 v2** (`flux1-dev-bnb-nf4-v2.safetensors`) y **Flux FP8** con un toggle "GPU Weights" que decide cuánto del modelo cargar en VRAM y cuánto offloadear (la opción "Shared" usa shared GPU memory de Windows; la opción "CPU" usa RAM del sistema). En 8 GB con 16 GB RAM, NF4 + GPU Weights ~6500 MB es la receta oficial.
- Flags útiles: `--cuda-stream` (15–25% speedup en 30XX/40XX con poca VRAM), `--pin-shared-memory` (con cuidado, puede crashear), `--cuda-malloc`, `--always-offload-from-vram`.
- Nodos Flux ya integrados; LoRAs Flux se cargan igual que SDXL.

**Cuándo elegir Forge sobre ComfyUI** en tu hardware: cuando quieres iterar rápido en Flux NF4 sin construir grafos, cuando necesitas extensiones de A1111 (DynamicPrompts, ADetailer, regional prompter, etc.), o cuando hay clientes no técnicos.

**Cuándo seguir en ComfyUI**: Flux GGUF (mejor calidad en 8 GB que NF4), pipelines con InstantID + IPAdapter + FaceDetailer + Ultimate SD Upscale en serie, automatización vía API.

### 7.3 Pinokio

Pinokio (<https://pinokio.co>) es un launcher one-click multiplataforma. Tiene un **drive compartido** en `pinokio/drive/drives/peers/d1704581225212/checkpoints/` que es accesible desde A1111, Fooocus y ComfyUI sin duplicar modelos. Apps relevantes para tu caso, instalables directamente desde la pestaña "Discover":

- **ComfyUI** (oficial, ya lo tienes)
- **Forge** / Stable Diffusion WebUI Forge
- **Automatic1111**
- **Fooocus** y **RuinedFooocus** (ofrece soporte Flux)
- **Fooocus-API** (REST endpoint, puerto 8888)
- **InvokeAI**
- **SwarmUI**
- **FluxGym** (UI sencilla para entrenar LoRAs Flux con bajo VRAM)
- **Kohya_ss / OneTrainer** para entrenar LoRA SDXL/SD1.5
- **LivePortrait** (animación facial desde imagen+driving)
- **AnimateDiff-Lightning**, **CogVideoX**, **Hunyuan Video** (video, requieren más VRAM)
- **Stable Video Diffusion**
- **Real-ESRGAN-NCNN** y **GFPGAN** standalone
- **ComfyUI Stack with Pinokio Manager**: hay variantes del comunidad que vienen con nodos preinstalados.

Para descubrir más: <https://pinokio.co/app> (sección "verified" + "community"). La wiki técnica es <https://github.com/6Morpheus6/pinokio-wiki>.

Recomendación práctica: en tu sistema con Pinokio + ComfyUI + (instalar) Forge tienes el set completo: ComfyUI para SDXL fine-tunes y Flux GGUF + pipelines complejos; Forge para Flux NF4 rápido y compatibilidad A1111.

---

## BLOQUE 8 — Recursos y documentación

### 8.1 Documentación oficial ComfyUI

- Repo principal: <https://github.com/comfyanonymous/ComfyUI> (ahora redirige a <https://github.com/Comfy-Org/ComfyUI>)
- Web oficial: <https://www.comfy.org>
- Docs oficiales: <https://docs.comfy.org>
- Docs de desarrollo (cómo escribir nodos): <https://docs.comfy.org/development/core-concepts/nodes>
- Ejemplos canónicos: <https://comfyanonymous.github.io/ComfyUI_examples/>
- ComfyUI-Manager: <https://github.com/Comfy-Org/ComfyUI-Manager>
- Comfy Registry (catálogo de custom nodes): <https://registry.comfy.org>
- DeepWiki técnica del repo: <https://deepwiki.com/Comfy-Org/ComfyUI>

### 8.2 Wikis y referencias técnicas

- **ComfyUI Wiki** (no oficial pero excelente): <https://comfyui-wiki.com>
- **RunComfy node docs**: <https://www.runcomfy.com/comfyui-nodes>
- **ltdrdata Nodes Info**: <https://ltdrdata.github.io>
- **Stable Diffusion Art** (tutoriales A1111/ComfyUI/Forge): <https://stable-diffusion-art.com>
- **CivitAI Education**: <https://education.civitai.com>
- **OpenModelDB** (upscalers): <https://openmodeldb.info>

### 8.3 Workflows fotorrealistas

- **OpenArt workflows** (cierra 18 ene 2026): <https://openart.ai/workflows/home>
- **CivitAI workflows**: <https://civitai.com/articles>
- **RunComfy workflow library**: <https://www.runcomfy.com/comfyui-workflows>
- **cubiq/ComfyUI_Workflows** (didácticos del autor IPAdapter): <https://github.com/cubiq/ComfyUI_Workflows>
- **MyAIForce** (tutoriales detallados): <https://myaiforce.com>
- **NextDiffusion** (guías Flux GGUF): <https://www.nextdiffusion.ai>

### 8.4 Canales/recursos técnicos en YouTube

- **Latent Vision** (cubiq, autor de IPAdapter/InstantID/PuLID nodes): <https://www.youtube.com/@latentvision> — tutoriales de referencia.
- **Dr.Lt.Data's ComfyUI Extension** (autor del Impact Pack): tutoriales sin narración con captions.
- **Sebastian Kamph**, **Olivio Sarikas**, **Scott Detweiler** (oficial ComfyUI), **CgTopTips**, **Pixaroma**.
- **MachineDeluxe** — Flux y workflows avanzados.

### 8.5 Repositorios GitHub clave (resumen)

- comfyanonymous/ComfyUI — base
- Comfy-Org/ComfyUI-Manager — gestor
- ltdrdata/ComfyUI-Impact-Pack y ComfyUI-Impact-Subpack — FaceDetailer
- cubiq/ComfyUI_IPAdapter_plus — IPAdapter/FaceID
- cubiq/ComfyUI_InstantID — InstantID
- balazik/ComfyUI-PuLID-Flux y lldacing/ComfyUI_PuLID_Flux_ll — PuLID Flux
- iFayens/ComfyUI-PuLID-Flux2 — PuLID Flux 2
- Gourieff/ComfyUI-ReActor — face swap
- Fannovel16/comfyui_controlnet_aux — preprocesadores
- Kosinkadink/ComfyUI-Advanced-ControlNet
- Kosinkadink/ComfyUI-VideoHelperSuite
- ssitu/ComfyUI_UltimateSDUpscale
- WASasquatch/was-node-suite-comfyui
- rgthree/rgthree-comfy
- pythongosssss/ComfyUI-Custom-Scripts
- city96/ComfyUI-GGUF — GGUF support
- yolain/ComfyUI-Easy-Use
- florestefano1975/comfyui-portrait-master
- mav-rik/facerestore_cf — GFPGAN/CodeFormer
- 6Morpheus6/pinokio-wiki — referencia Pinokio
- lllyasviel/stable-diffusion-webui-forge — Forge
- mcmonkeyprojects/SwarmUI — SwarmUI
- LykosAI/StabilityMatrix — gestor multi-UI

---

## Recomendación final concreta para tu setup

Para una RTX 3060 Ti 8 GB + i7-12700F + 16 GB RAM en mayo 2026, el stack óptimo es:

1. **Pinokio** ya lo tienes — instala adicionalmente **Forge** desde Pinokio para Flux NF4 rápido.
2. **ComfyUI + ComfyUI-Manager + ComfyUI-GGUF + Impact Pack + IPAdapter Plus + InstantID + comfyui_controlnet_aux + UltimateSDUpscale + ReActor + rgthree + WAS + Custom-Scripts**.
3. **Checkpoints SDXL (instalar 2–3, no más)**: Juggernaut XL v9 (genérico), RealVisXL V5.0 (retrato), epiCRealism XL Crystal Clear (editorial).
4. **Flux**: Flux.1 dev GGUF Q4_0 o Q5_0 (city96) + `t5-v1_1-xxl-encoder-Q4_K_M.gguf` para CLIP/T5 ofloadeado, **o** Flux.1 dev NF4 v2 dentro de Forge si prefieres velocidad.
5. **ControlNets**: el Union ProMax de xinsir cubre 95% de necesidades en un solo archivo (~2.5 GB).
6. **Upscalers**: 4x-UltraSharp + 4x_NMKD-Siax_200k.
7. **Cara/identidad**: IPAdapter FaceID Plus V2 SDXL + FaceDetailer (face_yolov8m + sam_vit_b) como pipeline diario; PuLID-Flux cuando trabajes con Flux.
8. **VAE**: `sdxl_vae_fp16_fix` para SDXL; `ae.safetensors` para Flux.
9. **Workflow base recomendado**: txt2img SDXL → IPAdapter (si hay personaje recurrente) → KSampler (28 pasos, dpmpp_2m karras, CFG 5–7) → VAE Decode → FaceDetailer → UltimateSDUpscale 2× con 4x-UltraSharp + denoise 0.25.
10. Lanzar ComfyUI con `--lowvram` solo si haces Flux GGUF Q5/Q6; con SDXL no necesitas flags. En Pinokio el script ya gestiona el venv: edita el archivo `start.json` de la app si quieres añadir flags persistentes.

Velocidades realistas que vas a observar: SDXL 1024² a 28 pasos ≈ 17–20 s; SDXL + ControlNet ≈ 25–30 s; Flux NF4 dev 1024² a 20 pasos ≈ 60–90 s; Flux schnell GGUF Q4 1024² a 4 pasos ≈ 18–25 s; Ultimate SD Upscale 2× ≈ 40–60 s adicionales. La 3060 Ti es suficientemente competente para producción editorial fluida en SDXL y para Flux a ritmo de "un par de imágenes buenas por minuto".