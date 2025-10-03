from flask import Blueprint, request, render_template, flash, send_file, after_this_request
import os
import io
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

stegomask_bp = Blueprint("masko", __name__)

# Folders for uploads and output
UPLOAD_FOLDER = "app/uploads"
OUTPUT_FOLDER = os.path.join(UPLOAD_FOLDER, "stego_output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_unique_filename(filename: str, suffix: str = None) -> str:
    """
    Retain original filename, add optional suffix and a short UUID for uniqueness.
    Example: secret.png -> secret_recovered_3f7a9b.png
    """
    name, ext = os.path.splitext(secure_filename(filename))
    short_uuid = uuid.uuid4().hex[:6]
    parts = [name]
    if suffix:
        parts.append(suffix)
    parts.append(short_uuid)
    return "_".join(parts) + ext


# -----------------------
# HIDE PNG INSIDE JPEG
# -----------------------
@stegomask_bp.route("/hide-image", methods=["GET", "POST"])
def hide_image():
    if request.method == "POST":
        jpeg_file = request.files.get("cover_jpeg")
        png_file = request.files.get("secret_png")

        if not jpeg_file or not png_file:
            flash("Please upload both JPEG (cover) and PNG (secret) images.", "error")
            return render_template("image_mask.html")

        try:
            # Save JPEG temporarily
            temp_jpeg_path = os.path.join(UPLOAD_FOLDER, secure_filename(jpeg_file.filename))
            jpeg_file.save(temp_jpeg_path)

            # Convert PNG to bytes
            secret_image = Image.open(png_file)
            byte_arr = io.BytesIO()
            secret_image.save(byte_arr, format="PNG")
            secret_png_bytes = byte_arr.getvalue()

            # Append PNG bytes after JPEG end marker
            with open(temp_jpeg_path, "ab") as f:
                f.write(secret_png_bytes)

            # Prepare output path with unique filename
            output_filename = generate_unique_filename(jpeg_file.filename, "stego")
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            os.rename(temp_jpeg_path, output_path)

            # Cleanup after sending
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_path)
                except Exception:
                    pass
                return response

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            flash(f"Failed to hide image: {str(e)}", "error")
            return render_template("image_mask.html")

    return render_template("image_mask.html")


# -----------------------
# EXTRACT PNG FROM STEGO JPEG
# -----------------------
@stegomask_bp.route("/extract-image", methods=["GET", "POST"])
def extract_image():
    if request.method == "POST":
        stego_file = request.files.get("stego_jpeg")

        if not stego_file:
            flash("Please upload the stego JPEG image.", "error")
            return render_template("image_mask.html")

        try:
            # Save stego file temporarily
            temp_stego_path = os.path.join(UPLOAD_FOLDER, secure_filename(stego_file.filename))
            stego_file.save(temp_stego_path)

            # Read JPEG content
            with open(temp_stego_path, "rb") as f:
                content = f.read()

            # Find JPEG end marker (FFD9)
            marker = bytes.fromhex("FFD9")
            try:
                offset = content.index(marker) + 2
            except ValueError:
                raise ValueError("JPEG end marker not found. Not a valid JPEG.")

            # Extract hidden PNG bytes
            hidden_png_data = content[offset:]
            if not hidden_png_data:
                raise ValueError("No hidden PNG found in the JPEG.")

            # Rebuild PNG image
            new_image = Image.open(io.BytesIO(hidden_png_data))
            output_filename = generate_unique_filename(stego_file.filename, "recovered")
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            new_image.save(output_path)

            # Cleanup after sending
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_path)
                except Exception:
                    pass
                return response

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            flash(f"Extraction failed: {str(e)}", "error")
            return render_template("image_mask.html")

    return render_template("image_mask.html")
