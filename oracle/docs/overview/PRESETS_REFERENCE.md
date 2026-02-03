# Presets Reference

> Auto-generated: 2026-01-07 22:32
> Run `python3 oracle/maintenance/project_oracle.py presets --save` to update

---

## Generate Presets

| Preset | Description | Output | L1 (Data) | L3 (Script) | L4 (Audio) | L5 (Media) | L6 (Assembly) |
|--------|-------------|--------|-----------|-------------|------------|------------|---------------|
| **best_bets_game** | Generate 5 best betting picks for a spec... | betting_picks | - | gemini | None | None | None |
| **best_bets_slate** | Generate top picks across all games for ... | betting_picks | - | perplexity | None | None | None |
| **matchup_card_video** | Text-overlay video with TTS for a single... | matchup_card | - | perplexity | None | pexels | ken_burns |
| **best_bets_matchup_infographic** | AI-generated infographic with one best b... | infographic | goatedbets_matchup_analysis | nano_banana | None | nano_banana | ken_burns |
| **best_bets_single_image** | Single focused infographic - one best be... | infographic | goatedbets_matchup_analysis | nano_banana | None | nano_banana | None |
| **matchup_analysis_infographic** | Detailed matchup breakdown with team edg... | infographic | goatedbets_matchup_analysis | nano_banana | None | nano_banana | None |
| **carousel_illustrated** | 3-slide carousel with 9:16 static videos... | carousel | goatedbets_api | carousel_script | None | nano_banana | carousel_assembly |
| **illustrated_insights_carousel** | 6-slide value carousel with 9:16 static ... | carousel | goatedbets_api | carousel_script | None | nano_banana | carousel_assembly |
| **dark_incentives** | Single-page player contract incentive gr... | single_image | manual_input | incentives_script | None | nano_banana | reel_converter |
| **best_bets_dark** | Dark gradient best bet infographic with ... | infographic | goatedbets_api | infographic_script | None | nano_banana | pil_overlay |
| **carousel_dark** | Dark-themed 3-slide carousel with neon a... | carousel | goatedbets_matchup_analysis | nano_banana | None | nano_banana | None |
| **ai_image_matchup** | Photorealistic/artistic image for matchu... | ai_image | goatedbets_matchup_analysis | imagen4 | None | imagen4 | None |
| **ai_image_player** | Artistic player-focused image - text ove... | ai_image | goatedbets_matchup_analysis | imagen4 | None | imagen4 | None |
| **meme_mashup** | Viral meme format: 2+ clips with transit... | meme_video | local_assets | None | elevenlabs | None | kling |
| **meme_overlay** | Single clip with text and/or logo overla... | meme_video | local_assets | None | None | None | None |
| **carousel_illustrated_pil** | Watercolor/sketch illustrations with PIL... | carousel | goatedbets_matchup_analysis | imagen4 | None | imagen4 | None |
| **short_form_video** | PLACEHOLDER - Short-form video under 60 ... | video | web_search | video_script | elevenlabs | pexels | ken_burns |
| **long_form_video** | PLACEHOLDER - Long-form video over 60 se... | video | web_search | video_script | elevenlabs | pexels | ken_burns |

## Discovery Presets

| Preset | Description | Mode |
|--------|-------------|------|
| **nfl_betting_trends** |  | discovery |
| **nfl_bad_beats** |  | discovery |

---

## Tool Reference

### L1 Data Sources
- `goatedbets_api` - GoatedBets matchup analysis API
- `web_search` - Perplexity/Tavily web search
- `local_assets` - Local video/image assets
- `balldontlie` - Sports data via balldontlie API (NFL/NBA)

### L3 Script Tools (LLM)
- `gemini` - Google Gemini 1.5 Flash
- `perplexity` - Perplexity Sonar (real-time web)
- `gpt-4o-mini` - OpenAI GPT-4o Mini
- `nano_banana` - Gemini for text-heavy infographics
- `carousel_script` - Carousel slide generation
- `infographic_script` - Infographic content generation

### L4 Audio Tools
- `elevenlabs` - ElevenLabs TTS

### L5 Media Tools
- `nano_banana` - Gemini Nano Banana (text-heavy images)
- `imagen4` - Google Imagen 4 (photorealistic)
- `flux_fal` - Flux via FAL.AI
- `pexels` - Pexels stock video/images
- `kling` - Kling AI video generation

### L6 Assembly Tools
- `carousel_assembly` - Multi-slide carousel assembly
- `reel_converter` - 9:16 static video conversion
- `pil_overlay` - PIL logo/text overlay
- `ken_burns` - Ken Burns effect animation
- `ffmpeg` - FFmpeg video processing
