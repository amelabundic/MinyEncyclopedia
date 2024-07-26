import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
import markdown2 # type: ignore
import re

from django.core.files.base import ContentFile # type: ignore
from django.core.files.storage import default_storage # type: ignore


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


"""
def save_entry(title, content):

    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

"""

def save_entry(title, content):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    # Convert content to bytes using utf-8 encoding
    content_bytes = content.encode('utf-8')
    default_storage.save(filename, ContentFile(content_bytes))


def search_entries(query):
    entries = list_entries()
    return [entry for entry in entries if query.lower() in entry.lower()]   

def get_random_title():
    entries = list_entries()
    if entries:
        return random.choice(entries)
    return None

def random_page(request):
        entries = list_entries()
        if entries:
           random_title = random.choice(entries)
           return HttpResponseRedirect('entry_page', args=[random_title])
        else:
            return render(request, 'error.html')

def get_entry(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        markdown_content = f.read().decode("utf-8")
        html_content = markdown2.markdown(markdown_content)
        return html_content
    except FileNotFoundError:
        return None 
    
   

   
        
