from blogs.models import AboutUs, Blog, Category


def about(request):
    return {
        "about": AboutUs.objects.first()
    }

def posts(request):
    return {
        "posts": Blog.objects.all()
    }

def categories(request):
    return {
        "categories": Category.objects.all()
    }
