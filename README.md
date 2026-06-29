# 🛡️ Aadhaar Shield

An AI-powered document privacy system that automatically detects and masks sensitive information from Aadhaar cards using **YOLOv8**, **FastAPI**, **Streamlit**, and **OpenCV**.

This project helps protect personal information by allowing users to upload an Aadhaar card, detect confidential fields, select what they want to hide, and generate a masked version of the document.

---

## 🚀 Features

- Detect sensitive fields using a custom-trained YOLOv8 model
- Interactive Streamlit web interface
- FastAPI backend with REST APIs
- Select specific fields to mask
- Multiple masking techniques:
  - Black Mask
  - Gaussian Blur
  - Pixelation
- Fast and accurate inference
- GPU (CUDA) support
- Download the masked image

---

## 📌 Supported Fields

The model can detect the following Aadhaar card fields:

- Name
- Aadhaar Number
- Date of Birth
- Gender

> The project can be extended to support PAN Card, Passport, Voter ID, and other identity documents.

---

# 🏗️ Project Architecture

```
                User Uploads Image
                         │
                         ▼
               Streamlit User Interface
                         │
                         ▼
                  FastAPI Backend
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 YOLOv8 Detection Service      Masking Service
          │                             │
          └──────────────┬──────────────┘
                         ▼
                  Masked Image Output
```

---

# 📂 Project Structure

```
aadhaar-shield/
│
├── app.py
├── main.py
├── train.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── dataset/
│   ├── data.yaml
│   ├── README.dataset.txt
│   └── README.roboflow.txt
│
├── models/
│   └── weights/
│       ├── best.pt
│       └── last.pt
│
├── routes/
│   ├── detect.py
│   └── mask.py
│
├── services/
│   ├── detector_service.py
│   └── mask_service.py
│
├── uploads/
├── outputs/
└── runs/
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| YOLOv8 | Object Detection |
| FastAPI | Backend API |
| Streamlit | Frontend Interface |
| OpenCV | Image Processing |
| PyTorch | Deep Learning Framework |
| NumPy | Numerical Operations |
| Pillow | Image Handling |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Kunal-2205/aadhaar-shield.git

cd aadhaar-shield
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Backend

```bash
uvicorn main:app --reload
```

Open Swagger API:

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Run the Frontend

```bash
streamlit run app.py
```

---

# 📖 Workflow

1. Upload an Aadhaar card image.
2. Detect sensitive fields using YOLOv8.
3. Review all detected fields.
4. Select the fields you want to hide.
5. Choose a masking method.
6. Generate the masked image.
7. Download the protected document.

---

# 📂 Dataset

The model was trained using a custom dataset in YOLO format.

Dataset configuration:

```
dataset/data.yaml
```

---

# 🧠 AI Model

- Model: YOLOv8
- Framework: Ultralytics
- Task: Object Detection
- Training: Custom Dataset
- Inference: Real-time Detection

---

# 📊 Project Highlights

- Custom-trained YOLOv8 model
- GPU acceleration supported
- FastAPI REST API
- Interactive Streamlit interface
- Multiple masking techniques
- Easy to extend for other identity documents

---

# 🚀 Future Improvements

- Support PAN Card
- Support Passport
- Support Voter ID
- OCR Integration
- Docker Support
- Cloud Deployment
- Batch Processing
- Mobile-Friendly Interface

---

# 🤝 Contributing

Contributions are welcome!

If you find a bug or have an idea for improvement:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

# 👨‍💻 Author

**Kunal Darji**

GitHub: https://github.com/Kunal-2205

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
