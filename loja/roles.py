from rolepermissions.roles import AbstractUserRole


class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_produto': True,
        'liberar_desconto': True,
        'cadastrar_vendedor': True,
    }


class Vendedor(AbstractUserRole):
    available_permissions = {
        'realizar_venda': True,
    }
