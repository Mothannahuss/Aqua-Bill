# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from aquabill.views import CustomAuthToken
# from aquabill.models import Device  # Import your Device model
# import json

# class DeviceTokenAuthTests(TestCase):

#     def setUp(self):
#         # Create a test device instance if needed
#         self.device = Device.objects.get_or_create(id=16)[0]
        
#         self.client = APIClient()

#     def test_device_token_auth(self):
#         # Replace 'your_endpoint_name' with the actual name you used in urls.py for the custom auth view
#         url = reverse('get-api') 
#         data = {'id': "16"}  # Use the actual device id field and value
#         response = self.client.post(url, data, format='json')
#         print(response.data['token'])
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)

# class DevicePartialUpdate(TestCase):

#     def setUp(self):
#         # Create a test device instance if needed
        
#         self.device = Device.objects.get(id=12)
#         self.id = self.device[0].id
#         self.client = APIClient()

#         self.token = self.get_token()


    
#     def get_token(self):
#         url = reverse('get-api') 
#         data = {'id': str(self.id)}
#         response = self.client.post(url, data, format='json')
#         return response.data['token']

#     def test_device_token_auth(self):
#         url = reverse('device-update', kwargs={'id': self.id})
#         data = {'id': str(self.id),'current_read': 20}  # Use the actual device id field and value
#         headers = { "Authorization" : "Token " + self.token }
#         response = self.client.patch(url, data, format='json', headers=headers)
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
