from flask import Blueprint, request, render_template, flash, send_file, session, redirect, url_for
import os
import shutil
from werkzeug.utils import secure_filename
from app.reverse_tools import recover_folder_from_image

decrypt_bp = Blueprint("decrypt", __name__)
UPLOAD_FOLDER = "app/uploads"
RECOVERED_FOLDER = os.path.join(UPLOAD_FOLDER, "recovered_output")
os.makedirs(RECOVERED_FOLDER, exist_ok=True)

# Global variable to hold last generated file (not recommended in production)
last_generated_file = None

@decrypt_bp.route("/stego/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        password = request.form.get("password_decrypt")
        file = request.files.get("upload_decrypt")

        if not password or not file:
            flash("Missing password or image!", "error")
            return render_template("stego.html")
        
        
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, "temp_image.png")
        file.save(input_path)

        output_dir = os.path.join(RECOVERED_FOLDER, "recovered")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        try:
            recover_folder_from_image(input_path, output_dir, password)
        except Exception as e:
            flash("Decryption failed: Incorrect password or corrupted image.", "error")
            return render_template("stego.html")
            #return redirect(url_for("decrypt.decrypt"))

        shutil.make_archive(output_dir, 'zip', output_dir)
        os.remove(input_path)

        # Directly send the zip file for download (no redirect!)
        return send_file(output_dir + ".zip", as_attachment=True)

    # GET request — show the page
    return render_template("stego.html")
