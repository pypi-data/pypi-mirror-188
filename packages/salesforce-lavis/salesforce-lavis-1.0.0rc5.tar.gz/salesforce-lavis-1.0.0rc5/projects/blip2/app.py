from flask import Flask, request
from flask_cors import CORS
from lavis.models import load_model_and_preprocess
from PIL import Image

import torch
import os

app = Flask(__name__)
CORS(app)


def decode_image(img_obj):
    img = Image.open(img_obj).convert("RGB")
    return img


def convert_to_bool(value):
    if isinstance(value, bool):
        return value

    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        raise ValueError(f"Unknown value {value}")


@app.route("/api/generate", methods=["POST"])
def generate():
    """VQA API
    Usage:
        curl -X POST 127.0.0.1:5000/api/generate
            -F "image=@/path/to/image"
            -F "prompt=What is this?"
    """
    r = request

    request_dict = r.form.to_dict()

    # parse request
    image_file = r.files.get("image")
    use_nucleus_sampling = convert_to_bool(
        request_dict.get("use_nucleus_sampling", False)
    )
    prompt = request_dict["prompt"]

    # load and process image
    image = decode_image(image_file)
    image = vis_processors["eval"](image).unsqueeze(0).to(device)

    if use_nucleus_sampling: 
        output = model.generate({
            "image": image,
            "prompt":prompt
        }, use_nucleus_sampling=True, temperature=0.8)
    else:
        output = model.generate({"image": image,"prompt":prompt})

    output = ["test"]
    
    return output


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model, vis_processors, _ = load_model_and_preprocess(
        name="blip2_t5",
        model_type="pretrain_flant5xl",
        is_eval=True,
        device=device
    )

    app.debug = True

    # UPLOAD FOLDER
    app.config["UPLOAD_FOLDER"] = "static/uploads"

    # make upload folder if not exists
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    app.run(host='0.0.0.0', debug=True)
