from flask import Blueprint, render_template
foodReviewz = Blueprint('foodReviewz',__name__)

@foodReviewz.route("/foodReviews")
def foodReviews():
    return render_template('foodReviews.html')
