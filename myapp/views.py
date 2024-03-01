from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from .models import Bill, User
import jwt
import json
import secrets


def test(request):
    return JsonResponse({'message': 'This is a test endpoint'})

# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data)
#             name = data['name']
#             email = data['email']
#             password = make_password(data['password'])
#             print(password)

#             if User.objects.filter(email=email).first()!=None:
#                 print(email)
#                 return JsonResponse({'success': False, 'message': 'Email already registered'}, status=400)

#             User.objects.create(name=name, email=email, password=password)
#             return JsonResponse({'success': True, 'message': 'User registered successfully'}, status=201)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': 'some error occured'}, status=500)

from django.contrib.auth.hashers import make_password

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            name = data['name']
            email = data['email']
            password = make_password(data['password'])
            # print(password)

            if User.objects.filter(email=email).exists():
                # print(email)
                return JsonResponse({'success': False, 'message': 'Email already registered'}, status=400)

            User.objects.create(name=name, email=email, password=password)
            return JsonResponse({'success': True, 'message': 'User registered successfully'}, status=201)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'message': 'Some error occurred'}, status=500)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            user = User.objects.filter(email=email).first()
            # print(f"User: {user}")  # Debugging statement
            if user is None:
                return JsonResponse({'success': False, 'message': 'User not found'}, status=401)

            # print(f"User password: {user.password}")  # Debugging statement
            if not check_password(password, user.password):
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)

            token = jwt.encode({'userId': str(user.id), 'email': user.email}, 'your_secret_key', algorithm='HS256')
            # print(f"Generated token: {token}")  # Debugging statement
            return JsonResponse({'success': True, 'message': 'Sign-in successful', 'token': token}, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'message': 'Failed to sign in'}, status=500)


@csrf_exempt
def create_bill(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            billno = data['billno']
            companyname = data['companyname']
            amount = data['amount']

            # Generate unique ID for doc_id
            # doc_id = secrets.token_hex(12)  # Generates a 24-character hexadecimal string
            
            Bill.objects.create(billno=billno, companyname=companyname, amount=amount)
            # Bill.objects.create(doc_id=doc_id,billno=billno, companyname=companyname, amount=amount)

            return JsonResponse({'success': True, 'message': 'Bill created successfully'}, status=201)
        except KeyError as ke:
            return JsonResponse({'success': False, 'message': f'Missing key: {ke}'}, status=400)
        except ValueError as ve:
            return JsonResponse({'success': False, 'message': f'Invalid value: {ve}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Internal server error'}, status=500)


from bson.decimal128 import Decimal128

@csrf_exempt
def get_all_bills(request):
    if request.method == 'GET':
        try:
            all_bills = list(Bill.objects.all().values( 'id','billno', 'companyname', 'amount', 'created_at', 'updated_at'))
            
            # Convert Decimal128 objects to strings
            for bill in all_bills:
                bill['amount'] = str(bill['amount'])

            return JsonResponse({'success': True, 'data': all_bills}, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'message': 'Internal server error'}, status=500)



@csrf_exempt
def get_bill_by_id(request, id):
    if request.method == 'GET':
        try:
            # print('inside try')
            bill = Bill.objects.filter(id=id).first()
            # print(bill)
            if bill:
                return JsonResponse({'success': True, 'data': {'id': bill.id, 'billno': bill.billno, 'companyname': bill.companyname, 'amount': str(bill.amount)}}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bill not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Internal server error'}, status=500)


@csrf_exempt
def update_bill(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            print('inside update')
            bill = Bill.objects.filter(id=id).first()
            # print(bill.doc_id)
            if bill:
                print('if')
                bill.billno = data.get('billno', bill.billno)
                bill.companyname = data.get('companyname', bill.companyname)
                bill.amount = data.get('amount', bill.amount)
                # bill.doc_id=id
                bill.save()
                return JsonResponse({'success': True, 'message': 'Bill updated successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bill not found'}, status=404)
        except Exception as e:
            print(f"Error: {e}")  # Print the error
            return JsonResponse({'success': False, 'message': 'Internal server error'}, status=500)


@csrf_exempt
def delete_bill(request, id):
    if request.method == 'DELETE':
        try:
            print('inside delete')
            bill = Bill.objects.filter(id=id).first()
            # print(bill.doc_id)
            if bill:
                bill.delete()
                return JsonResponse({'success': True, 'message': 'Bill deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Bill not found'}, status=404)
        except Exception as e:
            print(f"Error: {e}")  # Print the error
            return JsonResponse({'success': False, 'message': 'Internal server error'}, status=500)

