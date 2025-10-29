from django.shortcuts import render
import requests

API_URL = "http://127.0.0.1:8000"

def index(request):
    response = requests.get(f"{API_URL}/products")
    products = response.json() if response.status_code == 200 else []
    return render(request, "shop/index.html", {"products": products})
