from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Enum
from src.core.config import Base
from src.db.schemas.bagage_schemas import BagageType

class Bagage(Base):
    __tablename__ = 'Bagages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    bagage_type = Column(Enum("petit", "moyen", "grand", name="bagage_type_enum"), nullable=False)
    timestamp = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    position = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    