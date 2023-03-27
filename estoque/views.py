import sys
from datetime import date
from io import BytesIO

from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from PIL import Image, ImageDraw
from rolepermissions.decorators import has_permission_decorator

from .forms import ProdutoForm
from .models import Categoria, Imagem, Produto


# Create your views here.
@has_permission_decorator('cadastrar_produtos')
def add_produto(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        categoria = request.GET.get('categoria')
        preco_min = request.GET.get('preco_min')
        preco_max = request.GET.get('preco_max')

        produtos = Produto.objects.all()
        if nome or categoria or preco_min or preco_max:
            if not preco_min:
                preco_min = 0

            if not preco_max:
                preco_max = 999999999

            if nome:
                produtos = produtos.filter(nome__icontains=nome)

            if categoria:
                produtos = produtos.filter(categoria=categoria)

            produtos = produtos.filter(preco_venda__gte=preco_min).filter(
                preco_venda__lte=preco_max)

        categoria = Categoria.objects.all()

        return render(request, 'add_produto.html', {'categoria': categoria, 'produtos': produtos})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        preco_compra = request.POST.get('preco_compra')
        preco_venda = request.POST.get('preco_venda')
        imagens = request.FILES.getlist('imagens')

        produto = Produto(
            nome=nome,
            categoria_id=categoria,
            quantidade=quantidade,
            preco_compra=preco_compra,
            preco_venda=preco_venda
        )
        produto.save()

        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img)
            draw.text(
                (20, 280), f'Propriedade de Loja em {date.today()}', (255, 255, 255))

            output = BytesIO()  # salvar o arquivo configurado em bytes -> não salva na memoria
            img.save(output, format="JPEG", quality=100)
            # retorna o ponteiro para o começo do arquivo da imagem NECESSARIO
            output.seek(0)
            img_final = InMemoryUploadedFile(  # converte usando o InMemoryUploadedFiel
                output,
                'ImageField',
                name,
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
            img_dj = Imagem(
                imagem=img_final,
                produto=produto
            )
            img_dj.save()
        messages.add_message(request, messages.SUCCESS,
                             'Produto adicionado com sucesso')
        # reverse usa o name do url definido no path
        return redirect(reverse('add_produto'))


def produto(request, slug):
    if request.method == "GET":
        produto = Produto.objects.get(slug=slug)
        data = produto.__dict__
        data['categoria'] = produto.categoria.id
        # traz as informações que estão cadastradas
        form = ProdutoForm(initial=data)
        return render(request, 'produto.html', {
            'form': form
        })
