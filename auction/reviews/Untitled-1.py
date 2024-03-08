            <div class="col-md-6">
                <h4 class="mb-4">Leave a review</h4>
                <div class="d-flex my-3" id="ratingStars">
                    <p class="mb-0 mr-2">Your Rating * :</p>
                    <div class="text-primary">
                        <i class="bi bi-star" data-value="1"></i>
                        <i class="bi bi-star" data-value="2"></i>
                        <i class="bi bi-star" data-value="3"></i>
                        <i class="bi bi-star" data-value="4"></i>
                        <i class="bi bi-star" data-value="5"></i>
                    </div>
                </div>
                <form>
                    <div class="form-group">
                        <label for="message">Your Review *</label>
                        <textarea id="message" cols="30" rows="5" class="form-control"></textarea>
                    </div>
                    <div class="form-group mb-0">
                        <input type="hidden" id="selectedRating" name="selectedRating">
                        <input type="submit" value="Leave Your Review" class="btn btn-primary px-3">
                    </div>
                </form>
            </div>
class SellerReview(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


@login_required
def seller_review(request, username):
seller = get_object_or_404(User, username=username)
reviewer = get_object_or_404(User, email=request.user)
seller_reviews = SellerReview.objects.filter(seller=seller)
if request.method == 'POST':
rating = request.data.get("rating")
feedback = request.data.get("feedback")
print(feedback)
context = {
'reviews': seller_reviews,
}
return render(request, 'reviews/seller_review.html', context)

use fetch api to make a post request for feedback.