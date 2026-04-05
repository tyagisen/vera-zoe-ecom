from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from apps.cart.models import Cart, CartItem
from apps.cart.api.serializers import CartSerializer, AddToCartSerializer
from apps.products.models import ProductVariant
from django.shortcuts import get_object_or_404


class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart
    

class AddToCartAPIView(generics.GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        variant_id = serializer.validated_data["variant_id"]
        quantity = serializer.validated_data["quantity"]
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        with transaction.atomic():
            item,created = CartItem.objects.get_or_create(
                cart=cart,
                variant = variant,
                defaults={"quantity": quantity},
            )
            if not created:
                item.quantity +=quantity
                item.save()
            
        return Response({"message": "Item Added to cart"}, status=status.HTTP_200_OK)



class UpdateCartItemAPIView(generics.GenericAPIView):
    serializer_class =AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        quantity = serializer.validated_data["quantity"]
        item = CartItem.objects.get(id=pk, cart__user=request.user)
        item.quantity=quantity
        item.save()
        return Response({"message": "cart Updated"})


class RemoveCartItemAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = CartItem.objects.get(id=pk, cart__user=request.user)
        item.delete()
        return Response({"message": "Item Removed."})