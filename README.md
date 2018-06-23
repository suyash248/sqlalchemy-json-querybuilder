# Sqlalchemy JSON Querybuilder

It introduces a middleware between your application and Sqlalchemy ORM. So input to ORM can be provided in the form JSON/Objects.

## Installation

```sh
pip install sqlalchemy-json-querybuilder
```

# Usage

Filter criteria -

```python

# Each criterion has 3 attributes: field_name, operator, field_value

criterion_1 = {
    'field_name': 'MyModel1.some_field',
    'operator': 'some_operator'  # Supported operators are listed below
    'field_value': 'some_value'
}

# Once all the critera are defined in the form of dictionary/object, bundle them as follows -

filter_by = {
    'and': [criterion_1, criterion_2,....criterion_n],
    'or': [other_criterion_1, other_criterion_2,....other_criterion_n]
}

# If there are `and` critera only, then they can be bundled in following 2 ways -
filter_by = [criterion_1, criterion_2,....criterion_n] 

# Alternative way to bundle `and` criteria
filter_by = {
    'and': [criterion_1, criterion_2,....criterion_n]
}

# If there are `or` critera only, then they can be bundled as -
filter_by = {
    'or': [criterion_1, criterion_2,....criterion_n]
}
```

Ordering -

```python
ordering = ['MyModel1.some_field', '-MyModel1.other_field']   # `-` sign indicates DESC order.
```

Pagination - 

Following 3 attributes are used to control pagination:

 - `page`: Current page number.
 - `per_page`: Number of records to be displayed on a page.
 - `all`: Defaults to `False`, make it `True` in order to disable the pagination and fetch all records at once.

Querying -

```python
from sqlalchemy_json_querybuilder.querybuilder.search import Search

# session - SqlAlchemy session
# 'some_module.models' - Package/module where all the models are placed.
search_obj = Search(session, 'some_module.models', (MyModel1,), filter_by=criteria, order_by=ordering, page=1, per_page=10)

# Results contains `data` & `count`
results = search_obj.results
```

## Operators

Following operators are supported - 

`equals`, `notequals`, `lt`, `lte`, `gt`, `gte`, `like`, `ilike`, `startswith`, `istartswith`, `endswith`, `iendswith`, `contains`, `icontains`, `match`, `in`, `notin`, `isnull`, `isnotnull`, `any`, `has`

> Note - `i` stands for `case insensitive`.

- #### equals

```python
filter_by = [dict(field_name='User.name', field_value='ed', operator='equals')]
```
is translated to

```python
query.filter(User.name == 'ed')
```

- #### notequals

```python
filter_by = [dict(field_name='User.name', field_value='ed', operator='notequals')]
```
is translated to

```python
query.filter(User.name != 'ed')
```

- #### lt

```python
filter_by = [dict(field_name='User.age', field_value=18, operator='lt')]
```
is translated to

```python
query.filter(User.name < 18)
```

- #### lte

```python
filter_by = [dict(field_name='User.age', field_value=18, operator='lte')]
```
is translated to

```python
query.filter(User.name <= 18)
```

- #### gt

```python
filter_by = [dict(field_name='User.age', field_value=18, operator='gt')]
```
is translated to

```python
query.filter(User.name > 18)
```

- #### gte

```python
filter_by = [dict(field_name='User.age', field_value=18, operator='gte')]
```
is translated to

```python
query.filter(User.name >= 18)
```

- #### in

```python
filter_by = [dict(field_name='User.name', field_value=['ed', 'wendy', 'jack'], operator='in')]
```
is translated to

```python
query.filter(User.name.in_(['ed', 'wendy', 'jack']))
```

- #### notin

```python
filter_by = [dict(field_name='User.name', field_value=['ed', 'wendy', 'jack'], operator='notin')]
```
is translated to

```python
query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
```

- #### isnull

```python
filter_by = [dict(field_name='User.name', field_value=null, operator='isnull')]
```
is translated to

```python
query.filter(User.name == None)

# alternatively, if pep8/linters are a concern
query.filter(User.name.is_(None))
```

- #### isnotnull

```python
filter_by = [dict(field_name='User.name', field_value=null, operator='isnotnull')]
```

is translated to

```python
query.filter(User.name != None)

# alternatively, if pep8/linters are a concern
query.filter(User.name.isnot(None))
```

- #### contains

```python
filter_by = [dict(field_name='User.name', field_value='ed', operator='contains')]
```
is translated to

```python
query.filter(User.name.like('%ed%'))
```

- #### startswith

```python
filter_by = [dict(field_name='User.name', field_value='ed', operator='startswith')]
```
is translated to

```python
query.filter(User.name.like('ed%'))
```

- #### endswith

```python
filter_by = [dict(field_name='User.name', field_value='ed', operator='endswith')]
```
is translated to

```python
query.filter(User.name.like('%ed'))
```

- #### match

```python
filter_by = [dict(field_name='User.name', field_value='wendy', operator='match')]
```
is translated to

```python
query.filter(User.name.match('wendy'))
```

- #### any

```python
filter_by = [{
    'field_name': 'User.addresses',
    'operator': 'any',
    'field_value': {
        'field_name': 'Address.email_address',
        'operator': 'equals',
        'field_value': 'bar'
    }
}]
```
is translated to

```python
query.filter(User.addresses.any(Address.email_address == 'bar'))

# also takes keyword arguments:
query.filter(User.addresses.any(email_address='bar'))
```

- #### has

```python
filter_by = [{
    'field_name': 'Address.user',
    'operator': 'has',
    'field_value': {
        'field_name': 'User.name',
        'operator': 'equals',
        'field_value': 'bar'
    }
}]
```
is translated to

```python
query.filter(Address.user.has(name='ed'))
```

## Examples

Some examples are given below. Mote examples can be found [here](https://github.com/suyash248/sqlalchemy-json-querybuilder/blob/master/examples/main.py).


```python

#-------------- Creating connection & session ---------------#

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

# `filter_by` can have multiple criteria objects bundled as a list.
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

# `order_by` can have multiple column names. `-` indicates arranging the results in `DESC` order.
order_by = ['-NotificationGroup.client_id']

# returns `results` dict containing `data` & `count`
results = Search(session, "models.notification_group", (NotificationGroup,), 
                filter_by=filter_by, order_by=order_by, page=1, per_page=5).results

# Above code snippet is equivalent to

results = session.query(NotificationGroup).filter(
            NotificationGroup.group_mappings.any(
                NotificationGroupMapping.recipient.has(
                    Recipient.email=='Sam@gmail.com'
                )
            )
          ).all()
 
```

## References
- [Relationship operators](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-relationship-operators)
- [Filter operators](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-filter-operators)
