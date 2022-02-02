from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q,Sum

from products.models  import ProductColor, ProductImage, ProductOption, ColorThumbnail

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        try:
            gender           = request.GET.get("gender", None)
            category         = request.GET.get("category", None)
            color            = request.GET.get("color", None)
            size             = request.GET.get("size", None)
            min_price        = request.GET.get("min_price", 10000)
            max_price        = request.GET.get("max_price", 500000)
            products_colors  = ProductColor.objects.all()
            products_images  = ProductImage.objects.all()
            products_options = ProductOption.objects.all()
            sort             = request.GET.get("sort", None)

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

            products_colors = products_colors.filter(q).distinct().order_by("id")
    
            data = [{
                "id"            : product_color.id,
                "product_name"  : product_color.product.name,
                "thumbnail_img" : products_images.filter(product_color_id=product_color.id)\
                                  .first().image_url,
                "price"         : int(product_color.product.price),
                "product_color" : product_color.color.name,
                "total_stock"   : products_options.filter(product_color_id=product_color.id)\
                                  .aggregate(Sum('stock'))['stock__sum'],
            }for product_color in products_colors]

            if sort == "인기순":
                data = sorted(data, key= lambda dict : dict['total_stock'])
            if sort == "신상품 순":
                data = sorted(data, key= lambda dict : dict['id'], reverse=True)
            if sort == "높은 가격 순":
                data = sorted(data, key= lambda dict : dict['price'], reverse=True)
            if sort == "낮은 가격 순":
                data = sorted(data, key= lambda dict : dict['price'])

            return JsonResponse({"result" : data}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status=400)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        try:
            product_color     = ProductColor.objects.get(id=kwargs["product_id"])
            products_images   = ProductImage.objects.filter(product_color_id=kwargs["product_id"])
            products_options  = ProductOption.objects.filter(product_color__id=kwargs["product_id"])
            colors_thumbnails = ColorThumbnail.objects.filter(product_color__product__name=product_color.product.name)

            images = [{
                "image_id"  : product_image.id, 
                "image_url" : product_image.image_url
                } for product_image in products_images]
            
            sizes  = [{
                "size_id" : product_option.size.id,
                "size"    : product_option.size.name,
                "stock"   : product_option.stock
            } for product_option in products_options]

            colors = [{
                "color_id"  : color_thumbnail.product_color.color.id,
                "color"     : color_thumbnail.product_color.color.name,
                "color_img" : color_thumbnail.image_url
            } for color_thumbnail in colors_thumbnails]
            
            data = {
                "id"             : kwargs["product_id"],
                "product_name"   : product_color.product.name,
                "images"         : images,
                "sizes"          : sizes,
                "price"          : int(product_color.product.price),
                "colors"         : colors,
                "product_number" : product_color.product_number,
                "country"        : product_color.product.country.name,
                "material"       : product_color.material.name,
            }
            return JsonResponse({"result" : data}, status=200)
        except ProductColor.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT DOES NOT EXIST'}, status=404)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)