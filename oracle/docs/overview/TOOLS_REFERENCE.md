# AI Content Automation Tools Reference
**Last Updated: January 18, 2026 | v4.3**

Comprehensive pricing, quality, and capabilities guide for building automated video content pipelines including image animation workflows.

## ⚡ December 2025 Major Updates
| Model | Release Date | Key Change | Research Priority |
|-------|--------------|------------|-------------------|
| **Runway Gen-4.5** | Dec 1 | #1 Video Arena (Elo 1,247), native audio Dec 11 | ⭐⭐⭐⭐⭐ |
| **Kling 2.6** | Dec 3 | Native audio-visual (speech, singing, rap, SFX) | ⭐⭐⭐⭐⭐ |
| **Kling O1** | Dec 3 | Unified generation + editing + inpainting | ⭐⭐⭐⭐ |
| **HunyuanVideo 1.5** | Nov 20 | Open source, 8.3B params, runs on 14GB VRAM | ⭐⭐⭐⭐⭐ |
| **ByteDance Vidi2** | Dec 1 | Open source 12B, Spatio-Temporal Grounding | ⭐⭐⭐⭐ |
| **Adobe Firefly** | Dec 16 | Prompt-based video editing, FLUX.2 integration | ⭐⭐⭐ |
| **Runway GWM-1** | Dec 11 | First world model for physics simulation | ⭐⭐⭐ |

---

## Table of Contents
1. [Unified Platforms](#1-unified-platforms)
2. [Text-to-Speech (TTS) APIs](#2-text-to-speech-tts-apis)
3. [Speech-to-Text / Transcription](#3-speech-to-text--transcription)
4. [Image Generation APIs](#4-image-generation-apis)
5. [Video Generation & Image Animation](#5-video-generation--image-animation)
6. [Music Generation APIs](#6-music-generation-apis)
7. [Stock Footage APIs](#7-stock-footage-apis)
8. [Template-Based Video APIs](#8-template-based-video-apis)
9. [Video Editing / Composition](#9-video-editing--composition)
10. [Workflow Automation](#10-workflow-automation)
11. [MCP Servers (Model Context Protocol)](#11-mcp-servers-model-context-protocol)
12. [Recommendations](#12-recommendations)

---

## 1. Unified Platforms

### Google AI Studio
**The central hub for Google's generative AI models** - browser-based IDE for prototyping with Gemini, Veo, Imagen, and Lyria.

| Plan | Cost | Key Features |
|------|------|--------------|
| **Free Tier** | $0 | Gemini 2.5/3 access, generous daily quotas, API key generation |
| **Google AI Pro** | $19.99/mo | Higher limits, Nano Banana Pro, Veo 3.1 Fast (~90 videos/mo), Flow filmmaking |
| **Google AI Ultra** | $249.99/mo | Highest limits, Veo 3.1, Deep Think, 30TB storage, YouTube Premium |

**Free Tier Includes:**
- Gemini 2.5 Pro/Flash/Flash-Lite access
- ~10-50 RPM depending on region
- Limited Imagen 3 image generation
- API key generation (no billing required for testing)
- $300 Google Cloud credit for new accounts (extends testing)

**Models Available:**
- **Text:** Gemini 3 Pro, 2.5 Pro/Flash/Flash-Lite
- **Images:** Nano Banana Pro (Gemini 3 Pro Image), Imagen 4
- **Video:** Veo 2, Veo 3, Veo 3.1, Veo 3.1 Fast
- **Music:** Lyria 2, Lyria RealTime
- **Audio:** Live API for real-time audio

**API Pricing (Pay-as-you-go):**
| Model | Input | Output |
|-------|-------|--------|
| Gemini 3 Pro | $2.00/1M tokens | $12.00/1M tokens |
| Gemini 2.5 Flash | $0.075/1M tokens | $0.30/1M tokens |
| Nano Banana Pro (4K image) | N/A | $0.24/image |
| Nano Banana (2K image) | N/A | $0.134/image |
| Veo 3.1 Fast (no audio) | N/A | $0.10/second |
| Veo 3 (with audio) | N/A | $0.75/second |

---

### fal.ai
**Unified API marketplace** for 600+ image, video, and audio models with pay-per-use pricing.

| Plan | Cost | Features |
|------|------|----------|
| **Free Tier** | $0 | Free credits on signup, limited models |
| **Pay-as-you-go** | Per-model | Most cost-effective for volume |
| **Enterprise** | Custom | SOC 2, SLA, priority support |

**Popular Model Pricing (Dec 2025 Update):**
| Model | Type | Cost |
|-------|------|------|
| Flux Dev | Image | $0.025/image |
| **Kling 2.6** | Video w/Audio | $0.14/sec (~$0.70/5s) |
| **Kling 2.5 Turbo** | Text/Image-to-Video | $0.07/sec (~$0.35/5s) |
| Wan 2.1 I2V | Image-to-Video | $0.20 (480p), $0.40 (720p) |
| Hailuo 02 | Image-to-Video | $0.045/sec (768p), $0.017/sec (512p) |
| Seedance Pro | Image-to-Video | $0.62/5s video (1080p) |
| Veo 3.1 Fast | Text-to-Video | $0.10/second |
| **HunyuanVideo 1.5** | Text/Image-to-Video | Coming soon |

**Advantages:**
- Unified SDK (Python, JS, Swift)
- No infrastructure management
- Global CDN, 99.9% uptime SLA
- LoRA training support
- Model-agnostic (switch without code changes)
- Early access to new models (Kling 2.6, HunyuanVideo)

---

### Replicate
**Model marketplace** with pay-per-use access to open-source and proprietary models.

| Pricing Model | Cost | Best For |
|---------------|------|----------|
| **Pay-per-run** | Varies by model | Testing, low volume |
| **GPU time** | $0.000225/sec (CPU) to $0.001400/sec (A100) | Custom models |

**Popular Models:**
- Video: Kling 1.6/2.0, Wan 2.1, Veo 2
- Images: SDXL, Flux, Seedream 4
- Upscaling: Real-ESRGAN (~$0.01/image)
- Audio: Various TTS/music models

**Advantages:**
- Single API key for all models
- Good for experimentation and A/B testing
- Avoid vendor lock-in
- Custom model deployment

---

### PiAPI
**Third-party API access** to premium models without official APIs.

| Plan | Cost | Features |
|------|------|----------|
| **Free** | $0 | Limited credits, basic access |
| **Creator** | $8/mo | Priority generation, more features |
| **Pro** | $50/mo | Highest priority, all features, 20+ concurrent jobs |
| **Host-Your-Account** | $10/seat/mo | Use your own accounts via API |

**Supported Models (Dec 2025 Pricing):**
- **Kling 2.6 (with audio):** $0.55/5s, $1.10/10s (via Kie.ai)
- **Kling 2.6 (silent):** $0.28/5s, $0.55/10s
- **Kling 2.5 Turbo:** $0.21/5s, $0.42/10s
- **Kling 2.5 Pro:** $0.13-0.40/video
- **Luma Dream Machine:** $0.20/generation (60% cheaper than fal.ai)
- **Midjourney:** Full API access (no official API exists)
- **Flux:** LoRA support, concurrent jobs
- **Udio/Suno:** Music generation

**Kling 2.6 API Providers Comparison:**
| Provider | 5s Silent | 5s w/Audio | 10s Silent | 10s w/Audio |
|----------|-----------|------------|------------|-------------|
| **Kie.ai** | $0.28 | $0.55 | $0.55 | $1.10 |
| **fal.ai** | $0.35 | $0.70 | $0.70 | $1.40 |
| **WaveSpeed** | $0.35 | $0.70 | $0.70 | $1.40 |
| Per-second | $0.07/s | $0.14/s | $0.07/s | $0.14/s |

**Advantages:**
- Access to models without official APIs (Kling 2.6, Midjourney, Luma)
- Often 40-60% cheaper than official pricing
- 20+ concurrent jobs (vs official's 5 max)
- Watermark removal options
- Unified API for multiple services

---

## 2. Text-to-Speech (TTS) APIs

### Quality Rankings (Dec 2025)
Based on MOS (Mean Opinion Score) benchmarks and user surveys:

| Rank | Tool | MOS Score | Strengths |
|------|------|-----------|-----------|
| 1 | **ElevenLabs** | 4.2-4.5 | Best naturalness, emotion, voice cloning |
| 2 | **Cartesia** | 4.1-4.3 | Fastest latency, real-time apps |
| 3 | **OpenAI TTS** | 3.8-4.0 | Consistent, clean audio, low noise |
| 4 | **Google Cloud** | 3.7-3.9 | Multi-language, enterprise-grade |
| 5 | **Amazon Polly** | 3.6-3.8 | SSML control, AWS integration |

**Key Quality Findings:**
- ElevenLabs: 82% pronunciation accuracy vs OpenAI's 77%
- ElevenLabs: 45% high naturalness rating vs OpenAI's 22%
- OpenAI: 89% noise-free output (cleanest)
- ElevenLabs: 150ms TTFA vs OpenAI's 200ms (faster)
- ElevenLabs: 5% hallucination rate vs OpenAI's 10%

### Free / Open-Source Tier

| Tool | Free Tier | Paid Starting At | Cost/Unit | Quality | Python SDK | Best For |
|------|-----------|------------------|-----------|---------|------------|----------|
| **Coqui TTS** | Unlimited (local) | N/A | $0 | ★★★★ | ✅ `coqui-tts` | Local, voice cloning |
| **Google Cloud TTS** | 1M WaveNet/month | $4/1M | $16/1M Neural | ★★★★ | ✅ Official | Multi-language |
| **Amazon Polly** | 5M chars/month (12mo) | $4/1M | $16/1M Neural | ★★★☆ | ✅ boto3 | AWS integration |

**Coqui TTS Details:**
- XTTS-v2 model: 17 languages, voice cloning with 6-second samples
- Runs locally (requires GPU for best performance)
- Community-maintained fork at `idiap/coqui-ai-TTS`
- **Quality:** Excellent for local; occasional artifacts on edge cases
- **Limitation:** Original company shut down Dec 2023

### Low-Cost Tier ($0.01-0.02/1K chars)

| Tool | Free Tier | Paid Starting At | Cost/Unit | Quality | Python SDK | Best For |
|------|-----------|------------------|-----------|---------|------------|----------|
| **OpenAI TTS** | None | Pay-as-you-go | $15/1M (TTS-1) | ★★★★ | ✅ `openai` | Simple, consistent |
| **Azure TTS** | 500K chars/month | $4/1M | $16/1M Neural | ★★★★ | ✅ Azure SDK | 400+ voices, emotion |

**OpenAI TTS Details:**
- Models: `tts-1` (fast), `tts-1-hd` (quality)
- 6 voices: alloy, echo, fable, onyx, nova, shimmer
- **Quality:** Clean output, consistent but limited expressiveness
- **Limitation:** No voice cloning, limited voice options

### Mid-Tier ($0.10-0.30/1K chars)

| Tool | Free Tier | Paid Starting At | Cost/Unit | Quality | Python SDK | Best For |
|------|-----------|------------------|-----------|---------|------------|----------|
| **Play.ht** | 12,500 chars/month | $31/month | ~$0.12/1K | ★★★★ | ✅ REST | 600+ voices |
| **Murf.ai** | Limited trial | $29/month | ~$0.15/1K | ★★★☆ | REST | Video voiceovers |

### Premium Tier (Best Quality)

| Tool | Free Tier | Paid Starting At | Cost/Unit | Quality | Python SDK | Best For |
|------|-----------|------------------|-----------|---------|------------|----------|
| **ElevenLabs** | 10,000 chars/month | $5/month | ~$0.20/1K | ★★★★★ | ✅ `elevenlabs` | Best realism |

**ElevenLabs Details:**
- Plans: Starter ($5/30K), Creator ($22/100K), Pro ($99/500K), Scale ($330/2M)
- Flash/Turbo models: cheaper for high volume
- **Quality:** Industry-leading naturalness, emotion control, voice cloning
- Voice cloning from ~30 second samples
- 32+ languages, 3000+ voices

---

## 3. Speech-to-Text / Transcription

### Quality Rankings (Dec 2025)

| Rank | Tool | WER (Word Error Rate) | Strengths |
|------|------|----------------------|-----------|
| 1 | **ElevenLabs Scribe** | ~3.3% (English) | 99 languages, speaker ID, best accuracy |
| 2 | **Deepgram Nova-3** | ~4.5% | Real-time, ultra-low latency |
| 3 | **AssemblyAI** | ~5.2% | Sentiment, summarization, content moderation |
| 4 | **OpenAI Whisper** | ~6.7% | Open-source, 99 languages |
| 5 | **Google Speech-to-Text** | ~7.0% | 125+ languages, enterprise-grade |

### Free / Low-Cost Options

| Tool | Free Tier | Cost | Features |
|------|-----------|------|----------|
| **OpenAI Whisper** (open-source) | Unlimited (local) | Compute only | Full control, offline, 99 languages |
| **OpenAI Whisper API** | $5 free credits | $0.006/min | Simple API, 99 languages |
| **GPT-4o Transcribe** | Included in credits | $0.006/min | Better accuracy than Whisper |
| **GPT-4o Mini Transcribe** | Included in credits | $0.003/min | Cost-effective option |
| **Google Cloud STT** | 60 min/mo free | $0.016/min | Chirp model, real-time |

### Premium Options

| Tool | Cost | Best For |
|------|------|----------|
| **ElevenLabs Scribe** | Contact for API | Best accuracy, 99 languages |
| **Deepgram** | $0.0043/min (Nova-2) | Real-time, <300ms latency |
| **AssemblyAI** | $0.0037/min | Analytics (sentiment, topics) |
| **Amazon Transcribe** | $0.024/min (standard) | AWS integration, medical/legal |

**OpenAI Transcription Details:**
- Whisper: $0.006/min - legacy model, still excellent
- GPT-4o Transcribe: $0.006/min - improved accuracy
- GPT-4o Transcribe + Diarization: $0.006/min - includes speaker ID
- GPT-4o Mini: $0.003/min - 50% cheaper, good for high volume
- Supports: mp3, mp4, mpeg, mpga, m4a, wav, webm (max 25MB)

**Self-Hosting vs API (Break-even Analysis):**
| Volume | OpenAI API | Self-Host (A100 GPU) | Winner |
|--------|------------|----------------------|--------|
| <100 hrs/mo | $36 | $276/mo + setup | API |
| 500 hrs/mo | $180 | $276/mo | API (barely) |
| 1000+ hrs/mo | $360 | $276/mo | Self-Host |

---

## 4. Image Generation APIs

### NEW: Nano Banana Pro (Google Gemini 3 Pro Image)
**Released: November 2025** - Google DeepMind's flagship image generation model.

| Access Method | Cost | Quality | Best For |
|---------------|------|---------|----------|
| **Google AI Pro** | $19.99/month | 1MP, 3/day limit | Testing, casual use |
| **Google AI Ultra** | $34.99/month | Full 4K access | Production quality |
| **Gemini API** | ~$0.13-0.15/4K image | Full resolution | Developer integration |
| **Third-party (Kie.ai)** | ~$0.02/image | Same model | Budget bulk generation |

**Nano Banana Pro Features:**
- Up to 16MP (4K) resolution output
- Accurate text rendering in images
- Multi-image composition (up to 8 reference images)
- Physics-aware, hyper-realistic output
- Multi-angle character consistency
- Style transfer and image editing
- **Quality:** ★★★★★ - Currently best-in-class for image generation

**Nano Banana (Base) vs Pro:**

| Feature | Nano Banana (2.5 Flash) | Nano Banana Pro (Gemini 3) |
|---------|-------------------------|---------------------------|
| Cost | ~$0.039/image | ~$0.13-0.15/image |
| Resolution | Up to 1K | Up to 4K (16MP) |
| Speed | Faster | Slower, higher quality |
| Text rendering | Good | Excellent |

**Model Selection Notes (Dec 2025):**
- **`gemini-3-pro-image-preview`**: Best for infographics with text - clean, readable typography
- **`imagen-4.0-generate-001`**: Better for photorealistic images without text - has text rendering issues
- **`gemini-2.5-flash-image`**: Fast, lower quality - good for prototyping
- Use multimodal chat API with `response_modalities=['TEXT', 'IMAGE']` for Nano Banana Pro

### Other Image Generation APIs

| Tool | Free Tier | Paid | Cost/Image | Quality | Best For |
|------|-----------|------|------------|---------|----------|
| **Midjourney** | None | $10/month | ~$0.05 | ★★★★★ | Artistic, stylized |
| **DALL-E 3** | None | Pay-per-use | $0.04-0.08 | ★★★★ | Text integration |
| **Stable Diffusion** | Unlimited (local) | $0 | Compute only | ★★★★ | Local, customizable |
| **Flux** | Via third-party | Varies | $0.03-0.05 | ★★★★☆ | Speed + quality balance |

---

## 5. Video Generation & Image Animation

### Video Arena Leaderboard (Dec 17, 2025)
Based on Artificial Analysis Video Arena (blind human evaluations):

| Rank | Model | Elo Score | Native Audio | Key Strength |
|------|-------|-----------|--------------|--------------|
| 1 | **Runway Gen-4.5** | 1,247 | ✅ (Dec 11) | Best overall, physics, consistency |
| 2 | **Google Veo 3** | ~1,220 | ✅ | Highest fidelity, audio sync |
| 3 | **Google Veo 3.1** | ~1,200 | ✅ | Fast + quality + audio |
| 4 | **Kling 2.6** | ~1,190 | ✅ | Audio-visual, singing/rap |
| 5 | **Kling 2.5** | ~1,180 | ❌ | Complex motion, I2V leader |
| 6 | **Kling O1** | NEW | ❌ | Unified gen+edit+inpaint |
| 7 | **Sora 2 Pro** | ~1,150 | ✅ | Physics simulation |
| 8 | **Luma Ray 2** | ~1,100 | ❌ | Natural motion, physics |

### Quality Rankings (Dec 2025)
Based on comprehensive testing across motion quality, prompt adherence, and visual fidelity:

| Rank | Tool | Overall | Motion | Prompt Adherence | Best For |
|------|------|---------|--------|------------------|----------|
| 1 | **Runway Gen-4.5** | ★★★★★+ | Excellent | Excellent | Best overall, now has audio |
| 2 | **Google Veo 3.1** | ★★★★★ | Excellent | Excellent | Native audio, highest fidelity |
| 3 | **Kling 2.6** | ★★★★★ | Excellent | Excellent | Native audio, speech+singing |
| 4 | **OpenAI Sora 2** | ★★★★★ | Excellent | Excellent | Physics, native audio |
| 5 | **Kling 2.5/O1** | ★★★★★ | Excellent | Excellent | Complex motion, editing |
| 6 | **Runway Gen-4** | ★★★★☆ | Very Good | Very Good | Cinematic, consistency |
| 7 | **Luma Ray 2** | ★★★★ | Good | Good | Physics, smooth motion |
| 8 | **Hailuo/MiniMax** | ★★★★ | Good | Good | Speed, value |
| 9 | **HunyuanVideo 1.5** | ★★★★ | Good | Very Good | Open source, local |
| 10 | **Pika 2.5** | ★★★☆ | Decent | Decent | Quick tests, effects |

### Image Animation Comparison (Image-to-Video)
**Critical for your workflow** - animating generated/stock images:

| Tool | Image Animation | Max Length | Quality | Speed | API Available | Native Audio |
|------|-----------------|------------|---------|-------|---------------|--------------|
| **Runway Gen-4.5** | ★★★★★+ | 16s | Best overall | Fast | ✅ Official | ✅ (Dec 11) |
| **Kling 2.6** | ★★★★★ | 10s | Best audio sync | 2-3 min | ✅ Via PiAPI | ✅ |
| **Veo 3.1** | ★★★★★ | 8s (+extend) | Highest fidelity | Slow | ✅ Vertex AI | ✅ |
| **Kling 2.5 Master** | ★★★★★ | 10s | Best motion | 2-3 min | ✅ Via PiAPI | ❌ |
| **Runway Gen-4** | ★★★★☆ | 10s | Best consistency | Fast | ✅ Official | ❌ |
| **Luma Ray 2** | ★★★★ | 5s | Smooth physics | Fast | ✅ Via PiAPI | ❌ |
| **HunyuanVideo 1.5** | ★★★★ | 10s | Good (local) | Varies | ✅ Open Source | ❌ |
| **Hailuo 2** | ★★★★ | 6s | Good detail | 4-5 min | ✅ MiniMax API | ❌ |
| **Pika 2.5** | ★★★ | 5s | Decent | Fast | ❌ Web only | ❌ |

**Image Animation Quality Notes (Updated Dec 2025):**
- **Runway Gen-4.5:** NEW #1 - Best prompt adherence, physics, consistency. Native audio as of Dec 11. Only weakness is premium pricing.
- **Kling 2.6:** Native audio-visual generation - speech, singing, rap, SFX all generated with video. Best for talking characters.
- **Kling 2.5:** Best for complex motion without audio needs, facial expressions, dynamic scenes. Top choice for silent animation.
- **Veo 3.1:** Highest overall quality + native audio sync. Premium pricing but unmatched fidelity for final production.
- **Runway Gen-4:** Best subject consistency, maintains character identity well. Most reliable API for pure video.
- **Luma Ray 2:** Best physics simulation, natural micro-expressions. Can be unpredictable with prompts.
- **HunyuanVideo 1.5:** Best open-source option. Runs locally on 14GB VRAM. 75s generation on RTX 4090 with step-distillation.
- **Hailuo 2:** Good balance of speed and quality. Strong facial detail but occasional artifacts.

### Free Tier

| Tool | Free Tier | Paid Starting At | Quality | Python SDK | Best For |
|------|-----------|------------------|---------|------------|----------|
| **Pika Labs** | 80 credits/month | $8/month | ★★★☆ | ❌ Web only | Quick social clips |
| **Kling AI** | 66 credits/day | $10/month | ★★★★☆ | Via PiAPI | Realistic motion |
| **Luma Dream Machine** | Limited (watermark) | $10/month | ★★★★ | Via PiAPI | Smooth motion |

### Mid-Tier ($0.05-0.15/second)

| Tool | Free Tier | Paid Starting At | Cost/Unit | Quality | Python SDK |
|------|-----------|------------------|-----------|---------|------------|
| **Runway Gen-4** | 125 credits (once) | $12/month | $0.05/s (Turbo) | ★★★★☆ | ✅ Official |
| **Kling 2.0** | 66 credits/day | $37/month (Pro) | ~$0.05/s | ★★★★★ | Via PiAPI |

**Runway API Details (Dec 2025 - Gen-4.5 Update):**
- **Gen-4.5:** NEW - 15 credits/second ($0.15/s) - best quality, native audio
- Gen-4 Turbo: 5 credits/second ($0.05/s) - fast, good quality
- Gen-4: 10 credits/second ($0.10/s) - better quality
- Gen-4 Aleph: 15 credits/second ($0.15/s) - cutting edge
- Plans: Standard ($12/mo), Pro ($28/mo), Unlimited ($76/mo)
- Unlimited plan: Unlimited Gen-4.5/4 generations in Explore mode
- **Quality:** #1 on Video Arena (Elo 1,247) - best physics, consistency, audio
- **Limitation:** 5-16 second max per generation

**Kling 2.6/2.5/O1 Details (Dec 2025 - Major Update):**
- **Kling 2.6:** Native audio-visual generation (speech, singing, rap, SFX)
- **Kling O1:** Unified multimodal (generate + edit + inpaint in one model)
- Standard: $10/month, 660 credits
- Pro: $37/month, professional tier
- Premier: $92/month, 8,000 credits (70 credits = 10s video)
- **Quality:** Best for complex motion, animations, facial expressions
- **Kling 2.6 Audio:** EN/CN voice, multi-character dialogue, ambient sounds
- **Limitation:** Slow generation (~6 min), no unlimited plan

### Premium Tier ($0.15-0.75/second)

| Tool | Access | Cost/Unit | Quality | Native Audio | Best For |
|------|--------|-----------|---------|--------------|----------|
| **Veo 3.1** | Vertex AI | $0.10-0.75/s | ★★★★★+ | ✅ Yes | Highest quality + audio |
| **Sora 2** | ChatGPT/API | $0.10-0.50/s | ★★★★★ | ✅ Yes | OpenAI ecosystem |
| **Runway Aleph** | Pro+ plans | ~$0.15/s | ★★★★★ | ❌ | Cutting-edge quality |

**Google Veo 3/3.1 Details:**
- Veo 3.1 Fast: $0.10/s without audio, $0.15/s with audio
- Veo 3: $0.50/s without audio, $0.75/s with audio
- Third-party (Kie.ai, fal.ai): ~$0.10-0.15/s (cheaper)
- Access: Google AI Pro ($19.99/mo) for Fast, Ultra ($249.99/mo) for full
- Max 8 seconds per generation (extendable to 148s)
- **Quality:** Highest fidelity + native audio sync - ONLY model with native audio

**OpenAI Sora 2 Details (Sept 2025):**
- API: $0.10/s (720p), $0.30/s (720p Pro), $0.50/s (1024p Pro)
- ChatGPT Plus: 1,000 credits/mo (~30 videos/day free)
- ChatGPT Pro: 10,000 credits/mo (~100 videos/day)
- Third-party (Kie.ai, laozhang.ai): $0.15-0.20/video (60%+ cheaper)
- Max lengths: 4s/8s/12s (Sora 2), 10s/15s/25s (Sora 2 Pro)
- **Quality:** Excellent physics, realistic motion, synced audio
- **Limitation:** Invite-only app, enterprise API requires $50k+ commitment

### Avatar/Talking Head

| Tool | Free Tier | Paid Starting At | Quality | Best For |
|------|-----------|------------------|---------|----------|
| **HeyGen** | Limited trial | $99/month | ★★★★ | Pro avatars |
| **Synthesia** | None | $18/month | ★★★☆ | Corporate |

### Open Source Video Models (NEW - Dec 2025)
**Run locally or on rented GPUs - no per-generation costs**

| Model | Parameters | Min VRAM | Quality | API Cost | Best For |
|-------|------------|----------|---------|----------|----------|
| **HunyuanVideo 1.5** | 8.3B | 14GB (8GB w/GGUF) | ★★★★ | $0 (local) | Best open-source |
| **ByteDance Vidi2** | 12B | 24GB | ★★★★ | $0 (local) | Video editing/understanding |
| **Wan 2.5** | 27B MoE | 24GB | ★★★★ | $0 (local) | Cinematic, artistic |

**HunyuanVideo 1.5 Details (Released Nov 20, Training Code Dec 5):**
- Apache 2.0 license - fully commercial use
- 8.3B parameters (down from 13B in v1) with 2x faster inference
- Step-distilled model: 75 seconds on RTX 4090 (Dec 5 update)
- T2V and I2V support, 720p native with 1080p upscaling
- **VRAM Options:**
  - Full model: 16-24GB VRAM recommended
  - GGUF quantized: 8-12GB VRAM
  - 5G build: As low as 6GB VRAM (quality loss)
  - WanGP: 6GB VRAM with LoRA Accelerator
- **Quality:** Beats Wan2.2 and Kling2.1 in instruction following (92% vs 87% vs 84%)
- ComfyUI support with extensive community workflows
- **Best For:** High-volume batch processing, custom fine-tuning, privacy-sensitive applications

**ByteDance Vidi2 Details (Released Dec 1):**
- 12B parameters with Spatio-Temporal Grounding (STG)
- Powers TikTok "Smart Split" feature
- Focus on video editing/understanding rather than pure generation
- Pixel-level object tracking and manipulation
- **Best For:** Video editing pipelines, content repurposing

**GPU Rental Cost Comparison (HunyuanVideo 1.5):**
| Provider | RTX 4090 | Generation Time | Cost per Video |
|----------|----------|-----------------|----------------|
| Vast.ai | $0.40-0.60/hr | 75 sec | ~$0.01-0.02 |
| RunPod | $0.44/hr | 75 sec | ~$0.01 |
| Local | N/A | 75 sec | Electricity only |

---

## 6. Music Generation APIs

### Quality Rankings (Dec 2025)

| Rank | Tool | Quality | Vocals | Best For |
|------|------|---------|--------|----------|
| 1 | **Suno V5** | ★★★★★ | ✅ Excellent | Full songs with lyrics |
| 2 | **Udio 1.5** | ★★★★★ | ✅ Excellent | Audio quality, production |
| 3 | **Google Lyria 2** | ★★★★☆ | ❌ Instrumental only | API integration, quality |
| 4 | **Riffusion** | ★★★☆ | ❌ Instrumental only | Real-time, interactive |

### Suno AI
**Best for full songs with vocals and lyrics**

| Access | Cost | Output |
|--------|------|--------|
| **Free Tier** | $0 | 50 credits/day (~10 songs), non-commercial |
| **Pro** | $10/mo | 2,500 credits/mo, commercial use |
| **Premier** | $30/mo | 10,000 credits/mo |
| **API (official)** | ~$0.04/creation | Enterprise access |
| **Third-party APIs** | $0.01-0.02/call | Via SunoAPI.com, laozhang.ai |

**Suno V5 Features (Sept 2025):**
- Studio-quality audio output
- Natural vocals (nearly indistinguishable from human)
- Up to 4 minutes per song
- ELO score: 1,293 (vs V4.5's 1,208)
- 320kbps MP3 output

### Udio
**Best audio quality and production value**

| Access | Cost | Output |
|--------|------|--------|
| **Free Tier** | $0 | 100 credits/mo + 10/day (~5 songs/day) |
| **Standard** | $10/mo | 1,200 credits/mo |
| **Pro** | $30/mo | 6,000 credits/mo, commercial use |
| **API** | Via third-party | MusicAPI.ai, udioapi.pro |

**Udio 1.5 Features:**
- Higher fidelity than Suno (subjectively)
- Songs up to 2:10
- Style reference from audio
- Better genre adherence

### Google Lyria 2
**Best for API integration and instrumental**

| Access | Cost | Output |
|--------|------|--------|
| **Vertex AI API** | $0.06/30s | 48kHz WAV, instrumental |
| **AI Studio** | Free (limited) | Testing and prototyping |
| **Lyria RealTime** | Free (experimental) | Real-time, interactive music |
| **Replicate** | ~$0.03/30s | Third-party access |

**Lyria 2 Features:**
- 48kHz stereo WAV output
- 30 seconds per generation
- BPM, key, mood control
- SynthID watermarking
- Instrumental only (no vocals)
- 10-20 second generation time

### Music API Comparison

| Feature | Suno V5 | Udio 1.5 | Lyria 2 |
|---------|---------|----------|---------|
| Vocals | ✅ Excellent | ✅ Excellent | ❌ None |
| Max Length | 4 min | 2:10 | 30s |
| Commercial | Paid tiers | Paid tiers | ✅ API |
| API Access | Limited | Third-party | ✅ Official |
| Real-time | ❌ | ❌ | ✅ Lyria RT |
| Best Quality | Vocals | Production | Instrumental |

---

## 7. Stock Footage APIs

### Free Tier

| Tool | Free Tier | Rate Limits | Quality | Python SDK | Best For |
|------|-----------|-------------|---------|------------|----------|
| **Pexels** | Unlimited (attribution) | 200/hr, 20K/month | ★★★★ | ✅ REST | Curated quality |
| **Pixabay** | Unlimited (mention) | 100/min | ★★★☆ | ✅ REST | Large library |

### Paid Tier

| Tool | Paid Starting At | Cost/Unit | Quality | Best For |
|------|------------------|-----------|---------|----------|
| **Storyblocks** | ~$30/month | Unlimited | ★★★★ | High volume |
| **Shutterstock** | Pay-per-download | $9-15/clip | ★★★★★ | Premium quality |
| **Getty Images** | Enterprise | $50-500/clip | ★★★★★ | Editorial, premium |

---

## 8. Template-Based Video APIs

| Tool | Free Tier | Paid Starting At | Cost/Unit | Quality | Python SDK |
|------|-----------|------------------|-----------|---------|------------|
| **Shotstack** | 20 renders (watermark) | $49/month | $0.20-0.40/min | ★★★★ | ✅ Official |
| **Creatomate** | 20 renders/month | $41/month | $0.06-0.28/min | ★★★★ | ✅ Node.js |
| **Bannerbear** | 30 images/month | $49/month | $0.10-0.20/render | ★★★☆ | ✅ REST |
| **Placid** | 50 creatives/month | $29/month | ~$0.08/render | ★★★☆ | ✅ REST |

---

## 9. Video Editing / Composition

### Free / Open-Source

| Tool | License | Language | Quality | Limitations |
|------|---------|----------|---------|-------------|
| **MoviePy** | MIT | Python | ★★★★ | CPU-bound, no GPU |
| **FFmpeg** | LGPL/GPL | CLI/C | ★★★★★ | Complex syntax |
| **Remotion** | Special* | React/JS | ★★★★★ | License for companies >3 |

**MoviePy** - Best for Python automation:
```python
pip install moviepy
# v2.0 released with breaking changes
# Supports: cuts, concatenation, compositing, text overlays, transitions
```

**FFmpeg** - Industry standard:
```bash
pip install ffmpeg-python
# Supports virtually all formats, most reliable encoding
```

**Remotion** - React framework for video:
- Free for individuals/teams ≤3 people
- Company License required for larger teams
- Remotion Lambda for serverless AWS rendering
- Best for: Branded templates, data-driven videos, complex animations
- Sweet spot: Animated text overlays, stats displays, caption animations

---

## 10. Workflow Automation

### ComfyUI
**Node-based visual workflow builder** for AI image/video generation pipelines.

| Feature | Details |
|---------|---------|
| **Cost** | Free, open-source |
| **Platform** | Local (requires GPU) or Cloud (RunComfy, Comfy Cloud) |
| **Best For** | Complex multi-step workflows, batch processing |

**Key Capabilities:**
- Visual node-based interface (like Unreal Blueprints)
- Batch processing: 100+ images/videos overnight
- Auto Queue for continuous generation loops
- CSV-driven prompts for data-driven content
- Supports: Flux, SDXL, Wan 2.1/2.2, HunyuanVideo, LTX Video

**Popular Workflow Patterns:**
- Text-to-Image → Image-to-Video → Upscale → Frame interpolation
- Batch image generation with style consistency
- Video super-resolution (RealESRGAN 4x)
- Frame interpolation (GIMM-VFI up to 10x)

**Cloud Options:**
| Provider | Cost | Features |
|----------|------|----------|
| **RunComfy** | From $9/mo | Pre-configured workflows |
| **Comfy Cloud** | Beta | Official cloud platform |
| **RunPod** | ~$0.22-0.40/hr | Raw GPU rental |

**Local Installation:**
```bash
# Install at ~/ComfyUI (default path for pipeline integration)
cd ~
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
python main.py
```

### AnimateDiff (Local Image-to-Video)
**Free, open-source image animation** - run via ComfyUI or standalone.

| Feature | Details |
|---------|---------|
| **Cost** | Free (local GPU required) |
| **VRAM** | 8-12GB minimum |
| **Best For** | Image-to-video animation, batch processing |

**Capabilities:**
- Converts static images to short video clips (2-4 seconds typical)
- Motion modules for consistent animation style
- LoRA support for custom motion types
- Batch processing via ComfyUI workflows

**Installation (via ComfyUI):**
```bash
cd ~/ComfyUI/custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
# Download motion modules from Hugging Face
```

**Quality:** ★★★★ - Good for bulk animation, may need upscaling for production

### RIFE (Frame Interpolation)
**Real-Time Intermediate Flow Estimation** - smooths video by generating intermediate frames.

| Feature | Details |
|---------|---------|
| **Cost** | Free (local) |
| **Binary** | `rife-ncnn-vulkan` |
| **Model** | `rife-v4.6` (latest) |
| **Best For** | Frame interpolation, pixel art animation, smooth transitions |

**Capabilities:**
- Interpolate 2x, 4x, 8x frame rate
- Preserves pixel art style (unlike other interpolation methods)
- Uses Metal acceleration on M-series Macs
- Lightweight and fast

**Installation (macOS):**
```bash
brew install rife-ncnn-vulkan
# Or download from https://github.com/nihui/rife-ncnn-vulkan/releases
```

**Usage:**
```bash
rife-ncnn-vulkan -i input.mp4 -o output.mp4 -m rife-v4.6 -x
# -x enables 2x interpolation (24fps → 48fps)
```

**Quality:** ★★★★★ - Best for pixel art, game footage, preserves style integrity

### GPU Rental (for Self-Hosted Workflows)

| Provider | A100 40GB | A100 80GB | H100 | RTX 4090 |
|----------|-----------|-----------|------|----------|
| **Vast.ai** | $0.66-1.20/hr | $0.78-1.80/hr | $2.85-3.50/hr | $0.40-0.60/hr |
| **RunPod** | $0.74/hr | $1.09/hr | $3.89/hr | $0.44/hr |
| **Thunder Compute** | Similar | Similar | Similar | $0.36/hr |

**Break-Even Analysis (GPU vs API):**
| Use Case | API Cost/mo | GPU Rental/mo | Break-Even |
|----------|-------------|---------------|------------|
| TTS (Coqui vs ElevenLabs) | $5-330 | $2-5 (few hrs) | ~$20/mo |
| Images (SDXL vs Nano Banana) | $10-75 | ~$1.50 (2 hrs batch) | ~$30/mo |
| Video (Wan vs Kling API) | $50-200 | ~$20-50 | ~$100/mo |

**When to Use GPU Rental:**
✅ Open-source models at volume (Coqui TTS, SDXL, Whisper)
✅ Fine-tuning custom models
✅ Privacy/data residency requirements
✅ Batch processing (spin up, process, shutdown)

❌ Low volume (<$20/mo API costs)
❌ Need instant availability (cold start delays)
❌ Want simplicity (more DevOps overhead)

---

## 11. MCP Servers (Model Context Protocol)

### Production-Ready

| Server | Capabilities | Status |
|--------|--------------|--------|
| **MiniMax-MCP** | TTS, video gen, image gen, music, voice cloning | ✅ Production |
| **Epidemic Sound MCP** | Music search, context-aware audio | ✅ Beta |

### Community-Built

| Server | Capabilities |
|--------|--------------|
| **PiAPI MCP** | Midjourney, Flux, Kling, Hunyuan, Udio, Trellis |
| **Pollinations MCP** | Images, audio, text (no auth) |
| **Luma AI MCP** | Video generation |
| **AllVoiceLab MCP** | TTS, voice cloning, video translation |

---

## 12. Recommendations

### Best Free Stack (Testing/Prototyping)
**Total Cost: $0/month**

| Component | Tool | Quality | Notes |
|-----------|------|---------|-------|
| TTS | Coqui TTS (local) | ★★★★ | XTTS-v2, requires GPU |
| Images | Nano Banana Free (3/day) | ★★★★★ | Via Gemini app |
| Video/Animation | Pika Labs Free OR Kling Free | ★★★-★★★★ | 80 credits/month or 66/day |
| **NEW: Local Video** | HunyuanVideo 1.5 | ★★★★ | Requires 14GB+ VRAM |
| Stock | Pexels + Pixabay | ★★★★ | Free with attribution |
| Editing | MoviePy + FFmpeg | ★★★★★ | Full Python control |

### Best Low-Budget Stack (<$50/month)
**Estimated Cost: $30-50/month**

| Component | Tool | Cost | Quality |
|-----------|------|------|---------|
| TTS | OpenAI TTS-1 | ~$5/month | ★★★★ |
| Images | Nano Banana API | ~$5/month | ★★★★★ |
| Video/Animation | Kling Standard OR Runway | $10-12/month | ★★★★☆ |
| Stock | Pexels (Free) | $0 | ★★★★ |
| Templates | Creatomate | $41/month | ★★★★ |

**Output:** ~25-50 30-second videos/month

### Best Quality Stack - API (Image Animation Focus)
**Estimated Cost: $150-300/month**

| Component | Tool | Cost | Quality |
|-----------|------|------|---------|
| TTS | ElevenLabs Pro | $99/month | ★★★★★ |
| Images | Nano Banana Pro | ~$20/month | ★★★★★ |
| **Animation** | **Kling 2.6 + Runway Gen-4.5** | $65-100/month | ★★★★★ |
| Stock | Storyblocks | $30/month | ★★★★ |
| Editing | MoviePy + Remotion | $0 | ★★★★★ |

**Why this combo:** Kling 2.6 for native audio clips, Runway Gen-4.5 for best overall quality

### Best Quality Stack - Hybrid (ComfyUI + APIs)
**Estimated Cost: $50-100/month** (GPU rental + minimal API)

| Component | Tool | Cost | Quality |
|-----------|------|------|---------|
| TTS | OpenAI or Coqui (local) | $0-10/month | ★★★★ |
| Images | Flux via ComfyUI | ~$10/month GPU | ★★★★★ |
| **Video** | **HunyuanVideo 1.5 (local/cloud)** | ~$20-30/month GPU | ★★★★ |
| Audio clips | Kling 2.6 API (for talking) | ~$20/month | ★★★★★ |
| Editing | MoviePy + Remotion | $0 | ★★★★★ |

**Why this combo:** Best for high-volume, HunyuanVideo for bulk, Kling 2.6 API only for talking/audio needs

### Premium Stack (Best Possible Quality)
**Estimated Cost: $400-600/month**

| Component | Tool | Cost | Quality |
|-----------|------|------|---------|
| TTS | ElevenLabs Scale | $330/month | ★★★★★ |
| Images | Nano Banana Pro + Midjourney | ~$35/month | ★★★★★ |
| **Video** | **Runway Gen-4.5 Unlimited + Veo 3** | ~$150/month | ★★★★★+ |
| Avatar | HeyGen Pro | $99/month | ★★★★ |
| Stock | Storyblocks | $30/month | ★★★★ |

### Quick Selection by Use Case (Updated Dec 2025)

| Use Case | Image Gen | Animation | TTS | Total/month |
|----------|-----------|-----------|-----|-------------|
| **Budget Testing** | Nano Banana Free | Kling Free | Coqui | $0 |
| **Social Content** | Nano Banana | **Kling 2.6 Standard** | OpenAI | ~$40 |
| **Quality Content** | Nano Banana Pro | **Runway Gen-4.5 + Kling** | ElevenLabs | ~$200 |
| **Premium Production** | Midjourney + Nano Banana | **Runway Gen-4.5 Unlimited** | ElevenLabs | ~$500 |
| **Talking Characters** | - | **Kling 2.6** (native audio) | Built-in | ~$40 |
| **High Volume Local** | Flux (ComfyUI) | **HunyuanVideo 1.5** | Coqui | ~$30 GPU |

### Goated Bets Specific Pipeline Recommendations

**Tier 1: Quick MVP (API-only)**
- Images: Nano Banana Pro via fal.ai ($0.039/image)
- Animation: **Kling 2.6 via PiAPI** ($0.55/5s with audio) - native TTS included!
- Music: Suno via third-party ($0.10-0.15/song)
- Composition: MoviePy (free)
- **Cost: ~$100/month for 100 videos**

**Tier 2: Quality Production (Hybrid)**
- Images: Nano Banana Pro + Flux (ComfyUI)
- Animation: **Runway Gen-4.5** for hero content, **HunyuanVideo 1.5** for bulk
- Music: Suno API
- Composition: Remotion
- **Cost: ~$150/month for 100 videos**

**Tier 3: Maximum Volume (ComfyUI + GPU)**
- Images: Flux Dev on RTX 4090 ($0.40-0.60/hr)
- Animation: **HunyuanVideo 1.5** (step-distilled, 75s/video)
- Audio clips only: Kling 2.6 API for talking characters
- Music: Suno API
- **Cost: ~$50-80/month for 100+ videos**

---

## Appendix: Python Integration Examples

### OpenAI TTS
```python
from openai import OpenAI
client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Your text here"
)
response.stream_to_file("output.mp3")
```

### ElevenLabs
```python
from elevenlabs import generate, save

audio = generate(
    text="Your text here",
    voice="Rachel",
    model="eleven_multilingual_v2"
)
save(audio, "output.mp3")
```

### Runway API (Image Animation)
```python
import runwayml

client = runwayml.RunwayML()

# Image to Video (Animation)
task = client.image_to_video.create(
    model="gen4_turbo",
    prompt_image="https://example.com/image.png",
    prompt_text="Camera slowly zooms in, subject blinks naturally"
)
# Poll for completion
```

### Nano Banana Pro (Google AI)
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-3-pro-image')

response = model.generate_content(
    "A photorealistic portrait of a scientist in a lab"
)
# Handle image response
```

### MoviePy Composition
```python
from moviepy.editor import *

video = VideoFileClip("video.mp4")
audio = AudioFileClip("narration.mp3")
music = AudioFileClip("background.mp3").volumex(0.3)

final_audio = CompositeAudioClip([audio, music])
final = video.set_audio(final_audio)
final.write_videofile("output.mp4")
```

---

## Key Findings Summary (Updated Dec 17, 2025)

1. **Runway Gen-4.5** (Dec 1) - NEW #1 on Video Arena (Elo 1,247). Best prompt adherence, physics, consistency. Native audio added Dec 11. Premium but worth it for quality.

2. **Kling 2.6** (Dec 3) - Native audio-visual generation is a game-changer. Generates speech, singing, rap, sound effects WITH video in one pass. EN/CN support. Eliminates need for separate TTS for talking characters.

3. **HunyuanVideo 1.5** (Nov 20) - Best open-source video model. 8.3B params, runs on 14GB VRAM (6GB with optimizations). Step-distilled model generates video in 75 seconds on RTX 4090. Training code released Dec 5.

4. **Image Animation Quality Leaders (Dec 2025):**
   - **Runway Gen-4.5:** Best overall, now has audio
   - **Kling 2.6:** Best for talking characters (native audio)
   - **Kling 2.5:** Best for complex motion without audio needs
   - **Veo 3.1:** Highest fidelity + audio (premium)
   - **HunyuanVideo 1.5:** Best open-source (local/cloud)

5. **Native Audio Revolution:** Now four models support native audio:
   - Runway Gen-4.5 (Dec 11 update)
   - Kling 2.6 (speech, singing, rap, SFX)
   - Google Veo 3/3.1 (highest quality)
   - OpenAI Sora 2 (physics-focused)

6. **Cost-Effective Pipeline (Goated Bets):** 
   - Kling 2.6 for talking character clips ($0.55/5s with audio)
   - HunyuanVideo 1.5 for bulk silent animations ($0.01/video on GPU)
   - Total: ~$50-100/month for 100+ videos

7. **API Availability:** 
   - Runway: Best official API, Gen-4.5 available
   - Kling 2.6: Via PiAPI/Kie.ai ($0.28-1.10/video)
   - HunyuanVideo 1.5: Open source, run locally or fal.ai (coming soon)

8. **Open Source Gains:** HunyuanVideo 1.5 + ByteDance Vidi2 make local video generation viable. Break-even vs APIs at ~$30/month volume.

9. **TTS Disruption:** Kling 2.6's native audio may reduce need for separate TTS for video content. Still use ElevenLabs/OpenAI for non-video audio.

10. **Kling O1:** Unified generation + editing + inpainting model. Watch for API access - could simplify pipelines significantly.

---

## 13. Free Tools Integration (Pipeline Built-ins)

### Tier 1: Zero Cost, Zero API Key
Already integrated into the pipeline - unlimited usage.

| Tool | Category | Module | Purpose |
|------|----------|--------|---------|
| **Pillow/PIL** | Image Processing | `pil_processor.py` | Logo overlay, aspect conversion, gradients, text cards |
| **FFmpeg** | Video Processing | `ffmpeg_processor.py` | Ken Burns, slideshows, trimming, concatenation |
| **MoviePy** | Video Composition | `L6_assembly.py` | Multi-track editing, transitions |
| **Pexels API** | Stock Images | `L5_media.py` | 200 req/hr free |
| **Pixabay API** | Stock Images | `L5_media.py` | 100 req/min free |

### Smart Text Analysis Toolkit (P9)
**Location:** `scripts/_L3/utils/api_utils.py` | **Power:** Gemini Flash (~$0.0001/call, negligible)

Internal toolkit for intelligent text processing. Used by carousel presets for highlight extraction, sentiment detection, and content organization.

#### Core Analysis Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `analyze_for_highlights(text, context, max_highlights, max_chars)` | Find key phrases for visual emphasis | `List[str]` exact phrases |
| `analyze_for_buckets(text, bucket_defs, return_sentences)` | Categorize text into themes | `Dict[str, List[str]]` |
| `analyze_for_sentiment(text, context)` | Detect bullish/bearish/neutral | `Dict` with sentiment, confidence, reasoning |
| `extract_entities(text, entity_types)` | Pull out players, teams, stats | `Dict[str, List[str]]` |
| `extract_key_stats(text, stat_types)` | Structured stat extraction | `List[Dict]` with value, type, subject |
| `summarize_to_length(text, max_chars, style)` | Condense text to fit UI | `str` within limit |

**Usage Example - analyze_for_highlights:**
```python
from scripts._L3.utils.api_utils import analyze_for_highlights

highlights = analyze_for_highlights(
    text="Woody Marks could see bell-cow usage with 26 carries expected...",
    context="betting_prop",  # betting_prop | game_preview | player_spotlight | incentive
    max_highlights=3,
    max_chars_per_highlight=20
)
# Returns: ['bell-cow usage', '26 carries']
```

**Context Options:**
- `betting_prop` - Focus on projected stats, matchup advantages, usage indicators
- `game_preview` - Focus on key matchups, injury impacts, coaching tendencies
- `player_spotlight` - Focus on career achievements, season stats, streaks
- `incentive` - Focus on thresholds, current progress, dollar amounts

#### Predefined Bucket Sets

Use `get_bucket_definitions(name)` or `list_available_bucket_sets()`:

```python
BETTING_PROP_BUCKETS = {
    "matchup_edge": "Opponent defensive weakness or scheme advantage",
    "usage_role": "Expected touches, targets, snap count, workload share",
    "game_script": "Game situation that favors this player",
    "stat_support": "Historical stats or trends that support the bet",
    "risk_factors": "Concerns, injury notes, or reasons for caution",
    "key_phrases": "The 2-3 most important short phrases"
}

GAME_PREVIEW_BUCKETS = {
    "matchup_keys": "Critical X-factors and matchup advantages",
    "injury_impact": "Key injuries and how they affect chances",
    "coaching_notes": "Coaching tendencies or strategic considerations",
    "weather_travel": "Environmental or travel factors",
    "historical_context": "Past meetings or relevant trends"
}

PLAYER_ANALYSIS_BUCKETS = {
    "recent_form": "Last few games, hot/cold streaks",
    "season_trajectory": "Overall season improvement or decline",
    "role_situation": "Current role, snap share, target share",
    "matchup_history": "Past performance against this opponent"
}

INCENTIVE_BUCKETS = {
    "threshold_status": "Current progress toward threshold",
    "games_remaining": "Games left and pace needed",
    "motivation_level": "How likely to prioritize hitting incentive",
    "dollar_amount": "Monetary value at stake"
}
```

#### LLM-Powered Extraction (P9 Refactor)

Replace complex regex with intelligent LLM analysis:

| Function | Purpose | Replaces |
|----------|---------|----------|
| `extract_betting_thesis_llm()` | Identify pass/run/situational thesis | Regex pattern matching |
| `extract_cover_insight_llm()` | Generate 45-char carousel bullets | Brittle text slicing |
| `determine_predicted_winner_llm()` | Handle contrarian bets correctly | Simple string matching |

**extract_betting_thesis_llm:**
```python
thesis = extract_betting_thesis_llm(
    reasoning="The Ravens run game has been dominant...",
    teams={'winner': 'Ravens', 'loser': 'Texans'}
)
# Returns: {'type': 'run_based', 'angle': 'run_d_vulnerable', 'confidence': 0.95}
```

**Thesis Types:** `pass_based`, `run_based`, `situational`

**extract_cover_insight_llm:**
```python
# Follows narrative flow: setup → conflict → resolution
setup = extract_cover_insight_llm(reasoning, 'setup', teams, thesis)
# Returns: "BAL 10-5, playoff seeding at stake"

conflict = extract_cover_insight_llm(reasoning, 'conflict', teams, thesis)
# Returns: "HOU run D #26: 142.3 YPG allowed"

resolution = extract_cover_insight_llm(reasoning, 'resolution', teams, thesis)
# Returns: "BAL covers comfortably"
```

**L0 Toggle:** Tool Configuration → `[e] Toggle LLM Extraction`
- Default: **ON** (~$0.0003/matchup)
- Smart wrappers (`smart_extract_*()`) auto-route based on toggle

### Tier 2: Free Tier with API Key
Require signup but offer generous free tiers.

| Tool | Category | Free Tier | Integration Point |
|------|----------|-----------|-------------------|
| **Google Cloud TTS** | Voice | 1M chars/month | L4 audio_sync |
| **Amazon Polly** | Voice | 5M chars/12mo | L4 audio_sync |
| **Azure TTS** | Voice | 500K chars/month | L4 audio_sync |
| **OpenAI Whisper API** | Transcription | $5 free credits | L4 audio_sync |
| **Gemini Free** | LLM | Rate limited | L3 idea_creation |

### Tier 3: Local/GPU-Required (Zero Per-Use Cost)
Require local GPU but have no per-generation cost.

| Tool | Category | Requirements | Best For |
|------|----------|--------------|----------|
| **Coqui TTS** | Voice | CPU/GPU | Local voice generation |
| **Piper TTS** | Voice | CPU | Fast local TTS |
| **Whisper (local)** | Transcription | 4GB+ VRAM | Offline transcription |
| **Real-ESRGAN** | Upscaling | 4GB+ VRAM | Image/video enhancement |
| **HunyuanVideo 1.5** | Video Gen | 14GB+ VRAM | High-volume video |
| **Stable Diffusion** | Image Gen | 8GB+ VRAM | Custom image generation |

### Implementation Priority
Based on cost reduction potential and pipeline integration:

**Phase 1 (Immediate - No Dependencies)**:
- `add_watermark()` - Brand protection
- `create_gradient_background()` - Reduces API calls
- `create_text_card()` - Quote cards without API
- `trim_video()` - Essential utility
- `concatenate_videos()` - Multi-segment assembly
- `add_subtitles_burn()` - Caption burn-in

**Phase 2 (Medium - Core Enhancements)**:
- `parallax_effect()` - 2.5D depth for static images
- `split_screen()` - Matchup comparisons
- `create_collage()` - Multi-player layouts
- `apply_color_filter()` - Brand consistency

**Phase 3 (Advanced - Optional Dependencies)**:
- Coqui/Piper local TTS integration
- Local Whisper transcription
- Real-ESRGAN upscaling

---

## Version History
- **v4.3 (Jan 18, 2026)**: Added local animation tools section - ComfyUI installation, AnimateDiff (image-to-video), RIFE (frame interpolation). Updated for pipeline integration at `~/ComfyUI`.
- **v4.2 (Dec 26, 2025)**: Added Smart Text Analysis Toolkit (P9) - internal LLM-powered text processing functions for highlight extraction, sentiment detection, bucket categorization, and LLM extraction toggle.
- **v4.1 (Dec 20, 2025)**: Added Free Tools Integration section (Tier 1-3 tools), implementation priority phases.
- **v4.0 (Dec 17, 2025)**: Major update - Runway Gen-4.5 (#1 Video Arena), Kling 2.6 (native audio), Kling O1, HunyuanVideo 1.5 (open source), ByteDance Vidi2, Runway GWM-1 world model. Updated all pricing, added research priorities, Goated Bets pipeline recommendations.
- **v3.0 (Dec 8, 2025)**: Added unified platforms (Google AI Studio, fal.ai, Replicate, PiAPI), speech-to-text/transcription, music generation (Suno, Udio, Lyria), Sora 2 video, ComfyUI workflows, GPU rental analysis
- **v2.0 (Dec 4, 2025)**: Added quality rankings, Nano Banana Pro, image animation comparison, Veo 3.1, Kling 2.0/2.1, TTS quality benchmarks
- **v1.0 (Dec 2025)**: Initial comprehensive reference
- Pricing accurate as of December 26, 2025
- Verify current pricing on official sites before production use
