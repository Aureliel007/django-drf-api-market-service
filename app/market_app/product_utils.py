from .models import Category, Product, ShopCategory, ProductParameter, Parameter

def update_products_from_data(data, shop_id):
    
    # Импорт категорий
    for category in data.get('categories', []):
        cat = Category.objects.get_or_create(name=category['name'])[0]
        external_id = category.get('id')
        ShopCategory.objects.get_or_create(shop_id=shop_id, category_id=cat.id, external_id=external_id)  

    # Импорт товаров
    products = data.get('goods', [])
    for item in products:
        category_external_id = item.get('category')
        category_id = Category.objects.filter(shop_categories__external_id=category_external_id).first().id
        parameters = item.get('parameters', {})

        product = Product.objects.update_or_create(
            external_id=item['id'],
            defaults={
                'category_id': category_id,
                'shop_id': shop_id,
                'model': item.get('model', ''),
                'name': item.get('name'),
                'price': item.get('price'),
                'price_rrc': item.get('price_rrc'),
                'quantity': item.get('quantity', 0)
            }
        )[0]

        # Импорт параметров
        for key, value in parameters.items():
            parameter=Parameter.objects.get_or_create(name=key)[0]
            ProductParameter.objects.update_or_create(
                product=product,
                parameter=parameter,
                defaults={'value': value}
            )
            