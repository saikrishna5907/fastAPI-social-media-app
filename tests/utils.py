from fastapi import status


def assert_not_authenticated(response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"

def assert_forbidden(response):
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You are not authorized to perform this action"
    
def assert_post_not_found(response, id):
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Post with id: {id} was not found"
    
def assert_vote_create_success(response):
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == "Vote created successfully"
    
def assert_vote_update_success(response):
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == "Vote updated successfully"