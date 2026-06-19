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
# MAIN PROGRAM
# ==========================

print("🌐 Checking Internet Connection...")

retry_count = 12  # 12 x 5 min = 60 min

for i in range(retry_count):

    if internet_available():

        print("✅ Internet Connected")

        # ==========================
        # STEP 1 - GENERATE POST
        # ==========================

        print("\n📸 Step 1: Generating Post...")

        generate_result = os.system(
            "python test_gemini_image.py"
        )

        if generate_result != 0:

            print(
                "\n❌ Post Generation Failed"
            )

            break

        # Check files created

        if not os.path.exists(
            "post.txt"
        ):

            print(
                "\n❌ post.txt not found"
            )

            break

        if not os.path.exists(
            "selected_image.txt"
        ):

            print(
                "\n❌ selected_image.txt not found"
            )

            break

        # ==========================
        # STEP 2 - FACEBOOK UPLOAD
        # ==========================

        print(
            "\n🚀 Step 2: Uploading To Facebook..."
        )

        upload_result = os.system(
            "python fb_post.py"
        )

        if upload_result != 0:

            print(
                "\n❌ Facebook Upload Failed"
            )

            break

        # ==========================
        # SUCCESS
        # ==========================

        print(
            "\n🎉 Automation Completed Successfully"
        )

        break

    else:

        print(
            f"❌ No Internet ({i+1}/{retry_count})"
        )

        print(
            "⏳ Retrying after 5 minutes...\n"
        )

        time.sleep(300)

else:

    print(
        "\n❌ Internet not available for 1 hour."
    )