from models import db
from models.review import Review
from flask_jwt_extended import get_jwt_identity

# CREATE
def create_review(data):
    new_review = Review(
         title=data['title'],
        rating=data.get('rating'),
        content=data['content'],
        user_id=int(get_jwt_identity()),
        travel_id=data['travel_id']
    )
    db.session.add(new_review)
    db.session.commit()
    return {'message': 'Review created successfully',"status":201, 'data': new_review.to_dict()}

# GET ALL
def get_all_reviews():
    reviews = Review.query.all()
    return {"message":"getting all reviews","status":201,'data': [review.toDic() for review in reviews]}

# GET ONE
def get_review(review_id):
    review = Review.query.get(review_id)
    if review:
        return {"message":"getting review","status":201,'data':review.toDic()}
    return {'message': 'Review not found',"status":404}

# UPDATE
def update_review(review_id, data):
    review = Review.query.get(review_id)
    if review:
        review.rating = data.get('rating', review.rating)
        review.comment = data.get('comment', review.comment)
        db.session.commit()
        return {'message': 'Review updated successfully',"status":200, 'data': review.toDic()}
    return {'message': 'Review not found',"status":404}

# DELETE
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully',"status":200}
    return {'message': 'Review not found',"status":404}
