from fastapi import FastAPI, HTTPException
from database.client import *


app = FastAPI()



@app.post("/keys")
async def create_or_update_key(keys: dict):
    print(keys)
    mac_address = keys.get('mac_address')
    
    if not mac_address:
        raise HTTPException(status_code=400, detail="mac_address is required")
    
    existing_document = keys_collection.find_one({"mac_address": mac_address})
    
    if existing_document:
        # Obtener los elementos existentes y añadir los nuevos elementos
        existing_elements = existing_document.get('keys', [])
        new_elements = keys.get('keys', [])
        updated_elements = existing_elements + new_elements
        keys_collection.update_one(
            {"mac_address": mac_address}, 
            {"$set": {"keys": updated_elements}}
        )
    else:
        keys_collection.insert_one(keys)
    
    return keys

@app.get("/keys/{mac_address}")
def getKeysByMacAddress(mac_address: str):
    print(mac_address)
    # replace - with : in mac_address
    mac_address = mac_address.replace("-", ":")
    print(mac_address)
    keys = keys_collection.find_one({"mac_address": mac_address})

    if not keys:
        raise HTTPException(status_code=404, detail="Keys not found")
    
    # keys is a dictionary, we need to convert it to JSON
    keys["_id"] = str(keys["_id"])
    
    return keys 