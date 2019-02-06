# coding=utf-8

"""Function utilities to create user."""

# Django
from django.contrib.auth import get_user_model


def create_user(staff=False, superuser=False):
    """Create a user that can be used as an author of the Posts."""
    if superuser:
        return create_superuser()
    elif staff:
        return create_staff()
    else:
        return create_simple_user()


def create_simple_user():
    """Create a simple user that can be logged."""
    user_dict = {
        'username': "user",
        'password': "usermodel",
        'first_name': "User",
        'last_name': "Buyse"
    }
    user = get_user_model().objects.create_user(**user_dict)
    return user_dict, user


def create_staff():
    """Create a staff user that can be logged."""
    staff_dict = {
        'username': "user",
        'password': "usermodel",
        'first_name': "User",
        'last_name': "User",
        'is_staff': True
    }
    staff = get_user_model().objects.create_user(**staff_dict)
    return staff_dict, staff


def create_superuser():
    """Create a superuser that can be logged."""
    superuser_dict = {
        'username': "user",
        'password': "usermodel",
        'first_name': "User",
        'last_name': "User",
        'email': 'toto@example.com'
    }
    superuser = get_user_model().objects.create_superuser(**superuser_dict)
    return superuser_dict, superuser
