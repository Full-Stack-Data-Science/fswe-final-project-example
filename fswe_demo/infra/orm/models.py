from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from fswe_demo.infra.db.get_conn import Base


class PopularItemTable(Base):
    __tablename__ = "popular_items"

    product_asin = Column(String, primary_key=True, index=True)
    size = Column(Integer, nullable=False)
    prob = Column(Float, nullable=False)


class FPGrowthRecommendationTable(Base):
    __tablename__ = "fpgrowth_product_recommendations"

    product_asin = Column(String, primary_key=True)
    recommendations = Column(JSONB, nullable=False)
