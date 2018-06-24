from src.examples.models import Tag, Comment, Image
from lib.sqlalchemy_json_querybuilder.querybuilder.search import Search
from src.examples.connector import session
from datetime import datetime, timedelta

# Package/module containing all sqlalchemy model classes.
models_module = 'src.examples.models'

def populate_db():
    # ----------------------------
    # Populate the database
    # ----------------------------

    # Tags
    tag_cool = Tag(name='cool')
    tag_car = Tag(name='car')
    tag_animal = Tag(name='animal')

    # Comment
    comment_rhino = Comment(text='Rhinoceros, often abbreviated as rhino, is a group of five extant '
                                 'species of odd-toed ungulates in the family Rhinocerotidae.')

    # Images
    image_car = Image(uuid='uuid_car', tags=[tag_car, tag_cool], created_at=(datetime.utcnow() - timedelta(days=1)))
    image_another_car = Image(uuid='uuid_anothercar', tags=[tag_car], likes=2)
    image_rhino = Image(uuid='uuid_rhino', tags=[tag_animal], comments=[comment_rhino], likes=7)

    session.add(tag_cool)
    session.add(tag_car)
    session.add(tag_animal)

    session.add(comment_rhino)

    session.add(image_car)
    session.add(image_another_car)
    session.add(image_rhino)

    # Commit the changes:
    session.commit()

def filter_and():
    criterion1 = {
        "field_name": "Image.tags",
        "field_value": {
            "field_name": "Tag.name",
            "field_value":["cool"],
            "operator": "in"
        },
        "operator": "any"
    }
    criterion2 = {
        'field_name': 'Image.uuid',
        'operator': 'contains',
        'field_value': 'car'
    }
    filter_by = [criterion1, criterion2] # is equivalent to {'and': [criterion1, criterion2] }
    order_by = ['-Image.uuid']

    search = Search(session, models_module, (Image,), filter_by=filter_by, order_by=order_by)
    results = search.results
    print("Found {} record(s)".format(results['count']))
    for k, v in results.items():
        print('{}: {}'.format(k, v))

def filter_or():
    criterion1 = {
        "field_name": "Image.tags",
        "field_value": {
            "field_name": "Tag.name",
            "field_value":["cool"],
            "operator": "in"
        },
        "operator": "any"
    }
    criterion2 = {
        'field_name': 'Image.likes',
        'operator': '>',
        'field_value': 5
    }
    filter_by = {'or': [criterion1, criterion2] }
    order_by = ['-Image.uuid']

    search = Search(session, models_module, (Image,),
                    filter_by=filter_by, order_by=order_by, page=1, per_page=5)
    results = search.results
    print("Found {} record(s)".format(results['count']))
    for k, v in results.items():
        print('{}: {}'.format(k, v))

def filter_and_or():
    criterion1 = {
        "field_name": "Image.tags",
        "field_value": {
            "field_name": "Tag.name",
            "field_value": ["cool"],
            "operator": "in"
        },
        "operator": "any"
    }
    criterion2 = {
        'field_name': 'Image.uuid',
        'operator': 'contains',
        'field_value': 'car'
    }
    criterion3 = {
        'field_name': 'Image.created_at',
        'operator': '>',
        'field_value': datetime(2018, 6, 23)
    }

    # Note - and_expressions & or_expressions are glued via AND operator i.e. (all_and_exprs) AND (all_or_exprs)
    # SELECT field1, field2..fieldN FROM some_table WHERE
    #               (and_expr1 AND and_expr2 AND and_exprN)
    #                             AND
    #               (or_exp1 OR or_expr2 OR or_exprN)
    filter_by = {
        'and': [criterion3],
        'or': [criterion1, criterion2]
    }
    order_by = ['-Image.uuid']

    search = Search(session, models_module, (Image,),
                    filter_by=filter_by, order_by=order_by, page=1, per_page=5)
    results = search.results
    print("Found {} record(s)".format(results['count']))
    for k, v in results.items():
        print('{}: {}'.format(k, v))

if __name__ == '__main__':
    print('\n---------------- Demonstrating AND condition ----------------\n')
    filter_and()

    print('\n---------------- Demonstrating OR condition ----------------\n')
    filter_or()

    print('\n---------------- Demonstrating AND & OR condition ----------------\n')
    filter_and_or()

    # OUTPUT -

    # ---------------- Demonstrating AND condition ----------------
    # Found 1 record(s)
    # data: [<Image (uuid=uuid_car, likes=0, created_at=2018-06-22 14:15:59)>]
    # count: 1
    #
    # ---------------- Demonstrating OR condition ----------------
    #
    # Found 2 record(s)
    # data: [<Image (uuid=uuid_rhino, likes=7, created_at=2018-06-23 14:15:59)>, <Image (uuid=uuid_car, likes=0, created_at=2018-06-22 14:15:59)>]
    # count: 2
    #
    # ---------------- Demonstrating AND & OR condition ----------------
    #
    # Found 1 record(s)
    # data: [<Image (uuid=uuid_anothercar, likes=2, created_at=2018-06-23 14:15:59)>]
    # count: 1
