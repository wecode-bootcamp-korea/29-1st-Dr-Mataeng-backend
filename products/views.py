import json

from django.http  import JsonResponse
from django.views import View

from django.db.models       import Q

from products.models import ProductColor, ProductImage

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        try:
            gender      = request.GET.get("gender", None)
            category    = request.GET.get("category", None)
            products_colors = ProductColor.objects.all()
            products_images = ProductImage.objects.all()

            q = Q()
            
            if category:
                q &= Q(productoption__product_color__product__category__name=category)
            if gender:
                gender = gender.split(',')
                q &= Q(productoption__product_color__product__gender__name__in=gender)

            products_colors = ProductColor.objects.filter(q).distinct().order_by("id")

            data = [{
                "id"            : product_color.id,
                "product_name"  : product_color.product.name,
                "thumbnail_img" : products_images.filter(product_color_id=product_color.id).first().image_url,
                "price"         : round(product_color.product.price),
                "product_color" : product_color.color.name,
            }for product_color in products_colors]

            return JsonResponse({"result":data}, status=200)
        except Exception as e:
            return JsonResponse({"message": e}, status=400)