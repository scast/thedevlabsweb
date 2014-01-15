from .forms import TwitterSearchForm
def discover_form(req):
    return {'discover_form': TwitterSearchForm()}
