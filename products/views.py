import json

from django.http  import JsonResponse
from django.views import View
from django.db.models import Q

from products.models import ProductColor, ProductImage, ProductOption

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        try:
            gender          = request.GET.get("gender", None)
            category        = request.GET.get("category", None)
            color           = request.GET.get("color", None)
            size            = request.GET.get("size", None)
            min_price       = request.GET.get("min_price", 10000)
            max_price       = request.GET.get("max_price", 500000)
            products_colors = ProductColor.objects.all()
            products_images = ProductImage.objects.all()
            sort            = request.GET.get("sort", "인기순")

            sort_dict = {
                "인기순"      : "id",
                "신상품 순"    : "-id",
                # "높은 가격 순" : "-price",
                # "낮은 가격 순" : "price",
                }

            q  = Q()
            q &= Q(productoption__product_color__product__price__gte=min_price)
            q &= Q(productoption__product_color__product__price__lte=max_price)
            
            if category:
                q &= Q(productoption__product_color__product__category__name=category)
            if gender:
                gender = gender.split(',')
                q &= Q(productoption__product_color__product__gender__name__in=gender)
            if color:
                color = color.split(',')
                q &= Q(productoption__product_color__color__name__in=color)
            if size:
                size = size.split(',')
                q &= Q(productoption__size__name__in=size)

            products_colors = products_colors.filter(q).distinct().order_by(sort_dict[sort])
    
            data = [{
                "id"            : product_color.id,
                "product_name"  : product_color.product.name,
                "thumbnail_img" : products_images.filter(product_color_id=product_color.id)\
                                  .first().image_url,
                "price"         : int(product_color.product.price),
                "product_color" : product_color.color.name,
            }for product_color in products_colors]

            return JsonResponse({"result" : data}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status=400)
        except Exception as e:
            return JsonResponse({"message" : e}, status=400)