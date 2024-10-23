from django.shortcuts import render, redirect
from .forms import EntryForm
from random import choice
from . import util
import markdown


def index(request):
    """Returns all existing entries"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """Returns content of existing entries in HTML page"""
    entry_content = util.get_entry(title)
    
    if entry_content is None:
        return render(request, "encyclopedia/404.html", {"message": "Page not found"})
    
    if entry_content:
        entry_content_html = markdown.markdown(entry_content) 
        return render(request, 'encyclopedia/entry.html', {  
            'title': title,
            'content': entry_content_html
        })
        
def search(request):
    """Let's user search for existing markdown entries and return partial matches"""
    entry_title = request.GET.get('q') 
    all_entries = util.list_entries()  
    
    if entry_title.lower() in [entry.lower() for entry in all_entries]:
        return render(request, 'encyclopedia/entry.html', {
            'title': entry_title,
            'content': markdown.markdown(util.get_entry(entry_title))
        })
             
    else:
        matching_entries = []
        for entry in all_entries:
            if entry_title.lower() in entry.lower(): 
                matching_entries.append(entry)
       
        return render(request, 'encyclopedia/search_entries.html', {
            'query': entry_title,  
            'matching_entries': matching_entries  
        })


def new_entry(request):
    """ Let's user create a new markdown entry via a Django/HTML form"""
    entries = util.list_entries()
    
    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if entry_title in entries:
                return render(request, 'encyclopedia/404.html', {"message": "Page already exists"})
            
            else:
                content_with_title = f"# {entry_title}\n\n{content}"
                util.save_entry(entry_title, content_with_title) 
                return redirect('entry', title=entry_title) 
    else:
        form = EntryForm()
              
    return render(request, 'encyclopedia/new_entry.html', {
            'form': form 
    })

def edit(request, title):
    """ Let's user edit an existing markdown entry via HTML form"""
    content = util.get_entry(title.strip()) 

    if content is None:
        return render(request, "encyclopedia/404.html", {"message": "Page not found"})
    
    if content.startswith(f"# {title}\n"):
        content = content[len(f"# {title}\n\n"):].strip()
    
    if request.method == "GET":
        form = EntryForm(initial={"title": title, "content": content})
        return render(request, "encyclopedia/edit.html", {"form": form, "title": title})
    
    elif request.method == "POST":
        form = EntryForm(request.POST)
             
        if form.is_valid():
            entry_title = title
            content = form.cleaned_data["content"]
        
            content_with_title = f"# {entry_title}\n\n{content}"
            util.save_entry(entry_title, content_with_title) 
            return redirect('entry', title=entry_title) 
        
    return render(request, "encyclopedia/edit.html", {"form": form, "title": title})

def random(request):
    """ Returns a random entry page"""
    entries = util.list_entries()
        
    return redirect("entry", title=choice(entries))

