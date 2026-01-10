#!/usr/bin/env python3
"""
Generate restaurant-themed scripts and videos for FIFOX Content Factory
"""

import os

# Restaurant menu items with titles and descriptions
MENU_CONTENT = [
    ("SIGNATURE BURGER", "Our 8oz grass-fed beef burger with aged cheddar and crispy bacon."),
    ("GRILLED SALMON", "Wild-caught Atlantic salmon with lemon butter and herbs."),
    ("CAESAR SALAD", "Fresh romaine with parmesan, croutons, and house-made dressing."),
    ("RIBEYE STEAK", "12oz prime ribeye grilled to perfection with garlic butter."),
    ("CHICKEN PASTA", "Grilled chicken with sun-dried tomatoes in creamy alfredo sauce."),
    ("SEAFOOD PLATTER", "Fresh shrimp, scallops, and calamari with cocktail sauce."),
    ("MUSHROOM RISOTTO", "Creamy arborio rice with wild mushrooms and truffle oil."),
    ("FISH TACOS", "Crispy cod with cabbage slaw and chipotle mayo."),
    ("BBQ RIBS", "Slow-cooked baby back ribs with our secret BBQ sauce."),
    ("LOBSTER ROLL", "Fresh lobster meat on a toasted butter roll."),
    ("CAPRESE SALAD", "Fresh mozzarella, tomatoes, and basil with balsamic glaze."),
    ("PORK CHOPS", "Pan-seared pork chops with apple compote."),
    ("SHRIMP SCAMPI", "Jumbo shrimp in white wine garlic butter sauce."),
    ("VEGGIE BURGER", "House-made black bean patty with avocado and sprouts."),
    ("CRAB CAKES", "Maryland-style crab cakes with remoulade sauce."),
    ("STEAK FAJITAS", "Sizzling beef with peppers and onions."),
    ("GREEK SALAD", "Cucumber, tomato, olives, and feta with oregano vinaigrette."),
    ("CHICKEN WINGS", "Crispy wings tossed in buffalo or BBQ sauce."),
    ("FILET MIGNON", "8oz tender beef filet with red wine reduction."),
    ("TUNA POKE BOWL", "Fresh ahi tuna with rice, avocado, and sesame."),
    ("MAC & CHEESE", "Creamy three-cheese blend with breadcrumb topping."),
    ("LAMB CHOPS", "Herb-crusted lamb with mint chimichurri."),
    ("VEGETABLE STIR-FRY", "Seasonal vegetables in ginger soy sauce."),
    ("PULLED PORK SANDWICH", "Slow-smoked pulled pork with coleslaw."),
    ("SUSHI ROLLS", "Chef's selection of fresh nigiri and maki rolls."),
    ("CHICKEN TENDERS", "Crispy hand-breaded tenders with honey mustard."),
    ("SALMON SALAD", "Grilled salmon over mixed greens with citrus vinaigrette."),
    ("PRIME RIB", "Slow-roasted prime rib with au jus and horseradish."),
    ("VEGETABLE LASAGNA", "Layered pasta with roasted vegetables and ricotta."),
    ("COCONUT SHRIMP", "Crispy coconut-breaded shrimp with pineapple sauce.")
]

def generate_script(number, title, description):
    """Generate a script file"""
    content = f"""SCRIPT {number}:
Title: {title}
Body: {description}
[Voiceover Required]
"""
    return content

def generate_html(number, title, description):
    """Generate an HTML video preview file"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Foxes - Video {number}</title>
<style>
    body {{ background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #fff; font-family: sans-serif; overflow: hidden; }}
    .slide {{ text-align: center; animation: zoom 5s infinite alternate; }}
    h1 {{ font-size: 80px; text-transform: uppercase; color: #e67e22; text-shadow: 0 0 20px #e67e22; }}
    p {{ font-size: 30px; margin-top: 20px; }}
    .watermark {{ position: absolute; bottom: 20px; right: 20px; opacity: 0.5; }}
    @keyframes zoom {{ from {{ transform: scale(1); }} to {{ transform: scale(1.1); }} }}
</style>
</head>
<body>
    <div class="slide">
        <h1>{title}</h1>
        <p>{description}</p>
    </div>
    <div class="watermark">FIFOX PRODUCTION #{number}</div>
</body>
</html>
"""
    return html

def main():
    """Generate all scripts and videos"""
    output_dir = "Foxes"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🦊 Generating Restaurant Content for FIFOX")
    print("=" * 60)
    
    for i, (title, description) in enumerate(MENU_CONTENT, 1):
        # Generate script
        script_content = generate_script(i, title, description)
        script_file = os.path.join(output_dir, f"script_{i}.txt")
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Generate HTML
        html_content = generate_html(i, title, description)
        html_file = os.path.join(output_dir, f"video_{i}.html")
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"✓ Generated #{i}: {title}")
    
    print("=" * 60)
    print(f"✓ Successfully generated {len(MENU_CONTENT)} scripts and videos!")
    print(f"📁 Files saved to: {output_dir}/")

if __name__ == "__main__":
    main()
