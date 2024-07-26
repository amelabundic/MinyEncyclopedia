from turtle import title
from django.shortcuts import redirect, render # type: ignore
from django.http import Http404, HttpResponseRedirect # type: ignore
from django.urls import reverse # type: ignore
import markdown2 # type: ignore
from .forms import CreatePageForm
from .forms import EditPageForm

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Home" 
    })

def entry_page(request, title):
    content = util.get_entry(title)
    html_content = markdown2.markdown(content)
    return render(request, 'encyclopedia/entry_page.html', {
        'title': title,
        'content': html_content,
    })

def create_page(request):
    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) is not None:
                return render(request, 'encyclopedia/error.html', {
                    'message': f'The page "{title}" already exists.'
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry_page', args=[title]))
    else:
        form = CreatePageForm()
    
    return render(request, 'encyclopedia/create_page.html', {
        'form': form
    })

def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry_page', title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            raise Http404("The requested page was not found.")
        form = EditPageForm(initial={'content': content})

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    random_title = util.get_random_title()
    return render(request, 'encyclopedia/random.html', {
        'random_title': random_title
    })

def search(request):
    query = request.GET.get('q', '')
    results = util.search_entries(query)
    if len(results) == 1 and query.lower() == results[0].lower():
        return redirect('entry_page', title=results[0])
    if results:
        return render(request, 'encyclopedia/search.html', {
            'query': query,
            'results': results
        })
    else:
        return render(request, 'encyclopedia/error.html', {
            'message': "No results found."
        })

def random_page(request):
    random_title = util.get_random_title()
    return HttpResponseRedirect(reverse('entry_page', args=[random_title]))
