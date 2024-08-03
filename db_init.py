from db_models import Base, setup_db

def create_tables():
    engine, _ = setup_db()
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
