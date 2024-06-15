from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class Batik(Base):
    __tablename__ = 'batik'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    image_name: Mapped[str] = mapped_column(String)
    # numeric
    treshold: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)
    batik_stores = relationship("BatikStores", back_populates="batik")

    def __repr__(self):
        return f"Batik(id={self.id}, name={self.name}, image={self.image}, description={self.description})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "description": self.description
        }

class BatikStores(Base):
    __tablename__ = 'batik_stores'

    id: Mapped[int] = mapped_column(primary_key=True)
    batik_id : Mapped[int] = mapped_column(ForeignKey("batik.id"))
    store_id : Mapped[int] = mapped_column(ForeignKey("stores.id"))

    batik = relationship("Batik", back_populates="batik_stores")
    store = relationship("Stores", back_populates="batik_stores")


class Stores(Base):
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    instagram: Mapped[str] = mapped_column(String)
    tokopedia: Mapped[str] = mapped_column(String)
    tiktok: Mapped[str] = mapped_column(String)

    batik_stores = relationship("BatikStores", back_populates="store")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "instagram": self.instagram,
            "tokopedia": self.tokopedia,
            "tiktok": self.tiktok
        }

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    