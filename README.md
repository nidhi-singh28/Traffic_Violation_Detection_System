# 🚦 Traffic VDS — Traffic Challan Management System

> **Public Portfolio / Demo Build**

Traffic VDS is an AI-assisted traffic violation and challan management platform designed to demonstrate how computer vision, violation workflows, traffic rules, and administrative dashboards can be brought together in one web application.

This repository is the **public demo/portfolio version** of the project. It is intentionally separated from the original private academic/development repository.

---

## 🌐 Live Demo

**Live App:** _Add your deployed Streamlit URL here_

> 💡 After deployment, replace the line above with your live URL.

### Demo Accounts

| Role | Email | Password |
|---|---|---|
| Super Admin | `admin@traffic-demo.app` | `demo123` |
| Sub Admin | `subadmin@traffic-demo.app` | `demo123` |

These are **demo-only credentials**. No production account or real user data is used in this repository.

---

## 📸 Screenshots

Add screenshots to `docs/screenshots/` and use the filenames below.

### 1. Login / Landing Page
**File:** `docs/screenshots/01-login.png`

Show:
- Traffic VDS title
- Login form
- Demo access information

<!-- Add image here after uploading it:
![Traffic VDS Login](docs/screenshots/01-login.png)
-->

### 2. Super Admin Dashboard
**File:** `docs/screenshots/02-super-admin-dashboard.png`

Show:
- Total challans
- Pending/approved/paid statistics
- Revenue
- Dashboard navigation

<!--
![Super Admin Dashboard](docs/screenshots/02-super-admin-dashboard.png)
-->

### 3. Challan History
**File:** `docs/screenshots/03-challan-history.png`

Show:
- Challan list
- Status
- Fine amount
- Vehicle number
- Filtering/search

<!--
![Challan History](docs/screenshots/03-challan-history.png)
-->

### 4. AI Violation Detection — Demo Mode
**File:** `docs/screenshots/04-detection.png`

Show:
- Upload image/video section
- Detection result
- Detected violation
- Vehicle number
- Demo Mode notice

<!--
![Violation Detection](docs/screenshots/04-detection.png)
-->

### 5. Traffic Rules
**File:** `docs/screenshots/05-traffic-rules.png`

Show:
- Traffic rules
- Fine amounts
- Categories
- Rule management

<!--
![Traffic Rules](docs/screenshots/05-traffic-rules.png)
-->

### 6. Sub Admin Management
**File:** `docs/screenshots/06-sub-admins.png`

Show:
- Sub-admin list
- Active/inactive status
- Management controls

<!--
![Sub Admin Management](docs/screenshots/06-sub-admins.png)
-->

### 7. Sub Admin Dashboard
**File:** `docs/screenshots/07-sub-admin-dashboard.png`

Show:
- Personal challan statistics
- My challans
- Detection workflow

<!--
![Sub Admin Dashboard](docs/screenshots/07-sub-admin-dashboard.png)
-->

---

## ✨ Features

### Super Admin

- Dashboard with challan statistics and revenue
- Challan history with status and fine management
- Violation detection records
- Traffic rules management
- Sub-admin management
- Image/video violation detection workflow
- Challan generation from detected violations

### Sub Admin

- Personal dashboard
- View own challans
- Upload media for violation detection
- Generate challans from detected violations
- View traffic rules

### Detection Workflow

The original project architecture includes computer-vision components for:

- Helmet violation detection
- Triple riding detection
- Number plate recognition using OCR
- Photo and video processing

For this **public portfolio build**, the detection engine is deliberately replaced by a lightweight **mock/demo detector** so that the repository can run without private trained weights, large ML dependencies, or a production backend.

The UI still demonstrates the complete workflow:

```text
Upload Image / Video
        ↓
Demo Detection Engine
        ↓
Violation Result
        ↓
Traffic Rule Matching
        ↓
Fine Calculation
        ↓
Generate Challan
        ↓
Challan History / Dashboard
```

---

## 🏗️ Architecture

### Original Project Concept

```text
                ┌───────────────────────┐
                │   Streamlit Frontend  │
                │ Dashboard / Admin UI  │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │      FastAPI API      │
                │ Detection Pipeline    │
                └───────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          YOLO Models    EasyOCR       OpenCV
          Helmet/Triple  Number Plate   Media
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                  Challan Management
```

### Public Demo Architecture

```text
                ┌───────────────────────┐
                │   Streamlit Frontend  │
                │ Dashboard / Admin UI  │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Demo Detection      │
                │    Mock Engine        │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ In-Session Demo Store │
                │ Rules / Challans /    │
                │ Detection Records     │
                └───────────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Original Backend | FastAPI |
| Original Computer Vision | YOLO / Ultralytics, OpenCV |
| Original OCR | EasyOCR |
| Original ML Framework | PyTorch |
| Original Database | Supabase / PostgreSQL |
| Public Demo Storage | Streamlit session state |
| Public Demo Detection | Python mock detection engine |

---

## 📁 Project Structure

```text
Traffic_VDS_Demo/
├── app.py
├── requirements.txt
├── runtime.txt
├── .gitignore
├── README.md
├── .streamlit/
│   └── config.toml
├── pages/
│   ├── challan_history.py
│   ├── detect_violation.py
│   ├── my_challans.py
│   ├── sub_admin_dashboard.py
│   ├── sub_admin_management.py
│   ├── super_admin_dashboard.py
│   ├── traffic_rules.py
│   ├── traffic_rules_view.py
│   └── violation_detections.py
├── utils/
│   ├── backend_api.py
│   ├── styles.py
│   └── supabase_client.py
└── docs/
    └── screenshots/
```

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Traffic_VDS_Demo
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Streamlit application

```bash
streamlit run app.py
```

The app will open in your browser.

---

## ☁️ Deployment

This public build is designed to be easy to deploy as a Streamlit application.

### Streamlit deployment

1. Push this repository to GitHub.
2. Create a new Streamlit deployment.
3. Select this repository.
4. Set the main file to:

```text
app.py
```

5. Deploy.

No Supabase credentials, API keys, YOLO weights, or FastAPI server are required for this demo build.

---

## 🔐 Privacy & Security

This public repository intentionally excludes:

- Production Supabase credentials
- API keys
- Passwords
- `.streamlit/secrets.toml`
- Trained YOLO model weights
- Private datasets
- Real challan records
- Real user information
- Production deployment configuration
- Private development documentation

The demo uses synthetic/sample records only.

---

## 📌 About the Public Demo

This repository is intended for **portfolio and academic demonstration purposes**.

The public build demonstrates the application's interface, workflow, role-based navigation, challan management, traffic-rule management, and detection-to-challan flow without exposing private project assets or production credentials.

The original project may contain a fuller computer-vision implementation with trained models and backend services; those private assets are intentionally not included here.

---

## 👩‍💻 Project Collaboration

The Traffic VDS system was developed collaboratively as an academic/project implementation.

This public repository is a **cleaned portfolio/demo build** created separately from the original private development repository.

---

## 📬 Future Improvements

- Connect the public UI to a secured production backend
- Replace mock detection with deployable optimized ML inference
- Add secure cloud storage for evidence
- Add stronger authentication and role-based authorization
- Add payment/status integration
- Add analytics and reporting
- Add model confidence and detection visualizations

---

## ⭐ Portfolio Note

If you are viewing this project as a portfolio piece, the recommended flow is:

**Login → Super Admin Dashboard → Challan History → Traffic Rules → Detect Violation → Generate Challan → Violation Detections**

The screenshots above are intentionally organized around this user journey.
