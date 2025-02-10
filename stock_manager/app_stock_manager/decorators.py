from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Decorador para restringir acesso apenas a administradores."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Acesso negado. Você não tem permissão para acessar esta página.")
            return redirect("home")  # Redireciona para a página inicial (ou outra desejada)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
