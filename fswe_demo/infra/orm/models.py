from sqlalchemy import Column, Float, Integer, String

from fswe_demo.infra.db.get_conn import Base


class PopularItem(Base):
    __tablename__ = "popular_items"

    product_asin = Column(String, primary_key=True, index=True)
    size = Column(Integer, nullable=False)
    prob = Column(Float, nullable=False)
