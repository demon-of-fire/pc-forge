# What Does a GPU Actually Do?

A GPU (Graphics Processing Unit) is a specialized processor designed to handle massive parallel computation. Originally built to render 3D graphics, GPUs have evolved into one of the most important components for gaming, content creation, AI, and scientific computing.

## GPU Architecture: Parallel by Design

The fundamental difference between a CPU and a GPU is how they approach problems. A CPU is a generalist — a few extremely powerful cores that excel at complex, sequential tasks. A GPU is a specialist — thousands of smaller cores that excel at performing the same simple operation across massive datasets simultaneously.

Think of it this way: a CPU is like a team of 16 world-class chefs who can handle complex, custom orders. A GPU is like a team of 10,000 line cooks who can each do one simple task very quickly. For rendering millions of pixels on a screen, the GPU's approach wins by an enormous margin.

| Characteristic | CPU | GPU |
|---|---|---|
| Core count | 6-24 | 1,000-18,000+ |
| Clock speed | 4-6 GHz | 1.5-3 GHz |
| Core complexity | Very high | Relatively simple |
| Best at | Sequential logic, branch prediction | Parallel computation, math-heavy workloads |
| Memory | System RAM (DDR5) | Dedicated VRAM (GDDR6/6X or HBM) |

## CUDA Cores and Stream Processors

The "cores" inside a GPU are called different names depending on the manufacturer:

- **NVIDIA**: CUDA Cores (Compute Unified Device Architecture)
- **AMD**: Stream Processors (SPs)
- **Intel**: Xe Cores (within Arc GPUs)

These are not comparable across brands. NVIDIA's CUDA cores and AMD's stream processors have different architectures, so you cannot directly compare a 10,000-core NVIDIA GPU to a 6,000-core AMD GPU and assume the NVIDIA card is faster. The architecture, clock speed, and overall design determine real-world performance.

What you can compare across brands is:
- **Rasterization performance**: Traditional 3D rendering speed, measured in FPS
- **Ray tracing performance**: Hardware-accelerated light simulation
- **FP16/FP32/FP64 throughput**: Relevant for AI and compute workloads
- **Memory bandwidth**: How fast data moves between the GPU chip and VRAM

## VRAM: The GPU's Dedicated Memory

VRAM (Video RAM) is high-speed memory attached directly to the GPU. It stores textures, frame buffers, geometry data, and other assets the GPU needs instant access to.

### How Much VRAM Do You Need?

| VRAM | Suitable For |
|---|---|
| 8 GB | 1080p gaming with moderate texture settings |
| 12 GB | 1440p gaming, light content creation |
| 16 GB | 4K gaming, moderate video editing, entry AI work |
| 24 GB | 4K max settings, professional video editing, local AI models |
| 48 GB+ | Professional workstations, large AI model training |

VRAM requirements are increasing as games ship with higher-resolution textures. A game at 4K with ultra textures can easily consume 12-16 GB of VRAM. Running out of VRAM causes stuttering and texture pop-in as the GPU swaps data to and from system RAM through PCIe.

### VRAM Types

- **GDDR6**: Standard VRAM for most modern GPUs. Good bandwidth per dollar.
- **GDDR6X**: Higher-bandwidth variant used in NVIDIA's RTX 30/40 series. Runs hotter.
- **GDDR7**: Next-generation VRAM appearing in RTX 50-series cards. Improved bandwidth and efficiency.
- **HBM (High Bandwidth Memory)**: Stacked memory used in professional and data center GPUs. Extremely high bandwidth but very expensive.

## GPU's Role in Gaming

The GPU is the single most important component for gaming performance. It handles:

### Rasterization

Traditional rendering where the GPU converts 3D geometry into 2D pixels on your screen. This is still the primary rendering method for most games. GPU marketing and benchmarks largely focus on rasterization performance because it determines frame rates in the majority of titles.

### Ray Tracing

Hardware-accelerated simulation of how light behaves in the real world. Ray tracing produces more realistic reflections, shadows, ambient occlusion, and global illumination. It's computationally expensive — a GPU with strong ray tracing hardware can maintain playable frame rates with ray tracing enabled where weaker GPUs cannot.

### Shader Processing

Shader programs run on the GPU to determine the final color of each pixel. Modern games use complex pixel shaders for effects like:
- Material properties (roughness, metallic, subsurface scattering)
- Post-processing (motion blur, depth of field, bloom)
- volumetric effects (fog, clouds, god rays)

### Upscaling Technologies

NVIDIA DLSS, AMD FSR, and Intel XeSS use AI or algorithmic approaches to render the game at a lower resolution and then intelligently upscale to the target resolution. This dramatically improves performance with minimal visual quality loss. These technologies are GPU-specific — DLSS requires NVIDIA RTX hardware, for example.

## GPU's Role in AI and Machine Learning

GPUs have become the backbone of modern AI. The same parallel architecture that makes GPUs great at rendering millions of pixels makes them exceptional at the matrix multiplication operations that underpin neural networks.

### Why GPUs Dominate AI

Training a large language model involves performing trillions of floating-point operations across massive matrices. A GPU with thousands of cores can perform these operations in parallel, completing in hours what would take a CPU years.

Key GPU characteristics for AI:
- **Tensor Cores (NVIDIA)**: Dedicated hardware for matrix multiplication that accelerates AI training and inference
- **FP16/BF16 performance**: Reduced precision arithmetic is sufficient for many AI operations and runs much faster than FP32
- **VRAM capacity**: Larger models require more VRAM. A 70B parameter model needs at least 40 GB of VRAM to run at all, and 80+ GB for practical use
- **Memory bandwidth**: Loading model weights from VRAM is often the bottleneck in local inference

### Local AI on Consumer GPUs

You can run quantized AI models locally on consumer GPUs:
- **8 GB VRAM**: Small models (7B parameters at Q4 quantization)
- **12-16 GB VRAM**: Medium models (13B-30B parameters at Q4)
- **24 GB VRAM**: Large models (up to 70B at Q4 quantization)
- **48+ GB VRAM**: Very large models with minimal quantization

Tools like Ollama, LM Studio, and llama.cpp make it straightforward to run local LLMs on NVIDIA and AMD consumer GPUs.

## GPU Selection: What Actually Matters

### For Gaming

1. **Target resolution and frame rate**: 1080p 60fps needs a mid-range GPU. 4K 144fps needs the best available.
2. **Ray tracing**: If you want ray tracing, NVIDIA's RTX cards generally have stronger ray tracing hardware than AMD's equivalent rasterization tier.
3. **Upscaling**: DLSS is widely considered the best upscaling solution. FSR works on all GPUs but has slightly more visual artifacts.
4. **VRAM**: Ensure enough VRAM for your target resolution and texture settings.

### For AI/ML

1. **VRAM capacity**: The most important factor. More VRAM means larger models without quantization.
2. **Tensor core generation**: Newer generations are dramatically faster for AI workloads.
3. **Memory bandwidth**: Faster VRAM means faster model loading and inference.
4. **CUDA ecosystem**: NVIDIA's CUDA software ecosystem is far more mature than competitors'. Most AI tools assume NVIDIA GPUs.

### For Content Creation

1. **VRAM**: Video editing, especially with effects and multiple layers, benefits from more VRAM.
2. **CUDA/OpenCL acceleration**: Many creative apps (DaVinci Resolve, Blender, After Effects) use GPU acceleration for rendering and effects.
3. **Encoder quality**: NVIDIA's NVENC encoder produces excellent quality for streaming and video export.

## Integrated vs Discrete GPUs

Most Intel and AMD CPUs come with integrated graphics (iGPU). These share system RAM and have a fraction of the compute power of a discrete GPU.

| Type | Suitable For |
|---|---|
| Integrated graphics | Desktop tasks, video playback, very light gaming, troubleshooting |
| Entry discrete GPU (RTX 4060, RX 7600) | 1080p gaming, light content creation |
| Mid-range discrete GPU (RTX 4070, RX 7800 XT) | 1440p gaming, moderate content creation |
| High-end discrete GPU (RTX 4080/4090, RX 7900 XTX) | 4K gaming, heavy content creation, local AI |

## Summary

The GPU is the most important component for gaming performance and has become essential for AI workloads. CUDA cores and stream processors are not directly comparable across brands. VRAM capacity and bandwidth matter as much as raw GPU compute power. For gaming, match your GPU to your target resolution and frame rate. For AI, prioritize VRAM capacity and tensor core generation. For content creation, ensure your GPU has enough VRAM and is supported by your software's GPU acceleration framework.
