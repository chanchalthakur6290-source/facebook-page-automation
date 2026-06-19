import os
import requests
from dotenv import load_dotenv

# ==================================
# LOAD ENV VARIABLES
# ==================================

load_dotenv()

PAGE_ID = os.getenv("PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_TOKEN")

# ==================================
# CHECK ENV VARIABLES
# ==================================

if not PAGE_ID:
    print("❌ PAGE_ID not found in .env")
    exit(1)

if not ACCESS_TOKEN:
    print("❌ FACEBOOK_TOKEN not found in .env")
    exit(1)

# ==================================
# READ POST
# ==================================

try:

    with open(
        "post.txt",
        "r",
        encoding="utf-8"
    ) as file:

        caption = file.read().strip()

except Exception as e:

    print(f"❌ post.txt error: {e}")
    exit(1)

# ==================================
# READ IMAGE PATH
# ==================================

try:

    with open(
        "selected_image.txt",
        "r",
        encoding="utf-8"
    ) as file:

        image_path = file.read().strip()

except Exception as e:

    print(f"❌ selected_image.txt error: {e}")
    exit(1)

# ==================================
# CHECK IMAGE EXISTS
# ==================================

if not os.path.exists(image_path):

    print("❌ Image not found")
    print(image_path)
    exit(1)

# ==================================
# FACEBOOK PHOTO UPLOAD
# ==================================

print("\n🚀 Uploading To Facebook...")

url = f"https://graph.facebook.com/{PAGE_ID}/photos"

try:

    with open(image_path, "rb") as image_file:

        files = {
            "source": image_file
        }

        data = {
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }

        response = requests.post(
            url,
            files=files,
            data=data,
            timeout=60
        )

    print("\n📄 Facebook Response:")
    print(response.text)

except Exception as e:

    print(f"\n❌ Upload Error: {e}")
    exit(1)

# ==================================
# SUCCESS
# ==================================

if response.status_code == 200:

    print("\n✅ Facebook Post Successful")

    image_name = os.path.basename(
        image_path
    )

    # ==================================
    # SAVE IMAGE NAME
    # ==================================

    try:

        with open(
            "posted_images.txt",
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                image_name + "\n"
            )

        print(
            f"✅ {image_name} saved in posted_images.txt"
        )

    except Exception as e:

        print(
            f"⚠ Save Failed: {e}"
        )

    # ==================================
    # AUTO COMMENT
    # ==================================

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
                data=comment_data
            )

            print(
                "\n💬 Comment Response:"
            )

            print(
                comment_response.text
            )

    except Exception as e:

        print(
            f"\n⚠ Comment Failed: {e}"
        )

else:

    print("\n❌ Upload Failed")
    exit(1)