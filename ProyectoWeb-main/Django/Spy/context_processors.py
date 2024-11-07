from .models import Carrito

def carrito_context(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        items = carrito.items.all()
        total = sum(item.producto.precio * item.cantidad for item in items)
        return {
            'carrito_items': items,
            'carrito_total': total
        }
    return {
        'carrito_items': [],
        'carrito_total': 0
    }
