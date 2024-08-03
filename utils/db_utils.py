from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models.models import Base, FunnelData, AdsData, Product
from utils.env_loader import get_database_url

def get_session(database_url):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()

def create_all_tables():
    engine = create_engine(get_database_url())
    Base.metadata.create_all(engine)

def upsert_funnel_data(session, data):
    for item in data:
        # Assuming `nmID` is the unique identifier
        existing = session.query(FunnelData).filter_by(nmID=item["nmID"], date=item["date"]).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            new_record = FunnelData(**item)
            session.add(new_record)
    session.commit()

def upsert_product(session, nmID, vendorCode):
    """Вставка или обновление товара."""
    product = session.query(Product).filter_by(nmID=nmID, vendorCode=vendorCode).first()
    if product is None:
        product = Product(nmID=nmID, vendorCode=vendorCode)
        session.add(product)


def upsert_ads_data(session, data):
    for item in data:
        # Assuming `adID` and `date` together are the unique identifier
        existing = session.query(AdsData).filter_by(adID=item["adID"], date=item["date"], nmID=item["nmID"]).first()
        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            new_record = AdsData(**item)
            session.add(new_record)
    session.commit()
