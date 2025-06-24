from django.shortcuts import redirect

# Decorators para verificar se o usuário está logado
def user_login_required(view_func):
  def wrapper(request, *args, **kwargs):
    if 'user_id' in request.COOKIES:
      return view_func(request, *args, **kwargs)
    else:
      return redirect('login')
  return wrapper

def admin_login_required(view_func):
  def wrapper(request, *args, **kwargs):
        if 'admin_id' in request.COOKIES:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('admin')
  return wrapper