from pymongo import MongoClient
from bson import ObjectId

def add_components_from_parsed_bom(db, dict):
        for k, v in dict.items():
            print(k, v)
            collection = db[k]
            for i in v:
                if collection.find_one({"mpn":i["mpn"]}):
                    collection.update_one(
                        {"mpn": i["mpn"]},
                        {"$inc": {"qty": i["qty"]}},
                        upsert=True
                    )
                    pass
                else:
                    collection.insert_one(i)


def get_all_components(db):
    return_list = {}
    for i in db.list_collection_names():
        components = list(db[i].find({}))
        return_list[i] = convert_objectid_to_str(components)
    return return_list

def get_components_by_type(db, type):
    return convert_objectid_to_str(list(db[type].find({})))

def get_components_by_mpn(db, mpn):
    for index, val in enumerate(db.list_collection_names()):
        c = list(db[val].find({"mpn": mpn}))
        if c:
            convert_objectid_to_str(c)
    return {"message": "Component not found"}

def change_component_qty(db, type, mpn, qty):
    try:
        db[type].update_one({"mpn": mpn}, {"$set": {"qty": qty}})
    except:
        return {"message": "Component not found"}
    return {"message:": "Component updated"}

def add_component(db, type, component):
    try:
        db[type].insert_one(component)
        return True
    except:
        return False

def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


def db_find_from_str(db, str):
    return_array = []
    for i in db.list_collection_names():
        c = list(db[i].find({"$text": {"$search": str}}))
        if c:
            return_array.append(c)
    return convert_objectid_to_str(return_array)