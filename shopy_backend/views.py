from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Product,CartItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except:
            pass

        response = Response({"message": "Logged out"})
        response.delete_cookie("refresh_token")
        return response


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            return Response({
                "access": str(access),
                "refresh": str(refresh)
            })
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


class TestGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})
    

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class UserCartView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
class AddItemCartView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        product_id = request.data.get('id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class RemoveItemCartView(APIView):
    def delete(self, request, user_id, item_code):
        user = get_object_or_404(User, id=user_id)
        cart_item = get_object_or_404(CartItem, id=item_code, user=user)
        cart_item.delete()
        return Response({"detail": "Item removed"}, status=status.HTTP_204_NO_CONTENT)