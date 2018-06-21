# Sqlalchemy JSON Querybuilder

It introduces a middleware between your application and Sqlalchemy ORM. So input to ORM can be provided in the form JSON/Objects.

## Installation

```sh
python3 -m pip install --index-url https://test.pypi.org/simple sqlalchemy-json-querybuilder
```

## Usage

```python

#-------------- Models ---------------#

def generate_uuid():
    return str(uuid4())
    
class NotificationGroup(Base):
    __tablename__ = "notification_group"

    id = Column("id", db.String(75), primary_key=True, default=generate_uuid)
    client_id = Column('client_id', db.Integer, nullable=False)
    denotation = Column('denotation', db.String(250), nullable=False)    # TODO Size, validation
    description = Column('description', db.String(500))
    customers_sites = Column('customers_sites', db.TEXT, nullable=False)
    group_mappings = relationship("NotificationGroupMapping", backref="notification_group_mapping", lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('client_id', 'denotation', name='denotation'),
    )
 
class NotificationGroupMapping(Base):
    __tablename__ = "notification_group_mapping"

    id = Column("id", db.String(75), primary_key=True, default=generate_uuid)
    notification_group_id = Column(String(75), ForeignKey('notification_group.id'))
    event_id = Column(String(75), nullable=False)
    recipient_id = Column(String(75), ForeignKey('recipient_group.id'))
    recipient = relationship("Recipient")

    is_used = Column(db.Enum(YesNo), default=YesNo.YES)

    __table_args__ = (
        UniqueConstraint('notification_group_id', 'event_id', 'recipient_id'),
    )

class Recipient(Base):
    __tablename__ = 'recipients'

    client_id = Column('client_id', Integer, nullable=False)
    user_id = Column('user_id', Integer, nullable=False)
    email = Column('email', String(256), nullable=False)

    __table_args__ = (
        # While adding an unique constraint, always make sure to include `is_deleted` column. e.g. -
        db.Index('idx_recipients_c_id_u_id_is_deleted', "client_id", "user_id", "is_deleted"),
    )
```

```python

#-------------- Query -------------#

Recursively creates and evaluates criteria. e.g. Following JSON will be translated to -

{
    "field_name": "NotificationGroup.group_mappings",
    "field_value": {
      "field_name": "NotificationGroupMapping.recipient",
      "field_value": {
        "field_name": "Recipient.email",
        "field_value": "Sam",
        "operator": "contains"
      },
      "operator": "has"
    },
    "operator": "any"
}

This query -

results = db.session.query(NotificationGroup).filter(
            NotificationGroup.group_mappings.any(
                NotificationGroupMapping.event.has(
                    Event.denotation == "Den2"
                )
          ).all()
 
```

## Examples

Examples can be found [here](https://github.com/suyash248/sqlalchemy-json-querybuilder/blob/master/examples/main.py)
