from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request, "home.html")

def labs(request):
  return render(request, "labs.html")

def projects(request):
  return render(request, "projects.html")

def tutoring(request):
  return render(request, "tutoring.html")
