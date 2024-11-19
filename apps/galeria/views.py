from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.models import Fotografia
from django.contrib import messages
from apps.galeria.forms import FotografiaForms

# Em Index: order_by ordena as imagens que aparecem na página pela mais recente (colcar - antes de "data_fotografia" inverte a ordem). filter exibe apenas as que estejam com o campo booleano da tabela SQL publicada igual a True
def index(request):
    if not request.user.is_authenticated:
        messages.error( request, "Entre ou Cadastre-se para ver as fotografias")
        return redirect('login')
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    return render(request, "galeria/index.html", {"cards": fotografias})

def imagem(request, foto_id):
    if not request.user.is_authenticated:
        messages.error( request, "Entre ou Cadastre-se para ver as fotografias")
        return redirect('login')
    
    fotografia = get_object_or_404(Fotografia, pk = foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia":fotografia})

def buscar(request):
    if not request.user.is_authenticated:
        messages.error( request, "Entre ou Cadastre-se para ver as fotografias")
        return redirect('login')
    
    #O comando request.GET pega o que foi enviado pelo formulário cujo nome está entre []
    query = request.GET['buscar']
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            #campo da base dados a ser buscado seguido de __icontains mostra se existe alguma coisa em comum sem precisar ser exato
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)
            #Passar dados a serem enviados como dicionário
    return render(request, "galeria/buscar.html", {"cards": fotografias, "query":query})

def nova_imagem(request):
    if not request.user.is_authenticated:
        messages.error( request, "Entre ou Cadastre-se para cadastrar as fotografias")
        return redirect('login')
    
    form = FotografiaForms
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova fotografia cadastrada')
            return redirect ('index')



    return render (request, 'galeria/nova_imagem.html', {'form': form} )

def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)

    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia editada com sucesso')
            return redirect('index')


    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})

def excluir_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request, "Fotografia excluida com sucesso")
    return redirect('index')

def filtro(request, categoria):
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True, categoria=categoria)
    return render(request, 'galeria/index.html', {'cards': fotografias})
