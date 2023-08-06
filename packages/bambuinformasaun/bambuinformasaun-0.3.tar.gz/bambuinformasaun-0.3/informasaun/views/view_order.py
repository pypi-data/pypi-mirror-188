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
from django.db.models import Count,Sum
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
from vizitor.models import *
from main.decorators import login_ona, seidauk_login, allowed_users




@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def order(request):
    buka = False;
    bukatitle = "mamuk"
    

    if request.GET.__contains__('page') :
        page_num = request.GET.get('page')
    else:
        page_num = 1


    if request.GET.__contains__('pesquiza'):
        buka = True
        paginator = Paginator(Order.objects.order_by('id').filter(data__icontains=request.GET['pesquiza']), 1)
    else:
        paginator = Paginator(Order.objects.order_by('id'), 10)

    page_range = []
    for i in range(paginator.num_pages):
        page_range.append(i+1)
        data_Order = paginator.page(page_num)

        page_num_int = int(page_num)

    if buka :
        bukatitle = "Rezultadu Pesquiza husi <i>' (" + request.GET['pesquiza'] + ") '</i>"

    # data = []
    # lingua = Lingua.objects.all()
    # titulu = ""
    # for dadosinfo in data_Produtu :
    #     statuslingua = ""
    #     for dadoslingua in lingua : 
    #         konteudu = KonteuduProdutu.objects.filter(produtu = dadosinfo.produtu.id , lingua = dadoslingua.id).count()
    #         if konteudu > 0 :
    #             konteudu = KonteuduProdutu.objects.filter(produtu = dadosinfo.produtu.id , lingua = dadoslingua.id).last()
    #             # konteudu2 = KonteuduInformasaun.objects.filter(informasaun = dadosinfo.id , lingua = 1).last()
    #             titulu = konteudu.titulu
    #             statuslingua = statuslingua +  " <i><b>   <img src=" +dadoslingua.icon.url + " width='20px'> &nbsp; </b> </i> " + konteudu.titulu + "<br>"
    #         else :
    #             statuslingua = statuslingua +  "<i><b>   <img src=" +dadoslingua.icon.url + " width='20px'> &nbsp; </b> </i>  <font color ='red'> Laiha</font> <br>"
    #     data.append({'foun' : dadosinfo.produtu.foun,'presu' : dadosinfo.produtu.presu, 'kategoriaprodutu' : dadosinfo.produtu.kategoriaprodutu, 'imagen' : dadosinfo.produtu.imagen_main ,'lingua':dadoslingua.naran,'linguaicon' : dadoslingua.icon,'linguaid' : dadoslingua.id, 'statuslingua': statuslingua , 'data' : dadosinfo.produtu.data ,'titulu' : titulu , "id" : dadosinfo.produtu.id })


    context = {
        "pajina_order" : "active",
        "order" : data_Order,
        'bukatitle' : bukatitle,
        'page_range' : page_range,
        'current_page' : page_num_int,
    }
    return render(request, 'informasaun/order/lista.html',context)







@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def detallukonteuduorder(request,id):

    order = Order.objects.get(id = id)

    #konteudu lingua 

    listaorder =  ListaOrder.objects.filter(order__id = id)
    kliente =  User.objects.get(id = order.user_order.id)
    total_price = ListaOrder.objects.filter(order__id = id).aggregate(presu_order=Sum('presu_order'))
    order_seluk = Order.objects.filter(user_order = kliente.id)
    Order.objects.filter(id=id).update(status_hare=True) 


    context = {
        "id" : id,
        "asaun" : "input",
        "pajina_order" : "active",
        "listaorder" : listaorder,
        "kliente" : kliente,
        "order" : order,
        "total_price" : total_price['presu_order'],
        "order_seluk" : order_seluk,
    }
    return render(request, 'informasaun/order/detallukonteuduorder.html',context)



@login_ona
@allowed_users(allowed_roles=['adminbambu'])
def ordermandamensagenajax(request):

    mensagen =  request.POST['mensagen']
    ido =  request.POST['id']
  

    Order.objects.filter(id=ido).update(resposta=mensagen , status_resposta = True) 
    order = Order.objects.get(id=ido)
    context = {
        "asaun" : "input",
        "order" : order,
    }
    return render(request, 'informasaun/order/ajax_submitmensagen.html',context)


