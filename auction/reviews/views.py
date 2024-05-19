from django.shortcuts import render, redirect, get_object_or_404
from reviews.models import SellerReview
from payment.models import Transaction
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count
from collections import OrderedDict

User=get_user_model()

# Handling review to seller
@login_required
def seller_review(request, username):
    seller = get_object_or_404(User, username=username)
    reviewer = get_object_or_404(User, email=request.user)
    try:
        seller_reviews = SellerReview.objects.filter(seller=seller)
        average_rating = seller_reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating, 1) if average_rating is not None else 0.0

        # percentage of each star rating
        rating_counts = seller_reviews.values('rating').annotate(count=Count('rating'))
        total_reviews = seller_reviews.count()
        star_ratings = {i: 0 for i in range(1, 6)}
        for rating_count in rating_counts:
            star_ratings[rating_count['rating']] = rating_count['count'] / total_reviews * 100

        star_ratings_ordered = OrderedDict(sorted(star_ratings.items(), reverse=True))
        
        # only a user who has purchased a lot from the seller can give a review
        has_transaction = Transaction.objects.filter(lot__seller=seller, buyer=reviewer).exists()
        print(has_transaction)
        if request.method == 'POST':
            reviewer = request.user
            seller = User.objects.get(username=username)
            rating = request.POST.get('rating')
            feedback = request.POST.get('feedback')
            print(username, feedback, rating)
            try:
                review = SellerReview.objects.create(reviewer=reviewer, seller=seller, rating=rating, feedback=feedback)
                return JsonResponse({'message': 'Review submitted successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'error': 'Invalid request method'}, status=400)
            
        context = {
            'seller': seller,
            'reviews': seller_reviews,
            'average_rating': average_rating,
            'star_ratings': star_ratings_ordered,
            'has_transaction': has_transaction,
        }
        return render(request, 'reviews/seller_review.html', context)
    except Exception as e:
        print(e)
