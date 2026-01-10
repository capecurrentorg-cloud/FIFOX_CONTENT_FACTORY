#!/usr/bin/env python3
"""
FIFOX Avatar Setup Script
Validates avatar presence, generates HTML gallery, and provides setup instructions
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Supported image formats
SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.webp']

# Agent configuration
AGENTS = [
    {"name": "Mara", "file": "mara.png", "role": "Phone Orders & Reservations"},
    {"name": "Rhea", "file": "rhea.png", "role": "Reservations & Customer Appreciation"},
    {"name": "Vera", "file": "vera.png", "role": "Quality Control & Verification"},
    {"name": "Dara", "file": "dara.png", "role": "Content Strategy Director"},
    {"name": "Lara", "file": "lara.png", "role": "Kitchen Operations & Inventory"},
    {"name": "Tira", "file": "tira.png", "role": "TikTok Content Creator"},
    {"name": "Tora", "file": "tora.png", "role": "Twitter/X Content Creator"},
    {"name": "Sara", "file": "sara.png", "role": "Snapchat Content Creator"},
    {"name": "Kara", "file": "kara.png", "role": "Facebook Content Creator"},
    {"name": "IaRA", "file": "iara.png", "role": "Instagram Content Creator"},
    {"name": "Gara", "file": "gara.png", "role": "Pinterest & LinkedIn Content Creator"},
    {"name": "Fara", "file": "fara.png", "role": "Copywriter"},
    {"name": "Bara", "file": "bara.png", "role": "YouTube Content Creator"}
]


def validate_avatars():
    """Validate that all 13 avatars are present"""
    print("🦊 FIFOX Avatar Validation")
    print("=" * 60)
    
    avatars_dir = Path("avatars")
    
    if not avatars_dir.exists():
        print("❌ Error: 'avatars/' directory not found!")
        print("   Creating directory now...")
        avatars_dir.mkdir(exist_ok=True)
        return False
    
    all_present = True
    missing_avatars = []
    found_avatars = []
    
    for agent in AGENTS:
        avatar_found = False
        
        # Check for avatar with any supported format
        for ext in SUPPORTED_FORMATS:
            base_name = Path(agent["file"]).stem
            avatar_path = avatars_dir / f"{base_name}{ext}"
            
            if avatar_path.exists():
                avatar_found = True
                found_avatars.append({
                    "name": agent["name"],
                    "file": avatar_path.name,
                    "path": str(avatar_path),
                    "role": agent["role"]
                })
                print(f"✓ {agent['name']:8} - {avatar_path.name:15} ({agent['role']})")
                break
        
        if not avatar_found:
            all_present = False
            missing_avatars.append(agent)
            print(f"✗ {agent['name']:8} - Missing          ({agent['role']})")
    
    print("=" * 60)
    
    if all_present:
        print(f"✅ All 13 avatars are present!")
    else:
        print(f"⚠️  {len(missing_avatars)} avatar(s) missing:")
        for agent in missing_avatars:
            print(f"   - {agent['file']} ({agent['name']})")
        print(f"\n💡 See avatars/README.md for instructions on generating avatars")
    
    return all_present, found_avatars, missing_avatars


def load_agent_config():
    """Load agent configuration from agent_avatars.json"""
    try:
        with open('agent_avatars.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  agent_avatars.json not found")
        return None


def generate_html_gallery(found_avatars):
    """Generate HTML gallery page showing all fox agents"""
    
    config = load_agent_config()
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFOX Team Gallery - All 13 Agents</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .agent-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .agent-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .avatar-container {
            width: 200px;
            height: 200px;
            margin: 0 auto 20px;
            border-radius: 50%;
            overflow: hidden;
            border: 5px solid #f0f0f0;
        }
        
        .avatar-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .agent-name {
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .agent-role {
            font-size: 1em;
            color: #666;
            margin-bottom: 15px;
            min-height: 40px;
        }
        
        .agent-color {
            display: inline-block;
            padding: 5px 15px;
            background: #f0f0f0;
            border-radius: 20px;
            font-size: 0.9em;
            color: #555;
            margin-top: 10px;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 50px;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
        }
        
        .footer h2 {
            margin-bottom: 15px;
        }
        
        .footer p {
            margin: 10px 0;
            opacity: 0.9;
        }
        
        .missing-section {
            background: rgba(255, 100, 100, 0.2);
            border: 2px solid rgba(255, 100, 100, 0.5);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            color: white;
        }
        
        .missing-section h3 {
            margin-bottom: 15px;
        }
        
        .missing-list {
            list-style: none;
            padding-left: 20px;
        }
        
        .missing-list li {
            margin: 8px 0;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦊 FIFOX Team Gallery</h1>
            <p>Meet the 13 AI Agents Powering Your Restaurant</p>
        </div>
        
        <div class="gallery">
"""
    
    # Add agent cards for found avatars
    for agent in found_avatars:
        # Find color info from config
        color_info = "Brand Color"
        if config:
            for agent_config in config.get('agents', []):
                if agent_config['name'] == agent['name']:
                    color_info = f"🦊 {agent_config['ear_color']}"
                    break
        
        html += f"""
            <div class="agent-card">
                <div class="avatar-container">
                    <img src="{agent['path']}" alt="{agent['name']}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22%3E%3Crect fill=%22%23ddd%22 width=%22200%22 height=%22200%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-size=%2220%22 fill=%22%23999%22%3ENo Image%3C/text%3E%3C/svg%3E'">
                </div>
                <div class="agent-name">{agent['name']}</div>
                <div class="agent-role">{agent['role']}</div>
                <div class="agent-color">{color_info}</div>
            </div>
"""
    
    html += """
        </div>
"""
    
    # Add missing avatars section if any
    all_agent_names = [a['name'] for a in AGENTS]
    found_names = [a['name'] for a in found_avatars]
    missing_names = [name for name in all_agent_names if name not in found_names]
    
    if missing_names:
        html += """
        <div class="missing-section">
            <h3>⚠️ Missing Avatars</h3>
            <p>The following agents don't have avatars yet:</p>
            <ul class="missing-list">
"""
        for name in missing_names:
            agent_info = next((a for a in AGENTS if a['name'] == name), None)
            if agent_info:
                html += f"                <li>• {name} - {agent_info['role']}</li>\n"
        
        html += """
            </ul>
            <p style="margin-top: 20px;">📸 See <code>avatars/README.md</code> for instructions on generating avatars.</p>
        </div>
"""
    
    html += f"""
        <div class="footer">
            <h2>🎨 Avatar Setup Instructions</h2>
            <p>To add or update avatars:</p>
            <p>1. Generate avatars using the prompt in <code>README.md</code></p>
            <p>2. Place images in the <code>avatars/</code> directory</p>
            <p>3. Run <code>python setup_avatars.py</code> to regenerate this gallery</p>
            <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.7;">
                Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    with open('fox_gallery.html', 'w') as f:
        f.write(html)
    
    print(f"\n✅ HTML gallery generated: fox_gallery.html")
    print(f"   Open in browser to view all {len(found_avatars)} fox agents")


def display_instructions():
    """Display setup instructions"""
    print("\n" + "=" * 60)
    print("📖 AVATAR SETUP INSTRUCTIONS")
    print("=" * 60)
    print("""
To generate avatars for missing agents:

1. OPTION A - Generate with AI Tools:
   • Open the main README.md
   • Find the "SINGLE PROMPT FOR ALL 13 FOXES" section
   • Copy the complete prompt
   • Use with: Gemini, Midjourney, Leonardo.ai, or DALL-E
   • Save generated images as PNG files

2. OPTION B - Use Existing Images:
   • Rename images to match: {agent-name}.png
   • Ensure format is PNG, JPG, JPEG, or WEBP
   • Place in avatars/ directory

3. Validate Setup:
   • Run: python setup_avatars.py
   • Check fox_gallery.html in browser
   • Verify all 13 agents appear correctly

4. Integration:
   • Avatars automatically link to Command Center
   • Use in social media posts
   • Include in marketing materials

For detailed instructions, see: avatars/README.md
""")


def main():
    """Main setup function"""
    print("\n")
    
    # Validate avatars
    all_present, found_avatars, missing_avatars = validate_avatars()
    
    # Generate HTML gallery
    if found_avatars:
        generate_html_gallery(found_avatars)
    
    # Display instructions
    display_instructions()
    
    # Summary
    print("=" * 60)
    if all_present:
        print("🎉 Setup Complete! All 13 FIFOX agents have avatars!")
        print(f"   View the gallery: fox_gallery.html")
    else:
        print(f"⚠️  Setup Incomplete: {len(missing_avatars)} avatar(s) still needed")
        print(f"   Follow instructions above to complete setup")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
