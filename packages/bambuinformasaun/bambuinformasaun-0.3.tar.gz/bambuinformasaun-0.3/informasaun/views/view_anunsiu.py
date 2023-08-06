from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# from population.models import Population,DetailFamily,Family,Religion,Profession,Citizen,Aldeia,Village,User,Migration,Death,Migrationout,Temporary,ChangeFamily
# from population.utils import getnewidp,getnewidf
# from population.forms import Family_form,Family_form,FamilyPosition,Population_form,DetailFamily_form,CustumDetailFamily_form,Death_form,Migration_form,Migrationout_form,Changefamily_form
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

from django.core.paginator import Paginator

# from mapa.forms import *
# from custom.utils import getnewid, getjustnewid, hash_md5, getlastid
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import date
from django.http import JsonResponse
# from employee.models import *
# from datetime import datetime, timedelta
# from vizitor.forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mapa.models import *
from mapa.forms import *
from informasaun.models import *
from informasaun.forms import *
from django.contrib.auth.models import User
from jeral.utils import getlastid
from main.decorators import login_ona, seidauk_login, allowed_users




@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def anunsiu(request):
    page_num = 1
    buka = False
    bukatitle = "mamuk"
    if request.GET.__contains__('page') :
        page_num = request.GET.get('page')
    else:
        page_num = 1
    if request.GET.__contains__('pesquiza'):
        buka = True
        paginator = Paginator(KonteuduAnunsiu.objects.order_by('-id').filter(titulu__icontains=request.GET['pesquiza']), 10)

    else:
        paginator = Paginator(KonteuduAnunsiu.objects.order_by('-id'), 1)

    page_range = []
    for i in range(paginator.num_pages):
        page_range.append(i+1)
        data_Informasaun = paginator.page(page_num)
        page_num_int = int(page_num)

    if buka :
        bukatitle = "Rezultadu Pesquiza husi <i>' (" + request.GET['pesquiza'] + ") '</i>"

    data = []
    lingua = Lingua.objects.all()
    titulu = ""
    for dadosinfo in data_Informasaun :
        statuslingua = ""
        for dadoslingua in lingua : 
            konteudu = KonteuduAnunsiu.objects.filter(anunsiu = dadosinfo.anunsiu.id , lingua = dadoslingua.id).count()
            if konteudu > 0 :
                konteudu = KonteuduAnunsiu.objects.filter(anunsiu = dadosinfo.anunsiu.id , lingua = dadoslingua.id).last()
                # konteudu2 = KonteuduInformasaun.objects.filter(informasaun = dadosinfo.id , lingua = 1).last()
                titulu = konteudu.titulu
                statuslingua = statuslingua +  " <i><b>   <img src=" +dadoslingua.icon.url + " width='20px'> &nbsp; </b> </i> " + konteudu.titulu + "<br>"
            else :
                statuslingua = statuslingua +  "<i><b>   <img src=" +dadoslingua.icon.url + " width='20px'> &nbsp;  </b> </i>  <font color ='red'> Laiha</font> <br>"
        data.append({'imagen' : dadosinfo.anunsiu.imagen_main ,'lingua':dadoslingua.naran,'linguaicon' : dadoslingua.icon,'linguaid' : dadoslingua.id, 'statuslingua': statuslingua , 'data' : dadosinfo.anunsiu.data ,'titulu' : titulu , "id" : dadosinfo.anunsiu.id })


    context = {
        "pajina_anunsiu" : "active",
        "anunsiu" : data,
        'bukatitle' : bukatitle,
        'page_range' : page_range,
        'current_page' : page_num_int,
    }
    return render(request, 'informasaun/anunsiu/lista.html',context)





@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def inputanunsiu(request):

    dataagora = timezone.now()
    if request.method == 'POST':
        hashed = getlastid(Anunsiu)
        forms = KonteuduAnunsiuForm(request.POST)
        if forms.is_valid():

            info = Anunsiu()
            info.id = hashed[0]
            info.data = request.POST['data']
            info.date_created = dataagora
            info.user_created = User.objects.get(id = request.user.id)
            info.save()


            instance = forms.save(commit=False)
            instance.anunsiu = Anunsiu.objects.get(id=hashed[0])
            # instance.id = hashed[0]
            # instance.hashed = hashed[1] 
            instance.save()
            messages.success(request,"Dados Rejistu  ho Susessu..!")
            return redirect('informasaun:anunsiu')


    anunsiuform = KonteuduAnunsiuForm()
    context = {
        "asaun" : "input",
        "pajina_anunsiu" : "active",
        # "dokumentu" : dokumentu,
        "pajina_titulu" : "Rejistu Perfil",
        "button" : "Rejistu",
        "forms" : anunsiuform,
    }
    return render(request, 'informasaun/anunsiu/input.html',context)




@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def manezakonteuduanunsiu(request,id):

    #konteudu lingua 

    konteuduanunsiu =  KonteuduAnunsiu.objects.filter(anunsiu = id)
    konteuduanunsiu =  KonteuduAnunsiu.objects.get(anunsiu = id)
    lingua = Lingua.objects.all()
    data = []

    for dados in lingua.iterator() :
        konteudu = KonteuduAnunsiu.objects.filter(lingua=dados.id,anunsiu = id).count()
        if konteudu > 0 :
            konteudu = KonteuduAnunsiu.objects.filter(lingua=dados.id,anunsiu = id).last()
            data.append({'lingua':dados.naran,'linguaicon' : dados.icon,'linguaid' : dados.id,  'status': 'iha' , 'data' : konteudu.data ,'titulu' : konteudu.titulu , "id" : konteudu.id })
        else :
            data.append({'lingua':dados.naran,'linguaicon' : dados.icon,'linguaid' : dados.id, 'status': 'laiha' , 'data' : "Mamuk" ,'titulu' : "Mamuk" , "id" : int(id) })

    #konteudu imagen

    fileanunsiu =  FileAnunsiu.objects.filter(anunsiu = id)
    forms = FileAnunsiuForm()
    anunsiu = Anunsiu.objects.filter(id = id)
    mainimagen = Anunsiu.objects.get(id = id)
    lingua = Lingua.objects.all()
    imagen = FileAnunsiu.objects.filter(anunsiu = id)


    if request.method == 'POST':
        forms = FileAnunsiuForm(request.POST, request.FILES)
        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.anunsiu = Anunsiu.objects.get(id=id)
            instance.save()
            messages.success(request,"Dadus Rejistu  ho Susessu..!")
            return redirect('informasaun:manezakonteuduanunsiu', id = id)

    context = {
        "asaun" : "input",
        "pajina_anunsiu" : "active",
        "konteuduanunsiu" : data,
        "pajina_titulu" : "Maneza Konteudu",
        "button" : "Rejistu",
        "id" : id,
        "naran_atividade" : konteuduanunsiu.titulu,
        "mainimagen" : mainimagen.imagen_main,
        "forms" : forms,
        "anunsiu" : anunsiu,
        "fileanunsiu" : fileanunsiu,


    }
    return render(request, 'informasaun/anunsiu/manezakonteudu.html',context)


    # editkonteuduanunsiu




@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def editkonteuduanunsiu(request,id,lingua):
    konteuduanunsiu = KonteuduAnunsiu.objects.get(id=id, lingua = lingua)

    if request.method == 'POST':
        hashed = getlastid(KonteuduAnunsiu)
        forms = KonteuduAnunsiuForm(request.POST, instance = konteuduanunsiu)
        if forms.is_valid():
            instance = forms.save(commit=False)
            # instance.id = hashed[0]
            # instance.hashed = hashed[1] 
            instance.lingua = Lingua.objects.get(id=lingua)
            Anunsiu.objects.filter(pk=konteuduanunsiu.anunsiu.id).update(data=request.POST['data'])
            instance.save()
            messages.success(request,"dados Rejistu  ho Susessu..!")
            return redirect('informasaun:manezakonteuduanunsiu' , id =  konteuduanunsiu.anunsiu.id)

    konteuduanunsiuform = KonteuduAnunsiuForm(instance = konteuduanunsiu)
    context = {
        "asaun" : "edit",
        "pajina_anunsiu" : "active",
        # "dokumentu" : dokumentu,
        "pajina_titulu" : "Atualiza Konteudu",
        "button" : "Atualiza",
        "forms" : konteuduanunsiuform,
    }
    return render(request, 'informasaun/anunsiu/inputkonteuduanunsiu.html',context)


    



@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def inputkonteuduanunsiu(request,id,lingua):
    if request.method == 'POST':
        hashed = getlastid(KonteuduAnunsiu)
        forms = KonteuduAnunsiuForm(request.POST)
        if forms.is_valid():
            print("tamaaa")
            instance = forms.save(commit=False)
            instance.anunsiu = Anunsiu.objects.get(id = id)
            instance.lingua = Lingua.objects.get(id=lingua)
            # instance.id = hashed[0]
            # instance.hashed = hashed[1] 
            Anunsiu.objects.filter(pk=id).update(data=request.POST['data'])
            instance.save()
            messages.success(request,"dados Rejistu  ho Susessu..!")
            return redirect('informasaun:manezakonteuduanunsiu' , id =  id)

    konteuduanunsiuform = KonteuduAnunsiuForm()
    context = {
        "asaun" : "input",
        "pajina_anunsiu" : "active",
        # "dokumentu" : dokumentu,
        "pajina_titulu" : "Rejistu Perfil",
        "button" : "Rejistu",
        "forms" : konteuduanunsiuform,
    }
    return render(request, 'informasaun/anunsiu/inputkonteuduanunsiu.html',context)


@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def apagafileanunsiu(request,id):
    fileanunsiu = FileAnunsiu.objects.get(id=id)
    idinfo = fileanunsiu.anunsiu.id
    fileanunsiu.delete()
    messages.success(request,"Dados Apaga  Susessu..!")
    return redirect('informasaun:manezakonteuduanunsiu', id = idinfo)




@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def deleteanunsiu(request,id):
    info = Anunsiu.objects.get(id=id)
    print("apaga")
    info.delete()
    messages.success(request,"Dados Apaga  Susessu..!")
    return redirect('informasaun:anunsiu')


