import pytest
from rest_framework.test import APIClient


client = APIClient()

@pytest.mark.django_db
def test_user_details_api():
    data = {
                "username" : "fanah",
                "email" : "fanah@gmail.com",
                "password" : "pandeyrb",
            }
    response = client.post('/api/register',data)
    response = client.post('/api/get-token',data)
    access_token = response.data["access"]
    
    
    
    #testing it with unautherized client
    response = client.get('/api/user-details')
    print(response.data)
    assert response.status_code == 401
    
    #testing it with autherized client
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    response = client.get('/api/user-details')
    print(response.data)
    assert response.status_code == 200
    
    #testing it with wrong method
    response = client.patch('/api/user-details')
    assert response.status_code == 405
    
    