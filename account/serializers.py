from rest_framework import serializers
from .methods import generate_code, send_verification_mail
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
    """Serializers MyUser model"""

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True,
                         'style':{'input_type': 'password'}
                        }
        }

    def save(self):
        user = MyUser(first_name=self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'],
                    email=self.validated_data['email'],
                    username=self.validated_data['username'],)

        password = self.validated_data['password']
        
        user.set_password(password)
        user.save()
        return user





# class RegisterSerializer(serializers.ModelSerializer):
#     """Serializes register"""
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True,}
#         }
    
#     def save(self):
#         user = User(first_name=self.validated_data['first_name'],
#                     last_name=self.validated_data['last_name'],
#                     email=self.validated_data['email'],
#                     username=self.validated_data['username'],)

#         password = self.validated_data['password']
        
#         user.set_password(password)
#         user.save()
#         return user

class EmailSerializer(serializers.Serializer):
    email  = serializers.EmailField()


class CodeSerializer(serializers.Serializer):
    code  = serializers.CharField(max_length=6)