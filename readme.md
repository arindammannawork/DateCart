Activate vertual environment:
.venv\Scripts\Activate.ps1

install all dependencies needed
pip install -r requirements.txt

start dev server  //// dont use this
fastapi dev main.py


start with uvicorn
uvicorn app:app --reload
