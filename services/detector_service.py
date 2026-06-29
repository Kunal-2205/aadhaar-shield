from ultralytics import YOLO
import cv2
import os
import json
import uuid

# ==========================
# Load Model Once
# ==========================
MODEL_PATH = "models/weights/best.pt"
model = YOLO(MODEL_PATH)

# ==========================
# Class Names (raw codes from dataset/data.yaml — 18 classes)
# These raw codes are what the model itself outputs (index -> code).
# ==========================
CLASS_NAMES = {
    0: "a_back",
    1: "a_bar",
    2: "a_emb",
    3: "a_front",
    4: "a_govt",
    5: "a_masked",
    6: "a_num",
    7: "a_photo",
    8: "a_qr",
    9: "a_top",
    10: "a_uidai",
    11: "a_vid",
    12: "card_passport",
    13: "card_voter_id",
    14: "p_emb",
    15: "p_front",
    16: "p_gov",
    17: "p_num",
}

# ==========================
# Human-readable display labels
# (cosmetic only — maps each raw code to a friendly name shown
# in the UI / JSON / preview image. Detection itself is unchanged.)
# ==========================
DISPLAY_LABELS = {
    "a_back": "Aadhaar Back Side",
    "a_bar": "Aadhaar Barcode",
    "a_emb": "Aadhaar Emblem",
    "a_front": "Aadhaar Front Side",
    "a_govt": "Government of India Text",
    "a_masked": "Masked Aadhaar Region",
    "a_num": "Aadhaar Number",
    "a_photo": "Photo",
    "a_qr": "QR Code",
    "a_top": "Aadhaar Top Section",
    "a_uidai": "UIDAI Logo/Text",
    "a_vid": "Virtual ID (VID)",
    "card_passport": "Passport Card",
    "card_voter_id": "Voter ID Card",
    "p_emb": "Passport Emblem",
    "p_front": "Passport Front Side",
    "p_gov": "Passport Govt Text",
    "p_num": "Passport Number",
}

# ==========================
# Box colors per class (BGR) — keyed by raw code
# ==========================
COLORS = {
    "a_back": (180, 130, 70),
    "a_bar": (60, 180, 220),
    "a_emb": (140, 90, 200),
    "a_front": (0, 255, 0),
    "a_govt": (200, 200, 0),
    "a_masked": (90, 90, 90),
    "a_num": (0, 0, 255),
    "a_photo": (255, 128, 0),
    "a_qr": (255, 0, 255),
    "a_top": (0, 200, 200),
    "a_uidai": (255, 0, 0),
    "a_vid": (100, 255, 100),
    "card_passport": (50, 50, 220),
    "card_voter_id": (220, 50, 220),
    "p_emb": (150, 90, 100),
    "p_front": (0, 165, 255),
    "p_gov": (170, 170, 0),
    "p_num": (0, 0, 150),
}
DEFAULT_COLOR = (255, 255, 255)

# ==========================
# Folders
# ==========================
IMAGE_DIR = "uploads/images"
JSON_DIR = "uploads/json"
PREVIEW_DIR = "uploads/previews"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)


def detect_fields(upload_file):

    # -------------------------
    # Generate Unique ID
    # -------------------------
    image_id = str(uuid.uuid4())

    extension = os.path.splitext(upload_file.filename)[1]

    image_path = os.path.join(
        IMAGE_DIR,
        image_id + extension
    )

    # -------------------------
    # Save Uploaded Image
    # -------------------------
    with open(image_path, "wb") as f:
        f.write(upload_file.file.read())

    # -------------------------
    # Read Image
    # -------------------------
    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Failed to load uploaded image.")

    # -------------------------
    # YOLO Prediction
    # IMPORTANT:
    # Use image_path instead of image
    # -------------------------
    results = model.predict(
        source=image_path,
        conf=0.30,
        save=False,
        verbose=False
    )

    detections = []
    detection_id = 1

    # -------------------------
    # Process YOLO Detections
    # (covers all 18 classes, including QR Code — no separate
    # rule-based QR detection needed anymore)
    # -------------------------
    for result in results:

        for box in result.boxes:

            cls = int(box.cls.item())
            conf = float(box.conf.item())
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            raw_code = CLASS_NAMES.get(cls, str(cls))
            label = DISPLAY_LABELS.get(raw_code, raw_code)

            detections.append({
                "id": detection_id,
                "class": label,
                "class_code": raw_code,
                "confidence": round(conf, 2),
                "bbox": [x1, y1, x2, y2]
            })

            color = COLORS.get(raw_code, DEFAULT_COLOR)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                image,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            detection_id += 1

    # -------------------------
    # Save Preview Image
    # -------------------------
    preview_path = os.path.join(
        PREVIEW_DIR,
        image_id + extension
    )

    cv2.imwrite(preview_path, image)

    # -------------------------
    # Save Detection JSON
    # -------------------------
    json_path = os.path.join(
        JSON_DIR,
        image_id + ".json"
    )

    with open(json_path, "w") as f:
        json.dump(
            {
                "image_id": image_id,
                "image_path": image_path,
                "detections": detections
            },
            f,
            indent=4
        )

    return {
        "image_id": image_id,
        "preview": preview_path,
        "detections": detections
    }