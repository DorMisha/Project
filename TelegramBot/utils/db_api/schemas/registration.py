from sqlalchemy import Column, BigInteger, String, sql, Float

from utils.db_api.db_gino import TimedBaseModel


class Registration(TimedBaseModel):
    __tablename__ = 'registrations'
    user_id = Column(BigInteger, primary_key=True)
    tg_first_name = Column(String(50))
    tg_last_name = Column(String(50))
    name = Column(String(50))
    phone = Column(String(20))
    age = Column(String(4))
    status = Column(String(25))

    query: sql.select