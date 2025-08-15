# app/routes/stego.py
import os
import shutil
from flask import Blueprint, render_template, request, flash
from werkzeug.utils import secure_filename
from app.stego_tools import folder_to_secure_image

stego_bp = Blueprint("stego", __name__)

UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
ENCRYPTED_IMG_FOLDER = os.path.join(UPLOAD_FOLDER, "encrypted_images")

os.makedirs(ENCRYPTED_IMG_FOLDER, exist_ok=True)


@stego_bp.route("/stego/", methods=["GET", "POST"])
def stego():
    if request.method == "POST":
        password = request.form.get("password")
        files = request.files.getlist("upload")

        if not password or not files:
            flash("Missing password or file!", "error")
            return render_template("stego.html")
        first_name = files[0].filename.split("/")[0]  # works for folder uploads too
        safe_base_name = secure_filename(first_name)

        # Create a temp folder to collect uploaded files
        temp_upload_dir = os.path.join(UPLOAD_FOLDER, "temp_input")
        if os.path.exists(temp_upload_dir):
            shutil.rmtree(temp_upload_dir)
        os.makedirs(temp_upload_dir, exist_ok=True)

        for file in files:
            # Preserve the relative path (folder structure) from the uploaded folder
            relative_path = file.filename  # e.g., "subdir1/subdir2/file.txt"
            safe_parts = [secure_filename(part) for part in relative_path.split("/")]
            safe_path = os.path.join(*safe_parts)

            file_path = os.path.join(temp_upload_dir, safe_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

        # Output path for image
        output_image_name = f"{safe_base_name}_encrypted.png"
        output_image_path = os.path.join(ENCRYPTED_IMG_FOLDER, output_image_name)

        # Call your function to encrypt and generate image
        folder_to_secure_image(temp_upload_dir, output_image_path, password)

        # Clean temp folder
        shutil.rmtree(temp_upload_dir)

        # Build URL to access image
        image_url = f"/static/uploads/encrypted_images/{output_image_name}"

        return render_template("stego.html", image_url=image_url)

    return render_template("stego.html")
