# 🍄 ForageCompanion32

_ForageCompanion32_ is a mini-project to identify poisonous mushrooms using an AI-powered image classifier. Just upload a mushroom photo and get instant feedback on its safety and characteristics. Perfect for hikers, mushroom foragers, and the curious nature lover!

---

## start the Application in a Single Command

To set up the environment, install dependencies, build the frontend, and launch the app—all in one go:

```bash
make start
```

---

## Development Setup

### 1. Build Frontend

To manually build the frontend:

```bash
make build
```

### 2. Start Frontend Dev Server

Useful during frontend development with hot-reloading:

```bash
make dev
```

### Run Python Backend

Make sure the environment is activated, then:

```bash
make run
```

---

## Install Dependencies and Set Up Environment

To create the virtual environment, install Python and frontend dependencies, and build the app:

```bash
make install
```

---

## 📁 Project Structure

```
ForageCompanion32/
├── frontend/            # Frontend React or Vite app
├── model/               # Trained Keras/TensorFlow model
├── static/              # Frontend build output
├── templates/           # HTML templates if using Flask/Jinja2
├── entrypoint.py        # Main backend entry point
├── setup.sh             # Shell script to create virtualenv
├── requirements-*.txt   # Prod/dev/test dependency files
├── Makefile             # Cross-platform commands
└── README.md            # You're here!
```

---

## Tech Stack

- **Frontend**: html/css/typescript (cause I hate react slop)
- **Backend**: Flask + TensorFlow/Keras
- **Model**: Custom-trained image classifier for mushrooms
- **Packaging**: Make + virtualenv
