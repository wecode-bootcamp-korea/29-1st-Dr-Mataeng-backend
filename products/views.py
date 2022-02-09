from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q,Sum,Count

from products.models  import ProductColor, ProductImage, ProductOption, ColorThumbnail

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        try:
            gender           = request.GET.getlist("gender", None)
            category         = request.GET.get("category", None)
            color            = request.GET.getlist("color", None)
            size             = request.GET.getlist("size", None)
            min_price        = request.GET.get("min_price", 10000)
            max_price        = request.GET.get("max_price", 500000)
            sort             = request.GET.get("sort", '신상품 순')
            offset           = int(request.GET.get("offset", 0))
            limit            = int(request.GET.get("limit", 6))
            products_colors  = ProductColor.objects.all()
            products_images  = ProductImage.objects.all()
            products_options = ProductOption.objects.all()

            """
            order_item 개수 Count
            status = Done 인 order_item들
            """

            sort_dict = {
                '인기순'      : '-total_sales',
                '낮은 가격 순' : 'product__price',
                '높은 가격 순' : '-product__price',
                '신상품 순'    : '-id'
            }

            q  = Q()
            q &= Q(productoption__product_color__product__price__range=[min_price, max_price])
            
            if category:
                q &= Q(productoption__product_color__product__category__name=category)
            if gender:
                q &= Q(productoption__product_color__product__gender__name__in=gender)
            if color:
                q &= Q(productoption__product_color__color__name__in=color)
            if size:
                q &= Q(productoption__size__name__in=size)

            products_colors = products_colors.filter(q)\
                              .annotate(total_sales=Count('productoption__orderitem__id'))\
                              .distinct().order_by(sort_dict.get(sort))\
                              [offset:offset+limit]
    
            data = [{
                "product_id"    : product_color.id,
                "product_name"  : product_color.product.name,
                "thumbnail_img" : products_images.filter(product_color_id=product_color.id)\
                                  .first().image_url,
                "price"         : int(product_color.product.price),
                "product_color" : product_color.color.name,
                "total_stock"   : products_options.filter(product_color_id=product_color.id)\
                                  .aggregate(Sum('stock'))['stock__sum'],
                "product_like"  : product_color.like_cnt,
                'total_sales'   : product_color.total_sales
            }for product_color in products_colors]

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
                "product_id" : color_thumbnail.product_color.id,
                "color_id"   : color_thumbnail.product_color.color.id,
                "color"      : color_thumbnail.product_color.color.name,
                "color_img"  : color_thumbnail.image_url
            } for color_thumbnail in colors_thumbnails]
            
            data = {
                "product_id"     : kwargs["product_id"],
                "product_name"   : product_color.product.name,
                "images"         : images,
                "sizes"          : sizes,
                "price"          : int(product_color.product.price),
                "colors"         : colors,
                "product_number" : product_color.product_number,
                "country"        : product_color.product.country.name,
                "material"       : product_color.material.name,
                "like"           : product_color.like_cnt,
            }
            return JsonResponse({"result" : data}, status=200)
        except ProductColor.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT DOES NOT EXIST'}, status=404)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)