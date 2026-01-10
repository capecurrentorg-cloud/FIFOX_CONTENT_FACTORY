#!/usr/bin/env python3
"""
Fix all video ads with working placeholder images
"""

import os
from pathlib import Path

# Menu items with reliable placeholder images
MENU_ITEMS = [
    ("SIGNATURE BURGER", "Our 8oz grass-fed beef burger with aged cheddar and crispy bacon.", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800"),
    ("GRILLED SALMON", "Wild-caught Atlantic salmon with lemon butter and herbs.", "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=800"),
    ("CAESAR SALAD", "Fresh romaine with parmesan, croutons, and house-made dressing.", "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=800"),
    ("RIBEYE STEAK", "12oz prime ribeye grilled to perfection with garlic butter.", "https://images.unsplash.com/photo-1558030006-450675393462?w=800"),
    ("CHICKEN PASTA", "Grilled chicken with sun-dried tomatoes in creamy alfredo sauce.", "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800"),
    ("SEAFOOD PLATTER", "Fresh shrimp, scallops, and calamari with cocktail sauce.", "https://images.unsplash.com/photo-1559737558-2f8b6e6c4f7e?w=800"),
    ("MUSHROOM RISOTTO", "Creamy arborio rice with wild mushrooms and truffle oil.", "https://images.unsplash.com/photo-1476124369491-c4d6d4e1eb88?w=800"),
    ("FISH TACOS", "Crispy cod with cabbage slaw and chipotle mayo.", "https://images.unsplash.com/photo-1599974789162-f1c9c60e62e0?w=800"),
    ("BBQ RIBS", "Slow-cooked baby back ribs with our secret BBQ sauce.", "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"),
    ("LOBSTER ROLL", "Fresh lobster meat on a toasted butter roll.", "https://images.unsplash.com/photo-1534939268851-c2cd58d0b04b?w=800"),
    ("CAPRESE SALAD", "Fresh mozzarella, tomatoes, and basil with balsamic glaze.", "https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=800"),
    ("PORK CHOPS", "Pan-seared pork chops with apple compote.", "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=800"),
    ("SHRIMP SCAMPI", "Jumbo shrimp in white wine garlic butter sauce.", "https://images.unsplash.com/photo-1563458838198-59e0cd6555e9?w=800"),
    ("VEGGIE BURGER", "House-made black bean patty with avocado and sprouts.", "https://images.unsplash.com/photo-1520072959219-c595dc870360?w=800"),
    ("CRAB CAKES", "Maryland-style crab cakes with remoulade sauce.", "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=800"),
    ("STEAK FAJITAS", "Sizzling beef with peppers and onions.", "https://images.unsplash.com/photo-1599974579630-ec1c57b7be27?w=800"),
    ("GREEK SALAD", "Cucumber, tomato, olives, and feta with oregano vinaigrette.", "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800"),
    ("CHICKEN WINGS", "Crispy wings tossed in buffalo or BBQ sauce.", "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=800"),
    ("FILET MIGNON", "8oz tender beef filet with red wine reduction.", "https://images.unsplash.com/photo-1546833998-877b37c2e5c6?w=800"),
    ("TUNA POKE BOWL", "Fresh ahi tuna with rice, avocado, and sesame.", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"),
    ("MAC & CHEESE", "Creamy three-cheese blend with breadcrumb topping.", "https://images.unsplash.com/photo-1543352634-a1c51d9f1fa7?w=800"),
    ("LAMB CHOPS", "Herb-crusted lamb with mint chimichurri.", "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=800"),
    ("VEGETABLE STIR-FRY", "Seasonal vegetables in ginger soy sauce.", "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=800"),
    ("PULLED PORK SANDWICH", "Slow-smoked pulled pork with coleslaw.", "https://images.unsplash.com/photo-1628238289717-4db0e00be3e0?w=800"),
    ("SUSHI ROLLS", "Chef's selection of fresh nigiri and maki rolls.", "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800"),
    ("CHICKEN TENDERS", "Crispy hand-breaded tenders with honey mustard.", "https://images.unsplash.com/photo-1562967914-608f82629710?w=800"),
    ("SALMON SALAD", "Grilled salmon over mixed greens with citrus vinaigrette.", "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=800"),
    ("PRIME RIB", "Slow-roasted prime rib with au jus and horseradish.", "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"),
    ("VEGETABLE LASAGNA", "Layered pasta with roasted vegetables and ricotta.", "https://images.unsplash.com/photo-1621510456681-2330135e5871?w=800"),
    ("COCONUT SHRIMP", "Crispy coconut-breaded shrimp with pineapple sauce.", "https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?w=800")
]

def generate_html(number, title, description, image_url):
    """Generate HTML with working images"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Foxes - Video {number}</title>
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
        <img src="{image_url}" alt="{title}" class="food-image" onerror="this.style.display='none'" />
        <div class="text-content">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    </div>
    <div class="watermark">FIFOX PRODUCTION #{number}</div>
</body>
</html>
"""
    return html

def main():
    """Fix all video ads"""
    print("🦊 Fixing FIFOX Video Ads with Working Images")
    print("=" * 60)
    
    output_dir = "Foxes"
    
    for i, (title, description, image_url) in enumerate(MENU_ITEMS, 1):
        html_content = generate_html(i, title, description, image_url)
        html_file = os.path.join(output_dir, f"video_{i}.html")
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"✓ Fixed video_{i}.html - {title}")
    
    print("=" * 60)
    print(f"✓ All {len(MENU_ITEMS)} videos fixed with working images!")

if __name__ == "__main__":
    main()
