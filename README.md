# Sqlalchemy JSON Querybuilder

It introduces a middleware between your application and Sqlalchemy ORM. So input to ORM can be provided in the form JSON/Objects.

## Installation

```sh
python3 -m pip install --index-url https://test.pypi.org/simple sqlalchemy-json-querybuilder
```

## Usage

```python

#-------------- Creating connection & sessison ---------------#

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
con_url = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(
    username='root', password='', host='localhost', port=3306, database='test'
)
engine = create_engine(con_url, pool_recycle=3600)

# Set up the session
session_maker = sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)
session = scoped_session(session_maker)

#-------------- Models ---------------#

from uuid import uuid4
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid4())
    
class NotificationGroup(Base):
    __tablename__ = "notification_group"

    id = Column("id", String(75), primary_key=True, default=generate_uuid)
    client_id = Column('client_id', Integer, nullable=False)
    denotation = Column('denotation', String(250), nullable=False) 
    description = Column('description', String(500))
    customers_sites = Column('customers_sites', Text, nullable=False)
    group_mappings = relationship("NotificationGroupMapping", backref="notification_group_mapping", lazy='dynamic')
 
class NotificationGroupMapping(Base):
    __tablename__ = "notification_group_mapping"

    id = Column("id", String(75), primary_key=True, default=generate_uuid)
    notification_group_id = Column(String(75), ForeignKey('notification_group.id'))
    event_id = Column(String(75), nullable=False)
    recipient_id = Column(String(75), ForeignKey('recipient_group.id'))
    recipient = relationship("Recipient")
    is_used = Column(String(75), nullable=False)

class Recipient(Base):
    __tablename__ = 'recipients'

    client_id = Column('client_id', Integer, nullable=False)
    user_id = Column('user_id', Integer, nullable=False)
    email = Column('email', String(256), nullable=False)

#-------------- Query -------------#
from sqlalchemy_json_querybuilder.querybuilder.search import Search

filter_by = [{
    "field_name": "NotificationGroup.group_mappings",
    "field_value": {
      "field_name": "NotificationGroupMapping.recipient",
      "field_value": {
        "field_name": "Recipient.email",
        "field_value": "Sam@gmail.com",
        "operator": "equals"
      },
      "operator": "has"
    },
    "operator": "any"
}]

order_by = ['-NotificationGroup.client_id']

results = Search(session, "models.notification_group", (NotificationGroup,), filter_by=filter_by, order_by=order_by)

> Above code snippet is equivalent to

results = session.query(NotificationGroup).filter(
            NotificationGroup.group_mappings.any(
                NotificationGroupMapping.recipient.has(
                    Recipient.email=='Sam@gmail.com'
                )
            )
          ).all()
 
```

## Examples

Examples can be found [here](https://github.com/suyash248/sqlalchemy-json-querybuilder/blob/master/examples/main.py)
