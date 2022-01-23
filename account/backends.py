from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

    # def authenticate(self, request, username=None, password=None, **kwargs):
    #     UserModel = get_user_model()
    #     if username is None:
    #         username = kwargs.get(UserModel.USERNAME_FIELD)
    #     try:
    #         case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
    #         user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
    #     except UserModel.DoesNotExist:
    #         UserModel().set_password(password)
    #     else:
    #         if user.check_password(password) and self.user_can_authenticate(user):
    #             return user