from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/maoyan_db?charset=utf8", max_overflow=5,encoding='utf-8')
Base = declarative_base()


class JdProduct(Base):
    __tablename__ = 'jd_product'
    id = Column(Integer, primary_key=True, autoincrement=True)    #主键，自增
    title = Column(String(512))
    sku = Column(String(128))
    picture = Column(String(1024))
    price = Column(String(128))
    comment = Column(String(1024))
    detail = Column(String(1024))
    store = Column(String(128))





