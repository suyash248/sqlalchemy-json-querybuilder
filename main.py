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
        dict(field_name='text', operator='contains', field_value='often')
    ]
    search = Search(session=session, model_cls=(Comment,), filter_by=filter_by)
    results = search.results
    print(results)

if __name__ == '__main__':
    filter()