from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Ad, Category


def home(request):
    ads = Ad.objects.filter(is_active=True).select_related('category')

    query = request.GET.get('q', '').strip()
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))

    category_slug = request.GET.get('category')
    if category_slug:
        ads = ads.filter(category__slug=category_slug)

    # Переменная current_category нужна только для подсветки активной категории в меню
    context = {
        'ads': ads,
        'query': query,
        'current_category': category_slug,
    }
    return render(request, 'ads/home.html', context)


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk, is_active=True)
    ad.increment_views()
    return render(request, 'ads/ad_detail.html', {'ad': ad})


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    ads = Ad.objects.filter(is_active=True, category=category)
    return render(request, 'ads/category.html', {'category': category, 'ads': ads})