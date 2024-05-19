from django.shortcuts import render
from auctionapp.models import *
from django.shortcuts import render
from lot.models import Category, Lot
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField


def index(request):
    try:
        # popular lots
        popular_lots = Lot.objects.filter(
            Q(is_active=True) & Q(is_auction_over=False)
            ).annotate(num_bids=Count('bids')).order_by('-num_bids')[:10]
        # print(popular_lots)

        # Auction ending soon
        soon_threshold = timezone.now() + timedelta(days=2)

        ending_soon_lots = Lot.objects.filter(
            Q(is_active=True) & Q(is_auction_over=False)
        ).annotate(
            end_time=ExpressionWrapper(
                F('auction_start_time') + timedelta(days=1) * F('auction_duration'),
                output_field=DateTimeField()
            )
        ).filter(
            end_time__lte=soon_threshold,
            end_time__gte=timezone.now()
        )[:10]

        # loved by others
        loved_by_others = Lot.objects.filter(
            Q(is_active=True) & Q(is_auction_over=False)
        ).annotate(num_favorites=Count('favorites')).order_by('-num_favorites')[:10]


        # upcoming auction
        upcoming_auctions = Lot.objects.filter(
            auction_start_time__gt=timezone.now(),
            is_active=True
        ).order_by('auction_start_time')
        print(upcoming_auctions)


        context = {
            'popular_lots': popular_lots,
            'ending_soon_lots': ending_soon_lots,
            'loved_by_others': loved_by_others,
            'upcoming_auctions':upcoming_auctions,  
            }

        return render(request, 'auctionapp/index.html', context)
    except Exception as e:
        print(e)


def lots_based_on_category(request, catgory_slug):
    try:
        lots_based_on_category = Category.objects.filter(slug=catgory_slug).first()
        print(lots_based_on_category)
        context = {
            'lots_based_on_category':lots_based_on_category,  
            }
        return render(request, 'auctionapp/categories/list.html', context)
    except Exception as e:
        print(e)

@login_required
def favorite_lots(request):
    try:
        favorite_lots = request.user.favorite_lots.all()
        return render(request, 'auctionapp/favorite_lots.html', {'favorite_lots': favorite_lots})
    except Exception as e:
        print(e)

# searching lot
# can remove stop words, stemming and ranking results
def search_lots(request):
    search_results = []
    context = None
    try:
        if 'query' in request.GET:
            query = request.GET.get('query', '')
            # Postgres full-text-search using a SearchVectorField
            search_vector = SearchVector('name', weight='A') + \
                SearchVector('description', weight='B') + \
                SearchVector('category__name', weight='C')

            # translates user terms into a query object for database comparison
            search_query = SearchQuery(query)
            # retrieving search results and sorting them by relevance
            search_results = Lot.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

            context = {
                'query':query,
                'results': search_results
            }
        return render(request, 'auctionapp/search_results.html', context)
    except Exception as e:
        print(e)