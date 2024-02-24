from django.shortcuts import render
from auctionapp.models import *
from django.shortcuts import render
from lot.models import Category, Lot
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def index(request):
    categories = Category.objects.all()
    art_category = Category.objects.filter(name="Fine Art").first()
    jwellery_category = Category.objects.filter(name="Jewelry").first()

    furniture_category = Category.objects.filter(name="Furnitures").first()
    context = {
        'jwellery_category': jwellery_category,
        'furniture_category': furniture_category,
        'art_category':art_category,  
        'categories': categories
        }

    return render(request, 'auctionapp/index.html', context)


def lots_based_on_category(request, catgory_slug):
    lots_based_on_category = Category.objects.filter(slug=catgory_slug).first()
    print("---------------------------------")

    print(lots_based_on_category)
    context = {
        'lots_based_on_category':lots_based_on_category,  
        }

    return render(request, 'auctionapp/categories/list.html', context)

@login_required
def favorite_lots(request):
    favorite_lots = request.user.favorite_lots.all()
    return render(request, 'auctionapp/favorite_lots.html', {'favorite_lots': favorite_lots})

# can remove stop words, stemming and ranking results
def search_lots(request):
    search_results = []
    context = None
    if 'query' in request.GET:
        query = request.GET.get('query', '')
        search_vector = SearchVector('name', weight='A') + \
            SearchVector('description', weight='B')
        search_query = SearchQuery(query)
        search_results = Lot.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')

        context = {
            'query':query,
            'results': search_results
        }
    return render(request, 'auctionapp/search_results.html', context)