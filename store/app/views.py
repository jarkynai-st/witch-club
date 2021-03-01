from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .filters import ProductFilter
from .models import Product, Order, Contact
from .forms import *
from .token import account_activation_token


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('products/active.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()

    context = {"form":form}
    return render(request,'products/register.html',context)





def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        login(request,user)
        return redirect('home')
    return render(request,'products/login.html')


def create_order(request,product_id):
    product = Product.objects.get(id=product_id)
    form = OrderForm(initial={'product':product,'user':request.user})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'products/create_order.html',context)




def update_order(request,order_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request,'products/create_order.html',context)


def contacts_page(request):
    contacts = Contact.objects.all()
    return render(request,'products/contacts.html',{"contacts":contacts})


def logout_page(request):
    logout(request)
    return redirect('home')


def homepage(request):
    products = Product.objects.all()
    filters = ProductFilter(request.GET,queryset=products)
    products = filters.qs
    contacts = Contact.objects.all()
    return render(request,'products/products.html',{"products":products,'filters':filters,'contacts':contacts})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation.Now you can login your account_act')
    else:
        return HttpResponse('Activation link is invalid!')