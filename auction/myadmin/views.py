from django.shortcuts import render, redirect
from django.contrib import messages
from lot.models import Category

def index(request):
    return render(request, 'myadmin/index.html')

def createCategory(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'create':
                name = request.POST.get('name')
                slug = request.POST.get('slug')
                description = request.POST.get('description')
                parent_id = request.POST.get('parent_id')
          
                if parent_id == "":
                    category = Category.objects.create(name=name, slug=slug, description=description)
                else:
                    parent = Category.objects.get(id=parent_id)
                    category = Category.objects.create(name=name, slug=slug, description=description, parent=parent)

                messages.success(request, "New category created successfully")
          
            else:
                category_id = request.POST.get('category_id')
                category = Category.objects.get(id=category_id)
                category.name = request.POST.get('name')
                category.slug = request.POST.get('slug')
                category.description = request.POST.get('description')
                category.save()
                messages.success(request,"Category updated")

            return redirect('myadmin:category_detail', category.slug)
      
        except Exception as e:
                messages.error(request, e)
                return redirect('myadmin:category_detail')
    
    category_options = Category.objects.all()

    context = {
        'category_options': category_options,
        'categories': category_options.filter(parent=None),
    }

    return render(request, "lot/category/list.html", context=context)

def categoryDetail(request, slug):
    category = Category.objects.get(slug=slug)

    context = {
        'category': category,
        'categories': category.sub_category.all(),

    }
    return render(request, 'lot/category/list.html', context=context)

def categoryDelete(request, slug):
    category = Category.objects.get(slug=slug)

    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, f"Category \"{category.name}\" deleted successfully")
        except Exception as e:
            messages.error(request, e)

    return redirect('myadmin:category_create')



