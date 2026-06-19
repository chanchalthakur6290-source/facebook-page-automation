import os
import random
from dotenv import load_dotenv
from google import genai
from PIL import Image

# ==========================
# LOAD ENV FILE
# ==========================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ==========================
# GEMINI CLIENT
# ==========================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# ==========================
# FOLDERS & FILES
# ==========================

image_folder = "image"
posted_file = "posted_images.txt"

os.makedirs(image_folder, exist_ok=True)

if not os.path.exists(posted_file):
    open(posted_file, "w").close()

# ==========================
# LOAD IMAGES
# ==========================

all_images = [
    file for file in os.listdir(image_folder)
    if file.lower().endswith((".jpg", ".jpeg", ".png"))
]

with open(posted_file, "r", encoding="utf-8") as f:
    posted_images = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ]

available_images = [
    img for img in all_images
    if img not in posted_images
]

if not available_images:
    print("❌ Sab images post ho chuki hain.")
    exit(1)

# ==========================
# RANDOM IMAGE
# ==========================

random_image = random.choice(available_images)

image_path = os.path.join(
    image_folder,
    random_image
)

print(f"📸 Selected Image: {random_image}")

with open(
    "selected_image.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(image_path)

# ==========================
# LOAD IMAGE
# ==========================

image = Image.open(image_path)

# ==========================
# PROMPT
# ==========================

prompt = """
Is image ko analyze karo.

Facebook Page post ke liye Hindi me do:

1. Ek attractive title
2. 2-3 line description
3. Sirf 5 relevant hashtags

Format:

✨ TITLE:
...

📝 DESCRIPTION:
...

🏷 HASHTAGS:
#tag1
#tag2
#tag3
#tag4
#tag5
"""

# ==========================
# GENERATE POST
# ==========================

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt, image]
)

result = response.text

# ==========================
# SAVE POST
# ==========================

with open(
    "post.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(result)

print("\n✅ post.txt created")
print("✅ selected_image.txt created")