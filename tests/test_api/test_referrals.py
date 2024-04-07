import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Profile

client = APIClient()

@pytest.mark.django_db
def test_referrals():
    data = {
                "username" : "fanah",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
            }
    response = client.post('/api/register',data)
    response = client.post('/api/get-token',data)
    access_token = response.data["access"]
    
    
    user = User.objects.get(username="fanah")
    referral_code = Profile.objects.get(user=user).referral_code
    data = {
                "username" : "tellis",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
                "referral_code" : referral_code
            }
    response = client.post('/api/register',data)
    
    
    #testing it with unautherized client
    response = client.get('/api/referral-details')
    print(response.data)
    assert response.status_code == 401
    
    #testing it with autherized client
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    response = client.get('/api/referral-details')
    print(response.data)
    assert response.status_code == 200
    
    #testing it with wrong method
    response = client.post('/api/referral-details')
    assert response.status_code == 405
    
    