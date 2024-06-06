from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import JSONResponse
from falcon_signature import FalconSignature
from passlib.context import CryptContext
from models import User, GDC, ChingsPhu
from database import user_collection, gdc_collection, chingsphu_collection
from database_collections import create_user, create_gdc, create_chingsphu
import tempfile
import shutil
import os

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

@app.post("/users/")
async def create_user_endpoint(user: User):
    return await create_user(user)

@app.post("/gdc/")
async def create_gdc_endpoint(gdc: GDC):
    return await create_gdc(gdc)

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
        return JSONResponse(status_code=200, content={"Status": "Error", "Message": str(e)})

@app.post("/sign")
async def sign(file: UploadFile = File(...), cccd: str = Form(...), CP_username: str = Form(...), start_place: str = Form(...), destination_place: str = Form(...)):
    try:
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

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        falcon = FalconSignature()
        message = await falcon.sign_pdf(temp_path, user_info, chingsphu_info, road_info)
        return JSONResponse(status_code=200, content={"Status": "Success", "Message": message})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"Status": "Error", "Message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"Status": "Error", "Message": str(e)})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

            
@app.post("/verify")
async def verify(file: UploadFile = File(...), gdc_id: str = Form(...)):
    try:
        gdc = await gdc_collection.find_one({"_id": gdc_id})
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

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        falcon = FalconSignature()
        is_valid = falcon.verify_pdf(gdc_id, temp_path, user_info, chingsphu_info)
        if is_valid:
            return JSONResponse(status_code=200, content={"Status": "Success", "Message": "Signature verified successfully!"})
        else:
            return JSONResponse(status_code=200, content={"Status": "Error", "Message": "Signature verification failed!"})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"Status": "Error", "Message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"Status": "Error", "Message": str(e)})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
