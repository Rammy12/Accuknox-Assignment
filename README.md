
## Question 1: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.?

### **Answer:**

By default, **Django signals execute synchronously**. This means the signal runs in the same execution flow as the caller, and the request does not complete until the signal finishes execution.

### **Proof with Code**

#### **views.py** (Triggering the Signal in APIView)

```python
import time
import datetime
import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer

class CreateUserView(APIView):
    def post(self, request):
        start_time = time.time()  # Start time tracking
        print(f"Creating a user at: {datetime.datetime.now()}")
        print(f"View running on Thread ID: {threading.get_ident()}")  # Check thread ID

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user instance, triggering post_save signal

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
```

#### **signals.py** (Post-Save Signal Execution)

```python
import time
import datetime
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    print(f"Signal started at: {datetime.datetime.now()}")
    print(f"Signal running on Thread ID: {threading.get_ident()}")  # Check thread ID
    time.sleep(3)  # Simulating a delay
    Profile.objects.create(user=instance, created_at=datetime.datetime.now())
    print(f"Signal finished at: {datetime.datetime.now()}")
```

### **Expected Behavior & Output:**

1. When a new user is created, the signal is triggered **before the API request completes**.
2. The total execution time includes the signal's 3-second delay.

#### **Console Output:**

```
Creating a user at: 2025-02-15 21:40:34.844182
View running on Thread ID: 19936
Signal started at: 2025-02-15 21:40:36.928689
Signal running on Thread ID: 19936    # Same thread ID as view
(Signal sleeps for 3 seconds...)
Signal finished at: 2025-02-15 21:40:39.951057
User created at: 2025-02-15 21:40:39.952057
```

#### **API Response:**

```json
{
    "message": "User created!",
    "Execution Time": 5.107875347137451,
    "View running on Thread ID": 19936
}
```

### **Conclusion:**

- The **request waits** for the signal to finish before returning a response.
- This confirms **Django signals are synchronous by default**.

---

## Question 2: Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.?

### **Answer:**

Yes, by default, Django signals run in the **same thread** as the caller.

### **Proof with Code**

- Both the **APIView (**`**)** and **Signal (**`**)** log the **thread ID**.
- If they run in the same thread, the thread IDs will match.

#### **Console Output:**

```
Creating a user at: 2025-02-15 21:40:34.844182
View running on Thread ID: 19936
Signal started at: 2025-02-15 21:40:36.928689
Signal running on Thread ID: 19936    # Same thread ID as view
(Signal sleeps for 3 seconds...)
Signal finished at: 2025-02-15 21:40:39.951057
User created at: 2025-02-15 21:40:39.952057
```

### **Conclusion:**

- The **thread ID in the view matches the signal’s thread ID**.
- This confirms that **Django signals run in the same thread as the caller by default**.

---

## Question 3: By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.?

### Answer:
Yes, **Django signals run in the same transaction as the caller by default**
### Proof with Code:

#### `views.py`
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import TestModel

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
```

#### `signals.py`
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel

@receiver(post_save, sender=TestModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal executed: Instance saved with name =", instance.name)
```

#### **Console Output:**
```
Signal executed: Instance saved with name = Before Rollback
Object created in DB
Exception occurred: Rolling back transaction!
```
#### **Responce:**
```
{
    "object_exists": false
}
```
### This fully structured example proves that Django signals are part of the same transaction as the caller!

---

## You are tasked with creating a Rectangle class with the following requirements:

An instance of the Rectangle class requires length:int and width:int to be initialized.
We can iterate over an instance of the Rectangle class 
When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}

## Class Definition
The `Rectangle` class is initialized with two integer parameters:
- `length`: The length of the rectangle
- `width`: The width of the rectangle

The class implements the `__iter__` method, making instances of `Rectangle` iterable.

## Code Implementation
```python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {"length": self.length}
        yield {"width": self.width}

# Creating an instance of Rectangle
rect = Rectangle(10, 5)

# Iterating over the Rectangle instance
for attribute in rect:
    print(attribute)
```

## Explanation
### Initialization
An instance of `Rectangle` is created with specified `length` and `width` values.

### Iteration
When iterated over, the instance first yields a dictionary containing the length in the format:
```python
{"length": <VALUE_OF_LENGTH>}
```
and then yields the width in the format:
```python
{"width": <VALUE_OF_WIDTH>}
```

### Output
```python
{'length': 10}
{'width': 5}
```
## Conclusion
The `Rectangle` class demonstrates how Python's iterator protocol can be leveraged to return structured data when iterating over an object. This approach enhances code readability and encapsulation.
