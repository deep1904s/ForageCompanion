import os
import base64
from io import BytesIO
from flask import Flask, request, render_template
from utils.predictor import predict_mushroom_from_stream
from utils import logger, allowed_file
from config import app_config

app = Flask(__name__)
app.config.from_mapping(
    BASE_DIR=app_config.BASE_DIR,
    MAX_CONTENT_LENGTH=app_config.MAX_CONTENT_LENGTH,
    ALLOWED_EXTENSIONS=app_config.ALLOWED_EXTENSIONS,
)

logger.info("App configuration loaded successfully.")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        logger.info("Received POST request at /")

        if "file" not in request.files:
            logger.warning("No file part in request")
            return render_template("index.html", error="No file part")

        file = request.files["file"]

        if file.filename == "":
            logger.warning("No selected file in upload")
            return render_template("index.html", error="No selected file")

        if file and allowed_file(file.filename):
            try:
                logger.info("Processing file: %s", file.filename)
                file_content = file.read()
                image_stream = BytesIO(file_content)

                predictions = predict_mushroom_from_stream(image_stream)
                logger.info("Prediction successful for file: %s", file.filename)

                encoded_img = base64.b64encode(file_content).decode("utf-8")
                ext = str(file.filename).rsplit(".", 1)[1].lower()
                mime = "png" if ext == "png" else "jpeg"
                image_data = f"data:image/{mime};base64,{encoded_img}"

                return render_template(
                    "index.html",
                    filename=file.filename,
                    predictions=predictions,
                    image_data=image_data,
                )
            except Exception as e:
                logger.exception("Error during prediction for file: %s", file.filename)
                return render_template(
                    "index.html", error=f"Prediction error: {str(e)}"
                )
        else:
            logger.warning("Disallowed file type attempted: %s", file.filename)
            return render_template("index.html", error="File type not allowed")

    logger.debug("GET request received at /")
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting app on port %d", port)
    app.run(host="0.0.0.0", port=port)
