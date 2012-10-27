from datetime import datetime

from restler import decorators
from sqlalchemy.ext.declarative import declarative_base

# Less common types
from sqlalchemy import Enum
# Currently unsupported types
from sqlalchemy import Interval, PickleType

# Standard/Generic Types
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Time,
    Float,
    Text,
    Binary
)

# More specific variants of the standard types
from sqlalchemy import (
    BigInteger,
    SmallInteger,
    Unicode,
    UnicodeText,
    LargeBinary,
    Numeric
)

# SQL Types
from sqlalchemy import (
    BIGINT,
    BINARY,
    BLOB,
    BOOLEAN,
    CHAR,
    CLOB,
    DATE,
    DATETIME,
    DECIMAL,
    FLOAT,
    INT,
    INTEGER,
    NCHAR,
    NVARCHAR,
    NUMERIC,
    REAL,
    SMALLINT,
    TEXT,
    TIME,
    TIMESTAMP,
    VARBINARY,
    VARCHAR
)

Base = declarative_base()

DATETIME_NOW = datetime.now()
TIME_NOW = DATETIME_NOW.time()
FLOAT_NUM = 1.01
A_STRING = "some string"
A_BINARY = '\xff\xd8\xff\xe1A\xecExif'


@decorators.sqlalchemy_serializer
class Model1(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    field2 = Column(String(1000), default=A_STRING)
    field3 = Column(Boolean, default=False)
    field4 = Column(Date, default=DATETIME_NOW)
    field5 = Column(DateTime, default=DATETIME_NOW)
    field6 = Column(Time, default=TIME_NOW)
    field7 = Column(Float, default=FLOAT_NUM)
    field8 = Column(Text, default=A_STRING)
    #field9 = Column(Binary, default=A_BINARY)
    interval = Column(Interval)
    pickle_type = Column(PickleType)
