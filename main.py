import os
import time
import requests

# ==========================
# CHECK INTERNET
# ==========================

def internet_available():
    try:
        requests.get(
            "https://www.google.com",
            timeout=10
        )
        return True
    except:
        return False

# ==========================
# INTERNET WAIT SYSTEM
# ==========================

print("🌐 Checking Internet Connection...")

internet_retry = 12  # 12 x 5 min = 60 min

for i in range(internet_retry):

    if internet_available():

        print("✅ Internet Connected")
        break

    print(
        f"❌ No Internet ({i+1}/{internet_retry})"
    )

    print(
        "⏳ Retrying after 5 minutes..."
    )

    time.sleep(300)

else:

    print(
        "\n❌ Internet not available for 1 hour."
    )

    exit(1)

# ==========================
# STEP 1 - GENERATE POST
# ==========================

MAX_GEMINI_RETRIES = 10

for attempt in range(MAX_GEMINI_RETRIES):

    print(
        f"\n📸 Step 1: Generating Post ({attempt+1}/{MAX_GEMINI_RETRIES})"
    )

    generate_result = os.system(
        "python test_gemini_image.py"
    )

    if generate_result == 0:

        if os.path.exists("post.txt") and os.path.exists("selected_image.txt"):

            print(
                "✅ Post Generated Successfully"
            )

            break

    print(
        "❌ Gemini Generation Failed"
    )

    if attempt < MAX_GEMINI_RETRIES - 1:

        print(
            "⏳ Waiting 60 seconds and retrying..."
        )

        time.sleep(60)

else:

    print(
        "\n❌ All Gemini retries failed"
    )

    exit(1)

# ==========================
# STEP 2 - FACEBOOK UPLOAD
# ==========================

MAX_FB_RETRIES = 5

for attempt in range(MAX_FB_RETRIES):

    print(
        f"\n🚀 Uploading To Facebook ({attempt+1}/{MAX_FB_RETRIES})"
    )

    upload_result = os.system(
        "python fb_post.py"
    )

    if upload_result == 0:

        print(
            "\n🎉 Automation Completed Successfully"
        )

        break

    print(
        "❌ Facebook Upload Failed"
    )

    if attempt < MAX_FB_RETRIES - 1:

        print(
            "⏳ Waiting 60 seconds..."
        )

        time.sleep(60)

else:

    print(
        "\n❌ Facebook upload failed after all retries"
    )

    exit(1)

print("\n✅ Workflow Finished Successfully")
