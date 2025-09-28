# 📘 Setup Guide – Flask Orders API

## 🔹 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/orders-api.git
cd orders-api
```

## 🔹 2. set the virtual env

### macOS/Linux  
```bash
python -m venv .venv
source .venv/bin/activate
```
### Windows (PowerShell)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 🔹 3. Install Dependencies   
```bash
pip install -r requirements.txt
```

## 🔹 4. Run the Application
```bash
python app.py
```

The app will be available at: http://127.0.0.1:5000/   


## 🔹 5. Test the API Endpoints  
### Health Check
- `GET /health`

### Orders
- `GET /orders`
- `POST /orders`
- `GET /orders/<id>`
- `DELETE /orders/<id>`

### Frontend UI
- `GET /`
