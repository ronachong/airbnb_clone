from base import *
from user import User

class Review(BaseModel):
    message = peewee.TextField(null=False)
    stars = peewee.IntegerField(default=0)
    user = peewee.ForeignKeyField(User, related_name="reviews", on_delete='cascade')

    def to_hash(self):
        from review_user import ReviewUser
        from review_place import ReviewPlace

        hash = {}
        hash["id"] = self.id
        hash["created_at"] = self.created_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["updated_at"] = self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        hash["message"] = self.message
        hash["stars"] = self.stars
        hash["from_user_id"] = self.user.id

        try:
            review_user = ReviewUser.get(ReviewUser.review == self.id)
            print "the get record worked"
            #hash["to_user_id"] = review_user.user.id
            hash["to_user_id"] = 10
            print "the setting of to_user_id worked"
        except:
            print "an exception arose, got caught"
            hash["to_user_id"] = None

        try:
            review_place = ReviewPlace.get(ReviewPlace.review == self.id)
            print "the get record worked"
            #hash["to_place_id"] = review_place.place.id
            hash["to_place_id"] = 10
            print "the setting of to_place_id worked"
        except:
            print "an exception arose, got caught"
            hash["to_place_id"] = None

        return hash
