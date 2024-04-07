
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Profile

client = APIClient()

@pytest.mark.django_db
def test_user_registration():
    data = {
                "username" : "fanah",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
            }
    response = client.post('/api/register',data)
    assert response.status_code == 201
    
    #testing username already exists
    data = {
                "username" : "fanah",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
            }
    response = client.post('/api/register',data)
    assert response.status_code == 400
    
    #testing wrong method
    data = {
                "username" : "fanah",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
            }
    response = client.get('/api/register',data)
    assert response.status_code == 405
    
    
    #testing registration with referral code 
    
    user = User.objects.get(username="fanah")
    referral_code = Profile.objects.get(user=user).referral_code
    data = {
                "username" : "tellis",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
                "referral_code" : referral_code
            }
    response = client.post('/api/register',data)
    assert response.status_code == 201
    

    
