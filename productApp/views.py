from django.core.paginator import PageNotAnInteger,EmptyPage,InvalidPage,Paginator
from django.views.generic import TemplateView,DetailView,ListView
from django.views import generic
from django.db.models import Q
from django.shortcuts import render
from .models import *
from cartApp.carts import Cart


# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'featured_categories': Category.objects.filter(featured=True),
                'featured_products': Product.objects.filter(featured=True),
                'sliders': slider.objects.filter(show=True),
            }
        )
        return context


class ProductDetails(DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related
        return context
    

class CategoryDetails(DetailView):
    model = Category
    template_name = 'product/category-details.html'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object().products.all()
        return context


class CustomPaginator:
    def __init__(self,request,queryset,paginate_by) -> None:
        self.paginator = Paginator(queryset,paginate_by)
        self.paginated_by = paginate_by
        self.queryset = queryset
        self.page = request.GET.get('page',1)

    def get_queryset(self):
        try:
           queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
           queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset = self.paginator.page(1)
        return queryset



class ProductList(ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'object_list'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = CustomPaginator(self.request, self.get_queryset(), self.paginate_by)
        queryset = page_obj.get_queryset()
        paginator = page_obj.paginator
        context['object_list'] = queryset
        context['paginator'] = paginator
        # print(context['object_list'],'yeamin')
        # print(context['paginator'],'yeamin')
        return context
    

class SearchProducts(generic.View):
    def get(self,*args, **kwagrs):
        key = self.request.GET.get('key','')
        products = Product.objects.filter(
            Q(title__icontains = key) |
            Q(category__title__icontains = key)
        )
        context = {
            'products':products,
            'key':key,
        }
        return render(self.request,'product/search-products.html',context)
