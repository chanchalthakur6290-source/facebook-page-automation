import os
import requests
from dotenv import load_dotenv

# ==========================
# LOAD ENV VARIABLES
# ==========================

load_dotenv()

PAGE_ID = os.getenv("PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_TOKEN")

# ==========================
# CHECK ENV VARIABLES
# ==========================

if not PAGE_ID:

    print("❌ PAGE_ID not found")
    exit(1)

if not ACCESS_TOKEN:

    print("❌ FACEBOOK_TOKEN not found")
    exit(1)

# ==========================
# READ POST CONTENT
# ==========================

try:

    with open(
        "post.txt",
        "r",
        encoding="utf-8"
    ) as file:

        caption = file.read().strip()

except Exception as e:

    print(
        f"❌ post.txt error: {e}"
    )

    exit(1)

# ==========================
# READ IMAGE PATH
# ==========================

try:

    with open(
        "selected_image.txt",
        "r",
        encoding="utf-8"
    ) as file:

        image_path = file.read().strip()

except Exception as e:

    print(
        f"❌ selected_image.txt error: {e}"
    )

    exit(1)

# ==========================
# CHECK IMAGE EXISTS
# ==========================

if not os.path.exists(image_path):

    print("❌ Image not found")
    print(image_path)

    exit(1)

# ==========================
# FACEBOOK UPLOAD
# ==========================

print("\n🚀 Uploading To Facebook...")

upload_url = (
    f"https://graph.facebook.com/"
    f"{PAGE_ID}/photos"
)

try:

    with open(
        image_path,
        "rb"
    ) as image_file:

        files = {
            "source": image_file
        }

        data = {
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }

        response = requests.post(
            upload_url,
            files=files,
            data=data,
            timeout=60
        )

except Exception as e:

    print(
        f"❌ Upload Error: {e}"
    )

    exit(1)

print("\n📄 Facebook Response:")
print(response.text)

# ==========================
# SUCCESS CHECK
# ==========================

if response.status_code != 200:

    print(
        "\n❌ Facebook Upload Failed"
    )

    exit(1)

print(
    "\n✅ Facebook Post Successful"
)

# ==========================
# SAVE IMAGE HISTORY
# ==========================

try:

    image_name = os.path.basename(
        image_path
    )

    posted_file = "posted_images.txt"

    if not os.path.exists(
        posted_file
    ):

        with open(
            posted_file,
            "w",
            encoding="utf-8"
        ):
            pass

    with open(
        posted_file,
        "r",
        encoding="utf-8"
    ) as file:

        posted_images = [

            line.strip()

            for line in file.readlines()

            if line.strip()
        ]

    if image_name not in posted_images:

        with open(
            posted_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                image_name + "\n"
            )

        print(
            f"✅ Added To History: {image_name}"
        )

    else:

        print(
            f"⚠ Already Exists: {image_name}"
        )

except Exception as e:

    print(
        f"⚠ History Save Failed: {e}"
    )

# ==========================
# AUTO COMMENT
# ==========================

try:

    response_json = response.json()

    if "post_id" in response_json:

        post_id = response_json["post_id"]

        comment_url = (
            f"https://graph.facebook.com/"
            f"{post_id}/comments"
        )

        comment_message = """
🙏 Radhe Radhe 🙏

Aapko ye post kaisi lagi?

Comment me apni rai jarur bataye.

❤️ Jai Shri Krishna ❤️
"""

        comment_data = {

            "message": comment_message,

            "access_token": ACCESS_TOKEN
        }

        comment_response = requests.post(
            comment_url,
            data=comment_data,
            timeout=30
        )

        print(
            "\n💬 Comment Response:"
        )

        print(
            comment_response.text
        )

except Exception as e:

    print(
        f"⚠ Comment Failed: {e}"
    )

print(
    "\n🎉 Facebook Automation Completed Successfully"
)