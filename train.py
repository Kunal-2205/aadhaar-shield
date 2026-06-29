from ultralytics import YOLO
import torch
import os


def main():

    print("=" * 60)
    print("YOLOv8 Training")
    print("=" * 60)

    print("Torch Version :", torch.__version__)
    print("CUDA Available :", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU :", torch.cuda.get_device_name(0))

    print("=" * 60)

    # Create folders
    os.makedirs("models/train_results", exist_ok=True)
    os.makedirs("models/weights", exist_ok=True)

    # Load pretrained model
    model = YOLO("yolov8s.pt")

    model.train(

        # Dataset
        data="dataset/data.yaml",

        # Training
        epochs=120,
        imgsz=640,
        batch=4,

        # GPU
        device=0,

        workers=2,

        cache=False,

        # Optimizer
        optimizer="AdamW",

        lr0=0.001,

        cos_lr=True,

        patience=30,

        # Augmentation
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,

        degrees=3,
        translate=0.08,
        scale=0.40,
        shear=2,
        perspective=0.0005,

        fliplr=0.5,

        mosaic=0.5,

        mixup=0.0,

        close_mosaic=10,

        # Save inside project
        project="models",
        name="train_results",

        exist_ok=True,

        pretrained=True,

        plots=True,

        verbose=True
    )

    print("\nTraining Completed!")
    print("Best model saved in:")
    print("models/train_results/weights/best.pt")


if __name__ == "__main__":
    main()