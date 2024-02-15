from django.shortcuts import render, HttpResponse
from .utils import *

# Create your views here.


def home(request):
    return render(request, "app_for_bimamitra/home.html")
    #return HttpResponse("this is homepage.")
def about(request):
    return render(request, "app_for_bimamitra/about.html")

# def contactus(request):
#     return render(request, "app_for_bimamitra/contactus.html")

def bimabot(request):

    return render(request, "app_for_bimamitra/bimabot.html")


from .forms import ContactUsForm
def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # form.save()  # This will save the form data to the ContactUs model
            # Redirect to a success page or return a response
            return render(request, "app_for_bimamitra/contactus.html")  
    else:
        form = ContactUsForm()

    return render(request, 'app_for_bimamitra/contactus.html', {'form': form})



from .forms import InputForm
from .models import SearchRecord
def bimabot(request):
    chat_history = []
    response_text = None
    user='admin'
    
    if request.method == "POST":
        form = InputForm(request.POST)
        print("***************"*20)
        print("Form data:", request.POST)
        if form.is_valid():
            print("form is valid")
            user_input = form.cleaned_data['user_input']     
            response_text = generate_response_rag(user_input)
            # SearchRecord.objects.create(
            #         username = user,
            #         user_input=user_input,
            #         response=response_text
            #         )

            form=InputForm()
        else:
            print("form is invalid")
    else:
        
        form=InputForm()


    
    chat_db = SearchRecord.objects.filter(username=user)
    for i in chat_db:
        conversation_dict = {
                "You": i.user_input,
                "BimaBot": i.response
            }
        chat_history.insert(0,conversation_dict)
        
    
    return render(request, "app_for_bimamitra/bimabot.html", {'form':form, 'response': response_text, 'chat_history':chat_history})