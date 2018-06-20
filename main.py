from examples.models import *
from querybuilder.search import Search

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
    image_another_car = Image(uuid='uuid_anothercar', tags=[tag_car])
    image_rhino = Image(uuid='uuid_rhino', tags=[tag_animal], comments=[comment_rhino])

    session.add(tag_cool)
    session.add(tag_car)
    session.add(tag_animal)

    session.add(comment_rhino)

    session.add(image_car)
    session.add(image_another_car)
    session.add(image_rhino)

    # Commit the changes:
    session.commit()

def filter():
    filter_by = [
        {
            "field_name": "Image.tags",
            "field_value": {
                "field_name": "Tag.name",
                "field_value":["cool"],
                "operator": "in"
            },
            "operator": "any"
        }
    ]
    order_by = ['-Image.uuid']

    search = Search(session, 'examples.models', (Image,), filter_by=filter_by, order_by=order_by)
    results = search.results
    print("Found {} record(s)".format(results['count']))
    for r in results['data']:
        print(r)

if __name__ == '__main__':
    filter()