import os

os.makedirs('avatars', exist_ok=True)

# CARTOON/ANIME STYLE AVATAR PROMPTS - Women with fox ears
foxes = {
    "mara": "Cartoon anime style avatar illustration of a beautiful 28-year-old Latina woman with orange fox ears, auburn wavy hair, warm smile, orange polo shirt, phone headset, professional digital art style, clean white background",
    
    "rhea": "Cartoon anime style avatar illustration of a beautiful 31-year-old Greek-American woman with pink fox ears, honey blonde updo, elegant smile, pearl earrings, pink polo, professional digital art style, clean white background",
    
    "vera": "Cartoon anime style avatar illustration of a beautiful 26-year-old Vietnamese-American woman with emerald green fox ears, jet black straight hair, confident expression, green polo, professional digital art style, clean white background",
    
    "dara": "Cartoon anime style avatar illustration of a beautiful 34-year-old Nigerian-American woman with royal blue fox ears, dark curly hair, thoughtful expression, blue polo, professional digital art style, clean white background",
    
    "lara": "Cartoon anime style avatar illustration of a beautiful 38-year-old Italian-American woman with red-orange fox ears, brown ponytail, capable expression, white chef coat, professional digital art style, clean white background",
    
    "tira": "Cartoon anime style avatar illustration of a beautiful 22-year-old Korean-American woman with black and pink gradient fox ears, black hair with pink highlights, playful expression, black fitted tee, professional digital art style, clean white background",
    
    "tora": "Cartoon anime style avatar illustration of a beautiful 24-year-old Japanese-Brazilian woman with black and cyan fox ears, black hair with blue tips, artistic creative expression, black hoodie, professional digital art style, clean white background",
    
    "sara": "Cartoon anime style avatar illustration of a beautiful 23-year-old Swedish-American woman with bright yellow fox ears, platinum blonde wavy hair, casual smile, yellow polo, professional digital art style, clean white background",
    
    "kara": "Cartoon anime style avatar illustration of a beautiful 25-year-old Irish-American woman with golden yellow fox ears, caramel curly hair, bubbly smile, golden polo, professional digital art style, clean white background",
    
    "ira": "Cartoon anime style avatar illustration of a beautiful 27-year-old Persian-American woman with purple and magenta gradient fox ears, dark wavy voluminous hair, elegant expression, gold hoop earrings, purple polo, professional digital art style, clean white background",
    
    "gara": "Cartoon anime style avatar illustration of a beautiful 26-year-old Puerto Rican woman with pink and orange gradient fox ears, brown to blonde ombre hair, warm friendly smile, pink polo, professional digital art style, clean white background",
    
    "farah": "Cartoon anime style avatar illustration of a beautiful 32-year-old Egyptian-American woman with navy blue fox ears, dark hair in neat bun, professional warm expression, navy polo, professional digital art style, clean white background",
    
    "bara": "Cartoon anime style avatar illustration of a beautiful 29-year-old Indian-American woman with red fox ears, long black sleek hair, thoughtful presenter expression, red polo, professional digital art style, clean white background"
}

with open('fox_avatar_prompts.txt', 'w') as f:
    f.write("🦊 FIFOX CARTOON AVATAR PROMPTS\n")
    f.write("=" * 50 + "\n\n")
    for name, prompt in foxes.items():
        f.write(f"{name.upper()}\n{prompt}\n\n")

print("✅ Cartoon avatar prompts saved!")
print("📝 Use these in DALL-E, Midjourney, or Leonardo.ai")
print(f"📊 {len(foxes)} avatars to generate")
