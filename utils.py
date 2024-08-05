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