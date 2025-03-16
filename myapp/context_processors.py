from .forms import ProductSearchForm

def search_form_context(request):
    return {'search_form': ProductSearchForm()}
