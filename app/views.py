import time
import threading
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
from .models import TestModel
from .serializers import UserRegistrationSerializer 

class CreateUserView(APIView):
    def post(self, request):
        start_time = time.time()  # Start time tracking
        print(f"Creating a user at: {datetime.datetime.now()}")
        ## for testing a thread (running same thread or not)
        print(f"View running on Thread ID: {threading.get_ident()}")  

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user instance

            end_time = time.time()  # End time tracking
            total_time = end_time - start_time  # Compute execution time

            print(f"User created at: {datetime.datetime.now()}")

            return Response(
                {
                    "message": "User created!",
                    "Execution Time": total_time,
                    "View running on Thread ID": threading.get_ident(),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TestSignalRollbackAPIView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():  # Start an atomic transaction
                obj = TestModel.objects.create(name="Before Rollback")
                print("Object created in DB")

                raise Exception("Rolling back transaction!") 

        except Exception as e:
            print(f"Exception occurred: {e}")

        # Check if the object exists after rollback
        exists = TestModel.objects.filter(name="Before Rollback").exists()
        return Response({"object_exists": exists}, status=status.HTTP_200_OK)

