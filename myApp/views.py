import razorpay
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myApp.models import Profile, Product


# razorpay client config
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# ----------------------------------- USER REGISTRATION -----------------------------------------
def user_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('registerFirstName')
        last_name = request.POST.get('registerLastName')
        email = request.POST.get('registerEmail')
        username = request.POST.get('registerUsername')
        password = request.POST.get('registerPassword')
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email is already use'})

        # Create the user
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect('userLogin')  # Redirect to the login page after successful registration

    return render(request, 'register.html')


# ------------------------------ USER LOGIN --------------------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                # Redirect superuser to admin panel
                return redirect('/admin/')
            return redirect('homePage')  # Redirect to the home page after successful login
        else:
            return render(request,'login.html',{'error_message': 'Invalid password'})
    return render(request, 'login.html', )


@login_required
def profile(request):
    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        username = request.POST.get('username')
        image = request.FILES.get('image_up_lode')
        dob = request.POST.get('d_o_b')
        # Update User model
        user = User.objects.get(username=request.user.username)
        user.first_name = firstname
        user.last_name = lastname
        user.username = username
        user.save()

        # Update or create Profile instance
        profile_instance, created = Profile.objects.get_or_create(user=request.user)
        print(image)
        if image:
            profile_instance.profile_picture = image
        if request.user.profile.date != dob:
            profile_instance.date = dob
        profile_instance.save()
        return redirect('homePage')
    # contex of profile page
    context = {
    }
    return render(request, 'profile.html',context)


# ------------------------- LOG OUT -------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('userLogin')


# --------------------------------- HOME PAGE ------------------------------------------
@login_required
def home_page(request):
    if request.method == 'POST':
        total_price = request.POST.get('total_price')
        amount = int(total_price + '00')
        if amount == 0:
            return redirect('homePage')
        request.session['amount'] = amount
        return redirect('payment')

    #creating product context
    product_data = Product.objects.all()

    context = {
        'product' : product_data,
    }


    return render(request, 'home.html',context)


# --------------------------------- PAYMENT PAGE ---------------------------------
def payment(request):
    amount = request.session.get('amount')
    currency = request.session.get('currency', 'INR')
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(
            amount=amount,
            currency='INR',
            payment_capture='0'
        )
    )

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'payment-handler/'
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
        'total_amount': amount / 100,
    }
    return render(request, 'payment.html', context)


# ----------------------- VERIFY SIGNATURE  -----------------------------------
@csrf_exempt
@login_required
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        amount = request.session.get('amount')
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.

            signature = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if signature is not None:

                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'payment-successful.html')
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment.
                    return render(request, 'payment-aborted.html')
            else:
                print('signature verification fails')
                # if signature verification fails.
                return render(request, 'payment-fail.html')
        except Exception as e:
            print(e)
            return render(request, 'payment-aborted.html')
    else:
        # if other than POST request is made.
        return render(request, 'payment-aborted.html')

# -----------------------STRONG PASSWORD VALIDAER ---------------------------
