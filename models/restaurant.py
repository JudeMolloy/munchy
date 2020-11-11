from db import db

restaurant_tag = db.Table('association',
                          db.Column('restaurant_id', db.Integer,
                                    db.ForeignKey('restaurants.id'),
                                    primary_key=True),
                          db.Column('tag_id', db.Integer,
                                    db.ForeignKey('tags.id'),
                                    primary_key=True)
                          )


class RestaurantModel(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), nullable=False)
    bio = db.Column(db.String(80))

    tags = db.relationship("TagModel", secondary=restaurant_tag,
                           back_populates="restaurants")

    def __init__(self, name, bio):
        self.name = name
        self.bio = bio

    @property
    def get_tags(self):
        return self.tags.all()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), nullable=False)

    restaurants = db.relationship("RestaurantModel", secondary=restaurant_tag,
                                  back_populates="tags")

    def __init__(self, name):
        self.name = name

    @property
    def get_restaurants(self):
        return self.restaurants.all()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
