from fastapi import FastAPI
from models import User, GDC, ChingsPhu
from database import user_collection, gdc_collection, chingsphu_collection

app = FastAPI()

# To run the server, run this command in the terminal:
# uvicorn main:app --reload

@app.get("/")
def read_root():
    return {"Message": "Nothing here!"}

@app.post("/users/")
async def create_user(user: User):
    user_dict = user.dict()
    user_dict["_id"] = user_dict["cccd"]
    result = await user_collection.insert_one(user_dict)
    return {"_id": str(result.inserted_id)}

@app.post("/gdc/")
async def create_gdc(gdc: GDC):
    gdc_dict = gdc.dict()
    gdc_dict["_id"] = gdc_dict["gdc_Id"]

    if not await user_collection.find_one({"_id": gdc_dict["cccd"]}):
        return {"error": "User not found"}
    if not await chingsphu_collection.find_one({"_id": gdc_dict["CP_username"]}):
        return {"error": "Chings phủ not found"}

    result = await gdc_collection.insert_one(gdc_dict)
    return {"_id": str(result.inserted_id)}

@app.post("/chingsphu/")
async def create_chingsphu(chingsphu: ChingsPhu):
    chingsphu_dict = chingsphu.dict()
    chingsphu_dict["_id"] = chingsphu_dict["CP_username"]
    result = await chingsphu_collection.insert_one(chingsphu_dict)
    return {"_id": str(result.inserted_id)}
