# FIFOX Agent Avatars

This directory contains avatar profile pictures for all 13 FIFOX agents.

## 🦊 Avatar Naming Convention

Each avatar should be named using the following format:
```
{agent-name}.png
```

### All Agent Avatars

1. **mara.png** - Mara (Phone Orders & Reservations)
2. **rhea.png** - Rhea (Reservations & Customer Appreciation)
3. **vera.png** - Vera (Quality Control & Verification)
4. **dara.png** - Dara (Content Strategy Director)
5. **lara.png** - Lara (Kitchen Operations & Inventory)
6. **tira.png** - Tira (TikTok Content Creator)
7. **tora.png** - Tora (Twitter/X Content Creator)
8. **sara.png** - Sara (Snapchat Content Creator)
9. **kara.png** - Kara (Facebook Content Creator)
10. **iara.png** - IaRA (Instagram Content Creator)
11. **gara.png** - Gara (Pinterest & LinkedIn Content Creator)
12. **fara.png** - Fara (Copywriter)
13. **bara.png** - Bara (YouTube Content Creator)

## 📸 How to Generate Avatars

### Option 1: Use AI Image Generation Tools

Use the complete avatar generation prompt from the main README.md with any of these tools:

- **Google Gemini** (recommended for batch generation)
- **Midjourney** (high quality, subscription required)
- **Leonardo.ai** (good free tier)
- **DALL-E 3** via ChatGPT Plus

Copy the "SINGLE PROMPT FOR ALL 13 FOXES" from the main README.md and generate all 13 avatars at once.

### Option 2: Manual Placement

If you already have avatar images:

1. Rename your images according to the naming convention above
2. Ensure all images are in PNG format (or JPG/JPEG/WEBP - see supported formats)
3. Place them directly in this `avatars/` directory
4. Run `python setup_avatars.py` to validate

## 🎨 Avatar Requirements

### Image Specifications
- **Format**: PNG preferred (JPG, JPEG, WEBP also supported)
- **Dimensions**: Minimum 512x512px, recommended 1024x1024px
- **Background**: Clean white or transparent
- **Style**: Professional headshot, photorealistic
- **Lighting**: Soft studio lighting

### Character Features
Each avatar must match the character descriptions in the main README.md:
- **Correct fox ear colors** (matches agent's brand color)
- **Accurate ethnic features and hair styles**
- **Appropriate age representation**
- **Professional restaurant uniform** (polo shirts or chef coat)

## ⚙️ Setup Process

After placing all avatar images in this directory:

1. Run the setup script:
   ```bash
   python setup_avatars.py
   ```

2. The script will:
   - Validate all 13 avatars are present
   - Check image formats and dimensions
   - Generate an HTML gallery page (`fox_gallery.html`)
   - Update configuration files

3. View the gallery:
   - Open `fox_gallery.html` in your browser
   - Verify all avatars display correctly

## 🔍 Troubleshooting

### Missing Avatars
If the validation script reports missing avatars, ensure:
- File names exactly match the convention (lowercase, .png extension)
- Files are in the `avatars/` directory, not a subdirectory
- No typos in file names (e.g., "iara.png" not "Iara.png")

### Image Format Issues
If images don't load properly:
- Convert to PNG format for best compatibility
- Ensure files aren't corrupted
- Check file permissions (should be readable)

### Quality Issues
If avatars don't match character descriptions:
- Re-generate using the exact prompt from README.md
- Verify fox ear colors match agent brand colors
- Ensure ethnic features and hair match descriptions

## 📋 Quick Reference

| Agent | File Name | Ear Color | Role |
|-------|-----------|-----------|------|
| Mara | mara.png | Orange | Phone Orders |
| Rhea | rhea.png | Pink | Reservations |
| Vera | vera.png | Emerald Green | Quality Control |
| Dara | dara.png | Royal Blue | Content Strategy |
| Lara | lara.png | Red-Orange | Kitchen Ops |
| Tira | tira.png | Black & Pink | TikTok |
| Tora | tora.png | Black & Cyan | Twitter/X |
| Sara | sara.png | Bright Yellow | Snapchat |
| Kara | kara.png | Golden Yellow | Facebook |
| IaRA | iara.png | Purple & Magenta | Instagram |
| Gara | gara.png | Pink & Orange | Pinterest/LinkedIn |
| Fara | fara.png | Navy Blue | Copywriter |
| Bara | bara.png | Red | YouTube |

## 🎯 Next Steps

Once all avatars are in place:
1. Run `python setup_avatars.py` to validate
2. Check the generated `fox_gallery.html` 
3. Avatars will automatically appear in the Command Center
4. Use in social media posts and marketing materials

---

**Need Help?** See the main README.md for the complete avatar generation prompt and additional guidance.
