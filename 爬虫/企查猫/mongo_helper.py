from pymongo import MongoClient

client = MongoClient()
db = client.qichamao

def insert_company(company_dict):
    db.company.insert_one(company_dict)


