from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

class Product(Base):
    __tablename__ = 'product'

    nmID = Column(Integer, primary_key=True)
    vendorCode = Column(String, nullable=False)

    # Отношение один-ко-многим с FunnelData и AdsData
    funnels = relationship('FunnelData', backref='product')
    ads = relationship('AdsData', backref='product')

class FunnelData(Base):
    __tablename__ = 'funnel'
    id = Column(Integer, primary_key=True)
    nmID = Column(Integer, ForeignKey('product.nmID'), nullable=False)
    date = Column(Date, nullable=False)
    owner = Column(String)
    vendorCode = Column(String)
    productType = Column(String)
    brandName = Column(String)
    openCardCount = Column(Integer)
    addToCartCount = Column(Integer)
    ordersCount = Column(Integer)
    ordersSumRub = Column(Float)
    buyoutsCount = Column(Integer)
    buyoutsSumRub = Column(Float)
    cancelCount = Column(Integer)
    cancelSumRub = Column(Float)
    avgPriceRub = Column(Float)
    avgOrdersCountPerDay = Column(Float)
    addToCartPercent = Column(Float)
    cartToOrderPercent = Column(Float)
    buyoutsPercent = Column(Float)
    stocksMp = Column(Integer)
    stocksWb = Column(Integer)

    __table_args__ = (
        UniqueConstraint('nmID', 'date', name='unique_nmid_date'),
    )

class AdsData(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True)
    adID = Column(Integer, nullable=False)
    nmID = Column(Integer, ForeignKey('product.nmID'), nullable=False)
    date = Column(Date, nullable=False)
    productName = Column(String)
    status = Column(Integer)
    views = Column(Integer)
    clicks = Column(Integer)
    ctr = Column(Float)
    cpc = Column(Float)
    sum = Column(Float)
    atbs = Column(Integer)
    orders = Column(Integer)
    cr = Column(Integer)
    shks = Column(Integer)
    sum_price = Column(Float)

    __table_args__ = (
        UniqueConstraint('nmID', 'adID', 'date', name='unique_nmid_adid_date'),
    )

def setup_db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return engine, Session
