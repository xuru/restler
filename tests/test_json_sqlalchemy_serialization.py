
import json
import unittest

from datetime import datetime, time
from restler.serializers import ModelStrategy, to_json, SKIP
from restler import decorators

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Standard/Generic Types
from sqlalchemy import  Column,\
    Integer,\
    String,\
    Boolean,\
    Date,\
    DateTime,\
    Time,\
    Float,\
    Text,\
    Binary

# More specific variants of the standard types
from sqlalchemy import\
    BigInteger,\
    SmallInteger,\
    Unicode,\
    UnicodeText,\
    LargeBinary,\
    Numeric

# Less common types
from sqlalchemy import Enum

# SQL Types
from sqlalchemy import\
    BIGINT,\
    BINARY,\
    BLOB,\
    BOOLEAN,\
    CHAR,\
    CLOB,\
    DATE,\
    DATETIME,\
    DECIMAL,\
    FLOAT,\
    INT,\
    INTEGER,\
    NCHAR,\
    NVARCHAR,\
    NUMERIC,\
    REAL,\
    SMALLINT,\
    TEXT,\
    TIME,\
    TIMESTAMP,\
    VARBINARY,\
    VARCHAR

# Currently unsupported types
from sqlalchemy import \
    Interval,\
    PickleType

# SchemaType - Only in SqlAlchemy .8x

Base = declarative_base()

DATETIME_NOW = datetime.now()
TIME_NOW = DATETIME_NOW.time()
FLOAT_NUM = 1.01
A_STRING = "some string"
A_BINARY = '\xff\xd8\xff\xe1A\xecExif'

@decorators.sqlalchemy_serializer
class Model1(Base):
    __tablename__ = 'test'

    id =  Column(Integer, primary_key=True)
    field2 = Column(String(1000), default=A_STRING)
    field3 = Column(Boolean, default=False)
    field4 = Column(Date, default=DATETIME_NOW)
    field5 = Column(DateTime, default=DATETIME_NOW)
    field6 = Column(Time, default=TIME_NOW)
    field7 = Column(Float, default=FLOAT_NUM)
    field8 = Column(Text, default=A_STRING )
    #field9 = Column(Binary, default=A_BINARY)

def flip(*args, **kwargs):
    return json.loads(to_json(*args, **kwargs))

class TestJsonSerialization(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model1 = Model1()
        self.session.add(self.model1)


    def test_simple(self):
        ss = ModelStrategy(Model1, include_all_fields=True)
        sj = json.loads(to_json(self.session.query(Model1).all(), ss))
        self.assertEqual(sj[0]['field2'], A_STRING)
        self.assertEqual(sj[0]['id'], 1)
        #ss = ss.include(aggregate=lambda o: '%s, %s' % (o.field2, o.field4))
        #sj = json.loads(to_json(Model1.objects.all(), ss))
        #self.assertEqual(sj[0]['aggregate'], u'1, 2')


"""
<Insert Brian's Tests Here/>
"""





