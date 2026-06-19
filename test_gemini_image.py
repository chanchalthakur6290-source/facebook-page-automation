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

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found")
    exit(1)

# ==========================
# GEMINI CLIENT
# ==========================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# ==========================
# FOLDERS & FILES
# ==========================

IMAGE_FOLDER = "image"
POSTED_FILE = "posted_images.txt"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

if not os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "w", encoding="utf-8"):
        pass

# ==========================
# LOAD ALL IMAGES
# ==========================

all_images = [
    file for file in os.listdir(IMAGE_FOLDER)
    if file.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
]

if not all_images:
    print("❌ No images found in image folder")
    exit(1)

# ==========================
# LOAD POST HISTORY
# ==========================

with open(
    POSTED_FILE,
    "r",
    encoding="utf-8"
) as file:

    posted_images = [
        line.strip()
        for line in file.readlines()
        if line.strip()
    ]

# ==========================
# AVAILABLE IMAGES
# ==========================

available_images = [
    img
    for img in all_images
    if img not in posted_images
]

if not available_images:
    print("❌ Sab images post ho chuki hain.")
    exit(1)

# ==========================
# RANDOM IMAGE
# ==========================

random_image = random.choice(
    available_images
)

image_path = os.path.join(
    IMAGE_FOLDER,
    random_image
)

print(f"📸 Selected Image: {random_image}")

# ==========================
# SAVE IMAGE PATH
# ==========================

with open(
    "selected_image.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(image_path)

# ==========================
# LOAD IMAGE
# ==========================

try:
    image = Image.open(image_path)

except Exception as e:

    print(f"❌ Image Error: {e}")
    exit(1)

# ==========================
# PROMPT
# ==========================

prompt = """
Is image ko analyse karo.

Facebook page post ke liye Hindi me likho:

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
# GENERATE CONTENT
# ==========================

try:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    result = response.text

except Exception as e:

    print(f"❌ Gemini Error: {e}")
    exit(1)

# ==========================
# SAVE POST
# ==========================

with open(
    "post.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(result)

print("✅ post.txt created")

# ==========================
# SAVE HISTORY
# ==========================

with open(
    POSTED_FILE,
    "a",
    encoding="utf-8"
) as file:

    file.write(
        random_image + "\n"
    )

print(
    f"✅ Added To History: {random_image}"
)

print(
    "✅ selected_image.txt created"
)

print(
    "\n🎉 Post Generated Successfully"
)