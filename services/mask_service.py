import os
import json
import cv2

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def mask_fields(image_id, selected_ids, mask_type="black"):

    json_path = os.path.join("uploads", "json", f"{image_id}.json")

    if not os.path.exists(json_path):
        raise Exception("Detection JSON not found.")

    with open(json_path, "r") as f:
        data = json.load(f)

    image = cv2.imread(data["image_path"])

    detections = data["detections"]

    for detection in detections:

        if detection["id"] not in selected_ids:
            continue

        x1, y1, x2, y2 = detection["bbox"]

        if mask_type == "black":

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                -1
            )

        elif mask_type == "blur":

            roi = image[y1:y2, x1:x2]

            if roi.size == 0:
                continue

            roi = cv2.GaussianBlur(
                roi,
                (35,35),
                30
            )

            image[y1:y2, x1:x2] = roi

        elif mask_type == "pixelate":

            roi = image[y1:y2, x1:x2]

            if roi.size == 0:
                continue

            h, w = roi.shape[:2]

            small = cv2.resize(
                roi,
                (16,16),
                interpolation=cv2.INTER_LINEAR
            )

            pixel = cv2.resize(
                small,
                (w,h),
                interpolation=cv2.INTER_NEAREST
            )

            image[y1:y2, x1:x2] = pixel

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{image_id}_masked.jpg"
    )

    cv2.imwrite(output_path, image)

    return output_path