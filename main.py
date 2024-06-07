from fastapi import FastAPI, UploadFile, Form, File, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from falcon_signature import FalconSignature
from pydantic import BaseModel
from models import User, ChingsPhu
from database import user_collection, gdc_collection, chingsphu_collection
from database_collections import create_user, create_chingsphu
import tempfile
import shutil
import os
from auth import create_access_token, decode_access_token, verify_password, hash_password
import qrcode
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import img2pdf

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginForm(BaseModel):
    username: str
    password: str

@app.post("/signup/")
async def signup(user: User):
    existing_user = await user_collection.find_one(user.cccd)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already in use")
    user.password = hash_password(user.password)
    return await create_user(user)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"cccd": form_data.username})
    if user and verify_password(form_data.password, user["password"]):
        access_token = create_access_token(data={"sub": form_data.username, "type": "user"})
        return {"access_token": access_token, "token_type": "bearer"}

    chingsphu = await chingsphu_collection.find_one({"CP_username": form_data.username})
    if chingsphu and verify_password(form_data.password, chingsphu["password"]):
        access_token = create_access_token(data={"sub": form_data.username, "type": "chingsphu"})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Invalid username or password")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return {"username": username}

@app.post("/chingsphu/")
async def create_chingsphu_endpoint(chingsphu: ChingsPhu):
    return await create_chingsphu(chingsphu)

@app.get("/keygen")
async def keygen():
    try:
        falcon = FalconSignature()
        falcon.generate_keys()
        return JSONResponse(status_code=200, content={"Status": "Success", "Message": "Keys generated successfully!"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"Status": "Error", "Message": str(e)})

@app.post("/sign")
async def sign(cccd: str = Form(...), CP_username: str = Form(...), start_place: str = Form(...), destination_place: str = Form(...), token: str = Depends(oauth2_scheme)):
    try:
        user_access = decode_access_token(token)
        if user_access is None or user_access["type"] != "chingsphu":
            raise HTTPException(status_code=401, detail="Not authorized")
        
        user = await user_collection.find_one({"_id": cccd})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        chingsphu = await chingsphu_collection.find_one({"_id": CP_username})
        if not chingsphu:
            raise HTTPException(status_code=404, detail="Chingsphu not found")

        user_info = {
            "cccd": user["cccd"],
            "name": user["name"],
        }

        chingsphu_info = {
            "CP_username": chingsphu["CP_username"],
            "sign_place": chingsphu["sign_place"],
        }
        
        road_info = {
            "start_place": start_place,
            "destination_place": destination_place,
        }

        temp_path = "template/input.pdf"

        falcon = FalconSignature()
        message, gdc_id = await falcon.sign_pdf(temp_path, user_info, chingsphu_info, road_info)
        
        if gdc_id is None:
            raise Exception("Failed to sign PDF and save signature to GDC", message)
        
        # Generate QR Code with verification link
        verification_url = f"http://localhost:8000/verify/{gdc_id}"
        qr = qrcode.make(verification_url)
        qr_path = f"{temp_path}.png"
        qr.save(qr_path)

        # Convert QR code PNG to PDF
        qr_pdf_path = f"{temp_path}_qr.pdf"
        with Image.open(qr_path) as img:
            conv = img2pdf.convert(img.filename)
            with open(qr_pdf_path, "wb") as file:
                file.write(conv)

        # Insert QR Code into PDF
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(temp_path)

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        qr_pdf_reader = PdfReader(qr_pdf_path)
        pdf_writer.add_page(qr_pdf_reader.pages[0])

        signed_pdf_path = f"signed_pdf/{gdc_id}.pdf"
        with open(signed_pdf_path, "wb") as f_out:
            pdf_writer.write(f_out)

        os.remove(qr_path)
        os.remove(qr_pdf_path)

        return JSONResponse(status_code=200, content={"Status": "Success", "Message": message, "Signed PDF Path": signed_pdf_path})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"Status": "Error", "Message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"Status": "Error", "Message": str(e)})
    
@app.post("/verify/{gdc_id}")
async def verify(gdc_id: str):
    try:
        gdc = await gdc_collection.find_one({"gdc_Id": gdc_id})
        if not gdc:
            raise HTTPException(status_code=404, detail="GDC not found")

        user = await user_collection.find_one({"_id": gdc["cccd"]})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        chingsphu = await chingsphu_collection.find_one({"_id": gdc["CP_username"]})
        if not chingsphu:
            raise HTTPException(status_code=404, detail="Chingsphu not found")

        user_info = {
            "cccd": user["cccd"],
            "name": user["name"],
        }

        chingsphu_info = {
            "name": chingsphu["name"],
            "sign_place": chingsphu["sign_place"],
        }
        
        road_info = {
            "start_place": gdc["start_place"],
            "destination_place": gdc["destination_place"],
        }

        signed_pdf_path = f"{gdc_id}.pdf"

        falcon = FalconSignature()
        is_valid = await falcon.verify_pdf(gdc_id, signed_pdf_path, user_info, chingsphu_info, road_info)
        if is_valid:
            return JSONResponse(status_code=200, content={"Status": "Success", "Message": "Signature verified successfully!"})
        else:
            return JSONResponse(status_code=200, content={"Status": "Error", "Message": "Signature verification failed!"})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"Status": "Error", "Message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"Status": "Error", "Message": str(e)})