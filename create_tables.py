from backend.database import engine, Base
import backend.models as models

Base.metadata.create_all(bind=engine)