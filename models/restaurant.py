from db import db

restaurant_tag = db.Table('restaurant_tag_association',
                          db.Column('restaurant_id', db.Integer,
                                    db.ForeignKey('restaurants.id'),
                                    primary_key=True),
                          db.Column('tag_id', db.Integer,
                                    db.ForeignKey('tags.id'),
                                    primary_key=True)
                          )

restaurant_clip = db.Table('restaurant_clip_association',
                           db.Column('restaurant_id', db.Integer,
                                     db.ForeignKey('restaurants.id'),
                                     primary_key=True),
                           db.Column('clip_id', db.Integer,
                                     db.ForeignKey('clips.id'),
                                     primary_key=True)
                           )


class RestaurantModel(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    bio = db.Column(db.String)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    profile_image_url = db.Column(db.String)

    relevance = db.relationship('RelevanceModel', backref='restaurants', lazy="dynamic", cascade="all, delete-orphan")

    tags = db.relationship("TagModel", secondary=restaurant_tag,
                           back_populates="restaurants")

    clips = db.relationship("ClipModel", secondary=restaurant_clip,
                            back_populates="restaurants")

    def __init__(self, name, bio, latitude, longitude, profile_image_url):
        self.name = name
        self.bio = bio
        self.latitude = latitude
        self.longitude = longitude
        self.profile_image_url = profile_image_url

    def __repr__(self):
        return self.name

    @property
    def get_tags(self):
        print(self.tags)
        return self.tags.all()

    @property
    def get_clips(self):
        return self.clips.all()

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
    name = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=False)

    restaurants = db.relationship("RestaurantModel", secondary=restaurant_tag,
                                  back_populates="tags")

    def __init__(self, name, icon):
        self.name = name
        self.icon = icon

    def __repr__(self):
        return self.name

    @property
    def get_restaurants(self):
        return self.restaurants.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ClipModel(db.Model):
    __tablename__ = "clips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    video_url = db.Column(db.String, nullable=False)

    restaurants = db.relationship("RestaurantModel", secondary=restaurant_clip,
                                  back_populates="clips")

    clip_data = db.relationship('ClipDataModel', backref='clips', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, title, description, video_url):
        self.title = title
        self.description = description
        self.video_url = video_url

    def __repr__(self):
        return self.title

    @property
    def get_restaurants(self):
        return self.restaurants.all()

    @property
    def get_views(self):
        pass

    @property
    def get_likes(self):
        pass

    @property
    def get_share_clicks(self):
        pass

    @property
    def get_order_clicks(self):
        pass

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
