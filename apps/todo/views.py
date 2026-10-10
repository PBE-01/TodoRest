from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from apps.todo.models import Category
from apps.todo.serializer import CategoryListSerializer, CategoryCreateSerializer, CategoryUpdateSerializer

# Create your views here.
class CategoryView(views.APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        context = {
            'categories': serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategoryCreateSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailUpdateView(views.APIView):
    def get(self, request, **kwargs):
        print(kwargs)
        id = kwargs.get('pk')
        category = get_object_or_404(Category, id=id)
        serializer = CategoryListSerializer(instance=category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, **kwargs):
        ### put methodi to‘liq yangilash. PUT metodi odatda resursni to‘liq yangilash uchun ishlatiladi.
        id = kwargs.get('pk')
        instance = Category.objects.get(id=id)
        serializer = CategoryUpdateSerializer(instance, request.data)
        ##### instance — bazadan olingan mavjud obyekt, request.data esa frontend yuborgan ma’lumotlar.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, **kwargs):
        ### patch methodi qisman yangilash. PATCH metodi obyektning faqat kerakli maydonlarini yangilash uchun ishlatiladi.
        id = kwargs.get('pk')
        instance = Category.objects.get(id=id)
        serializer = CategoryUpdateSerializer(instance, request.data, partial=True)
        ##### instance — bazadan olingan mavjud obyekt, request.data esa frontend yuborgan ma’lumotlar.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        id = kwargs.get('pk')
        category = Category.objects.get(id=id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)