from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class Categoria(models.Model):
    titulo = models.CharField(max_length=40)

    def __str__(self):
        return self.titulo


class Produto(models.Model):
    nome = models.CharField(max_length=40, unique=True)
    categoria = models.ForeignKey(
        'Categoria', on_delete=models.SET_NULL, null=True)
    quantidade = models.FloatField()
    preco_compra = models.FloatField()
    preco_venda = models.FloatField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # executa um save personalizdo para criar slug
            self.slug = slugify(self.nome)

        # chama o save da classe models.model padrão
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    def gerar_desconto(self, desconto):
        return self.preco_venda - ((self.preco_venda * desconto)/100)

    def lucro(self):
        lucro = self.preco_venda - self.preco_compra
        return (lucro * 100)/self.preco_compra


class Imagem(models.Model):
    imagem = models.ImageField(upload_to="imagem_produto")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
