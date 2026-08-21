# Traffic VDS — Traffic Violation Detection System

AI-based traffic violation detection and challan management system using Computer Vision and Deep Learning.

The system detects traffic violations from images/videos, recognizes vehicle number plates, and supports automatic challan generation and management through a role-based dashboard.

## 🚀 Live Demo

**Railway:** https://trafficvds-production.up.railway.app

## ✨ Features

* Helmet violation detection
* Triple-riding detection
* Mobile phone usage detection
* Vehicle number-plate detection
* Number plate recognition using OCR
* Automatic challan generation
* Challan history and status management
* Traffic rules management
* Super Admin and Sub Admin roles
* Image and video-based detection
* Dashboard for violation monitoring

## 🛠️ Tech Stack

| Component            | Technology                     |
| -------------------- | ------------------------------ |
| Frontend             | Streamlit                      |
| Backend              | FastAPI                        |
| Object Detection     | YOLOv8 (Ultralytics)           |
| OCR                  | EasyOCR                        |
| Computer Vision      | OpenCV                         |
| Database             | Supabase / PostgreSQL          |
| Programming Language | Python                         |
| Model Training       | Google Colab + NVIDIA Tesla T4 |
| Dataset Management   | Roboflow                       |

## 📊 Model Performance

The following results are reported in the project evaluation:

| Module                       |       Performance |
| ---------------------------- | ----------------: |
| Helmet Detection             | **92.72% mAP@50** |
| Triple Riding / Mobile Usage | **88.11% mAP@50** |
| Number Plate Detection       | **~85% Accuracy** |
| OCR Recognition              | **~85% Accuracy** |

### Helmet Detection

* mAP@50: **92.72%**
* mAP@50–95: **70.90%**
* Precision: **87.78%**
* Recall: **89.59%**

### Triple Riding / Mobile Usage Detection

* mAP@50: **88.11%**
* mAP@50–95: **51.49%**
* Precision: **83.40%**
* Recall: **81.70%**

> These values are the evaluation results reported in the project report and should not be interpreted as guaranteed real-world accuracy.

## 🔄 System Workflow

```text
Image / Video
      ↓
YOLOv8 Violation Detection
      ↓
Number Plate Detection
      ↓
EasyOCR Number Plate Recognition
      ↓
FastAPI Processing
      ↓
Challan Generation
      ↓
Dashboard & Records
```

## 📁 Project Structure

```text
Traffic_VDS_Demo/
│
├── app.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── dashboard.py
│   ├── challans.py
│   ├── detections.py
│   └── rules.py
│
├── utils/
│   ├── auth.py
│   ├── demo_data.py
│   └── ...
│
└── docs/
    └── screenshots/
        ├── super-admin-dashboard.png
        ├── sub-admin-dashboard.png
        ├── helmet-detection.png
        ├── triple-riding.png
        ├── number-plate-ocr.png
        ├── generated-challan.png
        └── challan-history.png
```

> This public repository is a demo/portfolio version. Private credentials, trained model weights, private datasets and production configuration are intentionally excluded.

## 🖼️ Screenshots

### Super Admin Dashboard

Add the **Super Admin Dashboard screenshot** from the project report here.

Save it as:

```text
docs/screenshots/super-admin-dashboard.png
```

Then add:

```markdown
![Super Admin Dashboard](docs/screenshots/super-admin-dashboard.png)
```

### Sub Admin Dashboard

Add the **Sub Admin Dashboard screenshot** here.

```markdown
![Sub Admin Dashboard](docs/screenshots/sub-admin-dashboard.png)
```

### Helmet Detection

Add the **Helmet Detection Result** screenshot here.

```markdown
![Helmet Detection](docs/screenshots/helmet-detection.png)
```
```markdown
![Helmet Detection](docs/screenshots/helmet-detection.png)
```

Helmet Detection Video

▶️ Watch Helmet Detection Demo

Replace YOUR_VIDEO_LINK_HERE with your uploaded video link.

### Triple Riding Detection

Add the **Triple Riding Detection Result** screenshot here.

```markdown
![Triple Riding Detection](docs/screenshots/triple-riding.png)
```
```markdown
![Triple Riding Detection](docs/screenshots/triple-riding.png)
```

### Number Plate & OCR

Add the **Number Plate Detection / OCR Result** screenshot here.

```markdown
![Number Plate OCR](docs/screenshots/number-plate-ocr.png)
```

### Generated Challan

Add the **Generated Challan** screenshot here.

```markdown
![Generated Challan](docs/screenshots/generated-challan.png)
```

### Challan History

Add the **Challan History** screenshot here.

```markdown
![Challan History](docs/screenshots/challan-history.png)
```

## 👥 Role-Based Access

### Super Admin

* Manage Sub Admin accounts
* Create and manage traffic rules
* Perform image/video violation detection
* View complete challan history
* Update challan amount
* Change challan status
* Monitor system activities

### Sub Admin

* Perform image/video violation detection
* Generate challans
* View traffic rules
* Access personal detection and violation records

## ⚠️ Limitations

* Detection performance may decrease under poor lighting.
* Small or blurred number plates may not be recognized correctly.
* Partial occlusion can affect object detection.
* Rain and fog can reduce image quality.
* OCR accuracy may decrease for damaged or unclear number plates.

## 🔮 Future Scope

* Night-time traffic detection
* Speed violation detection
* Live CCTV integration
* Real-time video processing
* RTO/vehicle database integration
* Automated SMS/email notifications
* Mobile application
* Large-scale cloud deployment

## 📌 Project Note

This project was developed for academic and portfolio demonstration purposes and demonstrates the practical application of Computer Vision, Deep Learning, OCR, APIs, databases and web technologies for intelligent traffic monitoring.

The public repository contains a demo-safe version and does not expose private credentials, production database configuration or trained model weights.
