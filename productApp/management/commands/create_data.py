import requests
from django.utils.text import slugify
from django.core.management import BaseCommand
from productApp.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('creating data......')
        response = requests.get('https://fakestoreapi.com/products').json()

        for product in response:
            #print(product)
            category, _ = Category.objects.get_or_create(
                title = product['category'],
                slug = slugify(product['category']),
                featured = True
            )
            Product.objects.create(
                category = category,
                title = product['title'],
                slug = slugify(product['title']),
                price = product['price'],
                thumbnail = product['image'],
                description = product['description']
            )
        print('Insertion complete!')
          
