from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder
import json

# Create your tests here.

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {'name': 'Test Vendor', 'contact_details': 'test@example.com', 'address': 'Test Address', 'vendor_code': 'VENDOR001'}

    def test_create_vendor(self):
        response = self.client.post('/api/vendors/', self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

    def test_get_vendors(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='Test Address', vendor_code='VENDOR001')
        self.po_data = {'po_number': 'PO001', 'vendor': self.vendor.id, 'order_date': '2024-05-05T12:00:00Z', 'delivery_date': '2024-05-10T12:00:00Z', 'items': json.dumps(['item1', 'item2']), 'quantity': 10, 'status': 'pending'}

    def test_create_purchase_order(self):
        response = self.client.post('/api/purchase_orders/', self.po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO001')

    def test_get_purchase_orders(self):
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_purchase_order(self):
        po = PurchaseOrder.objects.create(po_number='PO001', vendor=self.vendor, order_date='2024-05-05T12:00:00Z', delivery_date='2024-05-10T12:00:00Z', items=json.dumps(['item1', 'item2']), quantity=10, status='pending')
        response = self.client.patch(f'/api/purchase_orders/{po.id}/acknowledge/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(PurchaseOrder.objects.get(id=po.id).acknowledgment_date)

