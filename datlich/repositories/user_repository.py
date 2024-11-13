from ..models import UserModel

def save(user):
    user.save()
    return user

def find_by_username(username):
    try:
        return UserModel.objects.get(username=username)
    except UserModel.DoesNotExist:
        return None
