from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Organ(Base):
    __tablename__ = 'organ'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    medicine = relationship('Medicine', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'user_id': self.user_id
        }


class Medicine(Base):
    __tablename__ = 'medicine'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    type = Column(String(250))
    gland = Column(String(250))
    organ_id = Column(Integer, ForeignKey('organ.id'))
    organ = relationship(Organ)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'type': self.type,
            'gland': self.gland,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'user_id': self.user_id
        }


engine = create_engine('sqlite:///roadmaptohealthwithusers.db')
Base.metadata.create_all(engine)
