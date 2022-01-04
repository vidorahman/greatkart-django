from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from . models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
# from django.http import HttpResponse


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': page_products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)

# Menerima permintaan dengan argumen category_slug, product_slug


def product_detail(request, category_slug, product_slug):
    try:
        # Temukan salah satu field category__slug dan slug pada kelas Product,
        # apakah category__slug = category_slug dan slug = product_slug cocok.
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = 0
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
# try:
#     categories = Category.objects.get(slug=category_slug)
# except Category.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)
