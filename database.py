from motor.motor_asyncio import AsyncIOMotorClient

database_name = "ToiDaFakeHon250kgdc"
user_collection_name = "users"
gdc_collection_name = "gdc"
chingsphu_collection_name = "chingsphu"

client = AsyncIOMotorClient('mongodb+srv://coldboykiller:OJXwyzcZgRdGyhSN@falcontest.e2de0nb.mongodb.net/?retryWrites=true&w=majority&appName=FalconTest')

database = client[database_name]
user_collection = database[user_collection_name]
gdc_collection = database[gdc_collection_name]
chingsphu_collection = database[chingsphu_collection_name]