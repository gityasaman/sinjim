from rest_framework import serializers
from .methods import generate_code, send_verification_mail
from .models import MyUser
from questions.models import Question, Answer

class MyUserSerializer(serializers.ModelSerializer):
    """Serializers MyUser model"""
    upvotes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = ['firstname', 'lastname', 'username', 'password', 'upvotes']
        extra_kwargs = {
            'password': {'write_only': True,
                         'style':{'input_type': 'password'}
                        }
        }

    def save(self, email, *args, **kwargs):
        user = MyUser(firstname=self.validated_data['firstname'],
                      lastname=self.validated_data['lastname'],
                      email=email,
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