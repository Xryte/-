from .models import Category


def global_categories(request):
    if request.path.startswith('/admin/'):
        return {}


    return {
        'global_categories': list(Category.objects.all())
    }