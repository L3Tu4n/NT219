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

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginForm(BaseModel):
    username: str
    password: str

@app.post("/signup/")
async def signup(user: User):
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
        return JSONResponse(status_code=200, content={"Status": "Error", "Message": str(e)})

@app.post("/sign")
async def sign(file: UploadFile = File(...), cccd: str = Form(...), CP_username: str = Form(...), start_place: str = Form(...), destination_place: str = Form(...), token: str = Depends(oauth2_scheme)):
    try:
        user_info = decode_access_token(token)
        if user_info is None or user_info["type"] != "chingsphu":
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
async def verify(file: UploadFile = File(...), gdc_id: str = Form(...), token: str = Depends(oauth2_scheme)):
    try:
        user_info = decode_access_token(token)
        if user_info is None or user_info["type"] != "chingsphu":
            raise HTTPException(status_code=401, detail="Not authorized")
        
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
