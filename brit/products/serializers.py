from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from products.models import Products


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=True)

    class Meta:
        model = Products
        fields = ("name", "price")

    def create(self, validated_data):
        # Add the user to the validated data before creating the product
        user = self.context['request'].user
        validated_data['user'] = user
        product = Products.objects.create(**validated_data)
        return product

    def destroy(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            user = request.user  # Assuming user is authenticated

            # Check if the product belongs to the authenticated user
            if product.user == user:
                product.delete()
                return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You don't have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)

        except Products.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)