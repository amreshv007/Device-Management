from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import GivenTo, TakenFrom
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        # print("===================")
        barcode = request.POST["barcode"]
        bar = barcode.split(',')
        # print(bar)
        modelName = request.POST["model"]
        today = datetime.now()
        # date = today.strftime("%B %d, %Y")
        if request.POST["hidden"] == "0":
            givenTo = request.POST["givento"]
            for b in bar:
                barcode_in_givento = GivenTo.objects.filter(user=request.user,barcode=b);
                if not barcode_in_givento:
                    barcode_in_takenfrom = TakenFrom.objects.filter(user=request.user,barcode=b);
                    if barcode_in_takenfrom:
                        barcode_in_takenfrom.delete()
                    data = GivenTo(user=request.user, barcode=b, modelName=modelName, givento=givenTo, date=today);
                    data.save();
                else:
                    x = "Barcode-"+b+" is already present in GivenTo Table!"
                    messages.info(request, x)
                    return redirect("/device-info/login")
        if request.POST["hidden"] == "1":
            takenfrom = request.POST["takenfrom"]
            for b in bar:
                barcode_in_takenfrom = TakenFrom.objects.filter(user=request.user,barcode=b);
                if not barcode_in_takenfrom:
                    barcode_in_givento = GivenTo.objects.filter(user=request.user,barcode=b);
                    if barcode_in_givento:
                        barcode_in_givento.delete()
                    data = TakenFrom(user=request.user, barcode=b, modelName=modelName, takenfrom=takenfrom, date=today);
                    data.save();
                else:
                    x = "Barcode-"+b+" is already present in ReceivedFrom Table!"
                    messages.info(request, x)
                    return redirect("/device-info/login")
    if request.user.is_authenticated:    
        allgivento = GivenTo.objects.filter(user=request.user)
        alltakenfrom = TakenFrom.objects.filter(user=request.user)
    else:
        allgivento = GivenTo.objects.all()
        alltakenfrom = TakenFrom.objects.all()
    return render(request,"index.html",{'allgivento':allgivento, 'alltakenfrom':alltakenfrom})

@login_required(login_url='/device-info/login')
def deleteGivenRows(request):
    if request.method == "POST" and request.user.is_authenticated:
        del_barcodes = request.POST.getlist('checks[]')
        for b in del_barcodes:
            print(b," ");
            barcode_in_givento = GivenTo.objects.filter(user=request.user,barcode=b);
            if barcode_in_givento:
                barcode_in_givento.delete()
    return redirect("/device-info")

@login_required(login_url='/device-info/login')
def deleteTakenRows(request):
    if request.method == "POST" and request.user.is_authenticated:
        del_barcodes = request.POST.getlist('checks[]')
        for b in del_barcodes:
            print(b," ");
            barcode_in_takenfrom = TakenFrom.objects.filter(user=request.user,barcode=b);
            if barcode_in_takenfrom:
                barcode_in_takenfrom.delete()
    return redirect("/device-info")

def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect("/device-info")
        else:
            messages.info(request, "Incorrect! Username or Password!")
            return redirect("/device-info/login")
    else:
        if request.user.is_authenticated:
            return redirect("/device-info")
        else:
            return render(request,"login1.html",context)

def signup(request):
    context = {}
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password"]
        password2 = request.POST["re_password"]
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("User already exist!")
                messages.info(request,"User already exist!")
                return redirect("/device-info/signup")
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print("User created!")
                messages.info(request, "User created!")
                return redirect("/device-info/login")
        else:
            messages.info(request, "Password Mismatched!")
            return HttpResponseRedirect(request.path_info)
    else:
        if request.user.is_authenticated:
            return redirect("/device-info")
        else:
            return render(request,"signup1.html",context)

@login_required(login_url='/device-info/login')
def editProfile(request):
    return render(request, "edit-profile.html")

@login_required(login_url='/device-info/login')
def editfname(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        getuser = User.objects.get(username=request.user.username);
        User.objects.filter(username=request.user).update(first_name=first_name)
        # request.user.update(first_name=first_name)
        # print(request.user)
        # fname = User.objects.update(first_name=first_name)
    return redirect("/device-info/edit-profile")

@login_required(login_url='/device-info/login')
def editlname(request):
    if request.method == "POST":
        last_name = request.POST["last_name"]
        User.objects.filter(username=request.user).update(last_name=last_name)
    return redirect("/device-info/edit-profile")

@login_required(login_url='/device-info/login')
def editpassword(request):
    if request.method == "POST":
        curr_password = request.POST["currpassword"]
        new_password = request.POST["newpassword"]
        re_password = request.POST["re_password"]
        user_name = request.user.username
        user = auth.authenticate(username=user_name,password=curr_password)
        if user is not None:
            if new_password == re_password:
                # save the updated password.
                user.set_password(new_password)
                user.save()
                return redirect("/device-info/login")
            else:
                messages.info(request, "New Password Mismatched!")
                return HttpResponseRedirect(request.path_info)
        else:
            messages.info(request, "Enter Correct Current Password!")
    return redirect("/device-info/edit-profile")

@login_required(login_url='/device-info/login')
def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return redirect("/device-info/")


