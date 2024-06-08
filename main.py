from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse, FileResponse
from falcon_signature import FalconSignature
from pydantic import BaseModel
from models import User, ChingsPhu
from database import user_collection, gdc_collection, chingsphu_collection
from database_collections import create_user, create_chingsphu
import os
import random
import string
from datetime import datetime
from auth import create_access_token, decode_access_token, verify_password, hash_password
from QR_and_Text import generate_qr_code, insert_qr_to_pdf, create_watermark, add_watermark

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginForm(BaseModel):
    username: str
    password: str
    
class SignModel(BaseModel):
    gdc_Id: str
    CP_username: str

class RequestSignModel(BaseModel):
    cccd: str
    start_place: str
    destination_place: str

@app.post("/signup/")
async def signup(user: User):
    existing_user = await user_collection.find_one(user.cccd)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already in use")
    return await create_user(user)

@app.post("/token")
async def login(user: LoginForm):
    user_db = await user_collection.find_one({"cccd": user.username})
    if user_db and verify_password(user.password, user_db["password"]):
        access_token = create_access_token(data={"sub": user.username, "type": "user"})
        return {"access_token": access_token, "token_type": "bearer"}

    chingsphu = await chingsphu_collection.find_one({"CP_username": user.username})
    if chingsphu and verify_password(user.password, chingsphu["password"]):
        access_token = create_access_token(data={"sub": user.username, "type": "chingsphu"})
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
async def keygen(token: str = Depends(oauth2_scheme)):
    try:
        user_access = decode_access_token(token)
        if user_access is None or user_access["type"] != "chingsphu":
            raise HTTPException(status_code=401, detail="Not authorized")
        
        falcon = FalconSignature()
        falcon.generate_keys()
        return JSONResponse(status_code=200, content={"Status": "Success", "Message": "Keys generated successfully!"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"Status": "Error", "Message": str(e)})

@app.post("/sign")
async def sign(sign_data: SignModel, token: str = Depends(oauth2_scheme)):
    try:
        user_access = decode_access_token(token)
        if user_access is None or user_access["type"] != "chingsphu":
            raise HTTPException(status_code=401, detail="Not authorized")
        
        gdc = await gdc_collection.find_one({"gdc_Id": sign_data.gdc_Id})
        if not gdc:
            raise HTTPException(status_code=404, detail="GDC not found")

        user = await user_collection.find_one({"cccd": gdc["cccd"]})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        chingsphu = await chingsphu_collection.find_one({"_id": sign_data.CP_username})
        if not chingsphu:
            raise HTTPException(status_code=404, detail="Chingsphu not found")

        user_info = {
            "cccd": user["cccd"],
        }

        chingsphu_info = {
            "CP_username": chingsphu["CP_username"],
            "sign_place": chingsphu["sign_place"],
        }
        
        road_info = {
            "start_place": gdc["start_place"],
            "destination_place": gdc["destination_place"],
        }

        temp_path = "template/gdc.pdf"

        falcon = FalconSignature()
        message, gdc_id, signature = await falcon.sign_pdf(temp_path, user_info, chingsphu_info, road_info, sign_data.gdc_Id)
        
        if gdc_id is None:
            raise Exception("Failed to sign PDF and save signature to GDC", message)
        
        update_data = {
            "CP_username": chingsphu["CP_username"],
            "sign_place": chingsphu["sign_place"],
            "sign_date": datetime.now().isoformat(),
            "signature": signature
        }
                
        await gdc_collection.update_one({"gdc_Id": sign_data.gdc_Id}, {"$set": update_data})

        verification_url = f"http://localhost:8000/verify/{gdc_id}"
        qr_code_path = "qr_code.png"
        generate_qr_code(verification_url, qr_code_path)

        qr_inserted_pdf_path = f"signed_pdf/{gdc_id}_qr.pdf"
        insert_qr_to_pdf(temp_path, qr_code_path, qr_inserted_pdf_path)
        os.remove(qr_code_path)

        font_path = "Sitka Banner.ttf"
        watermark_pdf_path = "watermark.pdf"
        create_watermark(user, gdc, font_path, watermark_pdf_path)

        signed_pdf_path = f"signed_pdf/{gdc_id}.pdf"
        add_watermark(qr_inserted_pdf_path, watermark_pdf_path, signed_pdf_path)

        os.remove(watermark_pdf_path)
        os.remove(qr_inserted_pdf_path)

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
    
@app.post("/request_sign")
async def request_sign(request: RequestSignModel, token: str = Depends(oauth2_scheme)):
    user_access = decode_access_token(token)
    if user_access is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    user = await user_collection.find_one({"_id": request.cccd})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    gdc_Id = ''.join(random.choices(string.digits, k=6))
    while await gdc_collection.find_one({"gdc_Id": gdc_Id}):
        gdc_Id = ''.join(random.choices(string.digits, k=6))

    gdc = {
        "_id": gdc_Id,
        "gdc_Id": gdc_Id,
        "cccd": request.cccd,
        "start_place": request.start_place,
        "destination_place": request.destination_place,
    }
    await gdc_collection.insert_one(gdc)

    return {"gdc_Id": gdc_Id}

@app.get("/download_signed/{gdc_id}")
async def download_signed(gdc_id: str):
    gdc = await gdc_collection.find_one({"gdc_Id": gdc_id})

    if not gdc or "signature" not in gdc:
        raise HTTPException(status_code=404, detail="GDC not found or not signed yet")

    signed_pdf_path = f"signed_pdf/{gdc_id}.pdf"
    return FileResponse(signed_pdf_path, filename="signed_GDC.pdf")