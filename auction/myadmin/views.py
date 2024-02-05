from django.shortcuts import render, redirect
from django.contrib import messages
from lot.models import Category

def index(request):
    return render(request, 'myadmin/index.html')

def createCategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        parent_id = request.POST.get('parent')

        try:
            if parent_id == None:
                category = Category.objects.create(name=name, slug=slug, description=description)
            else:
                parent = Category.objects.get(id=parent_id)
                category = Category.objects.create(name=name, slug=slug, description=description, parent=parent)

            messages.success(request, "New category created successfully")
        except Exception as e:
            messages.error(request, e)
  
        return redirect('myadmin:category_detail', category.slug)
    
    category_options = Category.objects.all()

    context = {
        'category_options': category_options,
        'categories': category_options.filter(parent=None),
    }

    return render(request, "lot/category/create.html", context=context)

def categoryDetail(request, slug):
    category = Category.objects.get(slug=slug)

    context = {
        'category': category,

    }
    
    return render(request, 'lot/category/detail.html', context=context)

