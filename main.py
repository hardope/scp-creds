from fastapi import FastAPI, UploadFile, HTTPException, Form, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from cryptography.fernet import Fernet
import io
import os
import uuid
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# Environment setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./env_sharing.db")

# Database setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class EnvFile(Base):
    __tablename__ = "env_files"
    id = Column(String, primary_key=True, index=True)
    encrypted_data = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# FastAPI app setup
app = FastAPI()

# Database initialization
Base.metadata.create_all(bind=engine)

# Schemas
class UploadResponse(BaseModel):
    download_code: str
    decryption_key: str


@app.post("/upload", response_model=UploadResponse)
def upload_env(file: UploadFile, download_limit: int = 1, expiration_time: int = 5, db: Session = Depends(get_db)):
    try:
        file_content = file.file.read()
        decryption_key = Fernet.generate_key()
        fernet = Fernet(decryption_key)
        encrypted_data = fernet.encrypt(file_content)

        download_code = str(uuid.uuid4())
        env_file = EnvFile(id=download_code, encrypted_data=encrypted_data.decode())

        db.add(env_file)
        db.commit()

        print(f"Download code: {download_limit}, Expiration time: {expiration_time}")

        return {"download_code": download_code, "decryption_key": decryption_key.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/upload_text", response_model=UploadResponse)
def upload_env_text(file_content: str = Form(...), db: Session = Depends(get_db)):
    try:
        decryption_key = Fernet.generate_key()
        fernet = Fernet(decryption_key)
        encrypted_data = fernet.encrypt(file_content.encode())

        download_code = str(uuid.uuid4())
        env_file = EnvFile(id=download_code, encrypted_data=encrypted_data.decode())

        db.add(env_file)
        db.commit()

        return {"download_code": download_code, "decryption_key": decryption_key.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/download/{code}", response_class=StreamingResponse)
def download_env(code: str, decryption_key: str, db: Session = Depends(get_db)):
    env_file = db.query(EnvFile).filter(EnvFile.id == code).first()

    if not env_file:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        fernet = Fernet(decryption_key.encode())
        decrypted_data = fernet.decrypt(env_file.encrypted_data.encode())
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid decryption key")

    memory_file = io.BytesIO(decrypted_data)
    memory_file.seek(0)

    return StreamingResponse(memory_file, media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename=env_file.env"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
