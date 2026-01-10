#!/usr/bin/env python3
"""
Generate images for FIFOX restaurant menu items
Supports multiple image generation methods
"""

import os
import json
import requests
from pathlib import Path

# Menu items matching the scripts
MENU_ITEMS = [
    ("SIGNATURE BURGER", "8oz grass-fed beef burger with aged cheddar and crispy bacon"),
    ("GRILLED SALMON", "Wild-caught Atlantic salmon with lemon butter and herbs"),
    ("CAESAR SALAD", "Fresh romaine with parmesan, croutons, and house-made dressing"),
    ("RIBEYE STEAK", "12oz prime ribeye grilled to perfection with garlic butter"),
    ("CHICKEN PASTA", "Grilled chicken with sun-dried tomatoes in creamy alfredo sauce"),
    ("SEAFOOD PLATTER", "Fresh shrimp, scallops, and calamari with cocktail sauce"),
    ("MUSHROOM RISOTTO", "Creamy arborio rice with wild mushrooms and truffle oil"),
    ("FISH TACOS", "Crispy cod with cabbage slaw and chipotle mayo"),
    ("BBQ RIBS", "Slow-cooked baby back ribs with our secret BBQ sauce"),
    ("LOBSTER ROLL", "Fresh lobster meat on a toasted butter roll"),
    ("CAPRESE SALAD", "Fresh mozzarella, tomatoes, and basil with balsamic glaze"),
    ("PORK CHOPS", "Pan-seared pork chops with apple compote"),
    ("SHRIMP SCAMPI", "Jumbo shrimp in white wine garlic butter sauce"),
    ("VEGGIE BURGER", "House-made black bean patty with avocado and sprouts"),
    ("CRAB CAKES", "Maryland-style crab cakes with remoulade sauce"),
    ("STEAK FAJITAS", "Sizzling beef with peppers and onions"),
    ("GREEK SALAD", "Cucumber, tomato, olives, and feta with oregano vinaigrette"),
    ("CHICKEN WINGS", "Crispy wings tossed in buffalo or BBQ sauce"),
    ("FILET MIGNON", "8oz tender beef filet with red wine reduction"),
    ("TUNA POKE BOWL", "Fresh ahi tuna with rice, avocado, and sesame"),
    ("MAC & CHEESE", "Creamy three-cheese blend with breadcrumb topping"),
    ("LAMB CHOPS", "Herb-crusted lamb with mint chimichurri"),
    ("VEGETABLE STIR-FRY", "Seasonal vegetables in ginger soy sauce"),
    ("PULLED PORK SANDWICH", "Slow-smoked pulled pork with coleslaw"),
    ("SUSHI ROLLS", "Chef's selection of fresh nigiri and maki rolls"),
    ("CHICKEN TENDERS", "Crispy hand-breaded tenders with honey mustard"),
    ("SALMON SALAD", "Grilled salmon over mixed greens with citrus vinaigrette"),
    ("PRIME RIB", "Slow-roasted prime rib with au jus and horseradish"),
    ("VEGETABLE LASAGNA", "Layered pasta with roasted vegetables and ricotta"),
    ("COCONUT SHRIMP", "Crispy coconut-breaded shrimp with pineapple sauce")
]

def generate_image_prompt(title, description):
    """Create a detailed image generation prompt"""
    return f"Professional food photography of {title.lower()}, {description}, restaurant quality plating, warm lighting, appetizing, high resolution, commercial photography style, isolated on dark background"

def use_placeholder_images():
    """Use Unsplash food images as placeholders"""
    print("🖼️  Generating placeholder image URLs...")
    
    # Food photography keywords for Unsplash
    keywords = {
        "BURGER": "burger", "SALMON": "salmon", "SALAD": "salad", "STEAK": "steak",
        "PASTA": "pasta", "SEAFOOD": "seafood", "RISOTTO": "risotto", "TACOS": "tacos",
        "RIBS": "ribs", "LOBSTER": "lobster", "PORK": "pork", "SHRIMP": "shrimp",
        "WINGS": "wings", "TUNA": "tuna", "CHEESE": "cheese", "LAMB": "lamb",
        "SUSHI": "sushi", "CHICKEN": "chicken"
    }
    
    images_dir = Path("Foxes/images")
    images_dir.mkdir(exist_ok=True)
    
    image_urls = []
    for i, (title, desc) in enumerate(MENU_ITEMS, 1):
        # Find matching keyword
        keyword = "food"
        for key, value in keywords.items():
            if key in title:
                keyword = value
                break
        
        # Generate Unsplash URL
        image_url = f"https://source.unsplash.com/800x600/?{keyword},food,restaurant"
        image_urls.append(image_url)
        
        print(f"  ✓ Image URL for #{i} ({title}): {keyword}")
    
    return image_urls

def generate_html_with_images(image_urls):
    """Update HTML files to include images"""
    print("\n🎨 Updating HTML files with images...")
    
    for i, (title, description) in enumerate(MENU_ITEMS, 1):
        image_url = image_urls[i-1] if i-1 < len(image_urls) else ""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
<title>Foxes - Video {i}</title>
<style>
    body {{ 
        background: #000; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        height: 100vh; 
        margin: 0; 
        color: #fff; 
        font-family: sans-serif; 
        overflow: hidden; 
    }}
    .container {{
        text-align: center;
        position: relative;
        width: 90%;
        max-width: 1200px;
    }}
    .food-image {{
        width: 100%;
        max-width: 800px;
        height: auto;
        border-radius: 20px;
        box-shadow: 0 10px 50px rgba(230, 126, 34, 0.5);
        margin-bottom: 30px;
        animation: fadeZoom 3s ease-in-out infinite alternate;
    }}
    .text-content {{
        animation: slideUp 2s ease-out;
    }}
    h1 {{ 
        font-size: 60px; 
        text-transform: uppercase; 
        color: #e67e22; 
        text-shadow: 0 0 20px #e67e22; 
        margin: 10px 0;
    }}
    p {{ 
        font-size: 24px; 
        margin-top: 15px;
        color: #ecf0f1;
    }}
    .watermark {{ 
        position: absolute; 
        bottom: 20px; 
        right: 20px; 
        opacity: 0.5;
        font-size: 14px;
    }}
    @keyframes fadeZoom {{ 
        from {{ 
            transform: scale(0.98); 
            opacity: 0.9;
        }} 
        to {{ 
            transform: scale(1.02); 
            opacity: 1;
        }} 
    }}
    @keyframes slideUp {{
        from {{
            transform: translateY(30px);
            opacity: 0;
        }}
        to {{
            transform: translateY(0);
            opacity: 1;
        }}
    }}
</style>
</head>
<body>
    <div class="container">
        <img src="{image_url}" alt="{title}" class="food-image" />
        <div class="text-content">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    </div>
    <div class="watermark">FIFOX PRODUCTION #{i}</div>
</body>
</html>
"""
        
        html_file = Path(f"Foxes/video_{i}.html")
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"  ✓ Updated video_{i}.html with image")

def main():
    """Main function"""
    print("🦊 FIFOX Image Generator")
    print("=" * 60)
    
    print("\n📋 Options:")
    print("  1. Use placeholder images from Unsplash (Free, Instant)")
    print("  2. Setup for AI image generation (Requires API key)")
    print("\nUsing Option 1: Placeholder Images\n")
    
    # Generate placeholder images
    image_urls = use_placeholder_images()
    
    # Update HTML files
    generate_html_with_images(image_urls)
    
    print("\n" + "=" * 60)
    print("✓ All videos now include images!")
    print("\n📝 Note: Using Unsplash placeholder images.")
    print("   For custom AI-generated images, you'll need:")
    print("   - OpenAI API key (DALL-E)")
    print("   - Stability AI API key (Stable Diffusion)")
    print("   - Or another image generation service")

if __name__ == "__main__":
    main()
