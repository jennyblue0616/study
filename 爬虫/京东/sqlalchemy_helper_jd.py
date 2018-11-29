# 跟数据库有关

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from jdmodels import JdProduct

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1/maoyan_db?charset=utf8", max_overflow=5)
session_maker = sessionmaker(bind=engine)
session = session_maker()

def save_db(result_list):
    for item_dict in result_list:
        jd = JdProduct()
        jd.title = item_dict['title']
        jd.sku = item_dict['sku']
        jd.picture = item_dict['picture']
        jd.price = item_dict['price']
        jd.comment = item_dict['comment']
        jd.detail = item_dict['detail']
        jd.store = item_dict['store']


        session.add(jd)
        session.commit()



