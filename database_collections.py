from passlib.context import CryptContext
from fastapi import HTTPException
from database import user_collection, gdc_collection, chingsphu_collection
from models import User, GDC, ChingsPhu


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)
async def create_user(user: User):
    user_dict = user.dict()
    user_dict["_id"] = user_dict["cccd"]
    user_dict["password"] = hash_password(user_dict["password"])
    result = await user_collection.insert_one(user_dict)
    return {"_id": str(result.inserted_id)}

async def create_gdc(gdc: GDC):
    gdc_dict = gdc.dict()
    gdc_dict["_id"] = gdc_dict["gdc_Id"]

    user = await user_collection.find_one({"_id": gdc_dict["cccd"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not await chingsphu_collection.find_one({"_id": gdc_dict["CP_username"]}):
        raise HTTPException(status_code=404, detail="Chingsphu not found")
    
    if user["hadGdc"]:
        raise HTTPException(status_code=400, detail="User already has a GDC")

    await user_collection.update_one({"_id": gdc_dict["cccd"]}, {"$set": {"hadGdc": True}})
    result = await gdc_collection.insert_one(gdc_dict)
    return {"_id": str(result.inserted_id)}

async def create_chingsphu(chingsphu: ChingsPhu):
    chingsphu_dict = chingsphu.dict()
    chingsphu_dict["_id"] = chingsphu_dict["CP_username"]
    chingsphu_dict["password"] = hash_password(chingsphu_dict["password"])
    result = await chingsphu_collection.insert_one(chingsphu_dict)
    return {"_id": str(result.inserted_id)}