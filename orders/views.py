from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

class OrderDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
