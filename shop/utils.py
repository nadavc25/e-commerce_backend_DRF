# shop\utils.py
def generate_firebase_storage_url(image_name):
    print(f"generate_firebase_storage_url")
    base_url = "https://firebasestorage.googleapis.com/v0/b/sport-jersey-e-commerce.appspot.com/o/"
    end_url = "?alt=media"
    url = f"{base_url}{image_name}{end_url}"
    print("gen", url)
    # Correct the URL format
    corrected_url = url.replace("/o/http://", "/o/")

    print(corrected_url)
    print(f"generate_firebase_storage_url")
    return corrected_url
