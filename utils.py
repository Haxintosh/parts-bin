from pymongo import MongoClient

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
        return_list[i] = list(db[i].find({}))
    return return_list

def get_components_by_type(db, type):
    return list(db[type].find({}))

def get_components_by_mpn(db, mpn):
    return list(db.find({"mpn": mpn}))

def change_component_qty(db, type, mpn, qty):
    try:
        db[type].update_one({"mpn": mpn}, {"$set": {"qty": qty}})
    except:
        return False
    return True

def add_component(db, type, component):
    try:
        db[type].insert_one(component)
        return True
    except:
        return False
