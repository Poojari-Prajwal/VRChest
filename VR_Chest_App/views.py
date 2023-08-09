from django.shortcuts import get_object_or_404, render, redirect
from .models import Feedback, Appointment, Gallery_Image, Review, Article, Doctor, DoctorLeave
# import googlemaps
# import pandas as pd
import calendar
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import DoctorLeaveForm, ReviewForm, ArticleForm
from datetime import date, datetime
from slugify import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import json

# Create your views here.
def home(request):
    images = Gallery_Image.objects.all()
    reviews = Review.objects.all()
    return render(request,'home.html', {'images':images, 'reviews':reviews})

def saveFeedback(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        msg=request.POST.get('msg')
        obj = Feedback (Name = name, Email=email, Messege=msg)
        obj.save()  
        subject = 'VR Chest and Women Care'
        msg='Dear '+name+',\nThank you for your valueable feedback!\n\n Regards, \n VR Chest and Women Care'
        # send_mail(subject, msg , 'support@vrchestandwomencare.com', [email], fail_silently=True)
        messages.success(request,'Thanks for your valuable feedback!')
        return redirect('/')

def appointment(request):
    return render(request, 'appointment.html')

def appointmentConfirm(request):
    if request.method=='POST':
        name=request.POST.get('name')
        contact=request.POST.get('mobileno')
        email=request.POST.get('email')
        date=request.POST.get('date')
        time_slots=request.POST.get('timeSlot')
        doctor=request.POST.get('doctor')
        try:
            obj = Appointment(Name=name,Mobileno=contact, Email=email, Date=date, TimeSlots=time_slots, Doctor=doctor)
            obj.save()
            subject = 'Appointment Confirmed - VR Chest and Women Care'
            msg = 'Dear '+ name + ', \n\nYour appointment with '+ doctor+ ' is scheduled for '+ str(date)+ ' at '+ str(time_slots)+ '. Please arrive 15 minutes early to our hospital. We look forward to seeing you soon.\n\n Regards, \n VR Chest and Women Care'
            # send_mail(subject, msg, 'support@vrchestandwomencare.com', [email])
            messages.success(request,'Appointment Confirmed!')
        except Exception as e:
            messages.error(request,'Failed to confirm the appointment.')
        return redirect('/')


def get_available_time_slots(request):
    if request.method == "GET":
        selected_date = request.GET.get("date")
        doctor = request.GET.get("doctor")

        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        # Get the leave dates for the selected doctor
        doctor_obj = Doctor.objects.get(name=doctor)
        doctor_leave_dates = DoctorLeave.objects.filter(doctor=doctor_obj).values_list("leave_date", flat=True)
        
        if selected_date in doctor_leave_dates:
            return JsonResponse({"message": "Doctor is on leave"}, safe=False)  # Return an empty list to indicate no available slots for doctor's leave
        
        # Get the appointments for the selected date and doctor
        appointments = Appointment.objects.filter(Date=selected_date, Doctor=doctor)
        # Get the available slots for the selected doctor
        available_slots = get_doctor_time_slots(doctor)
        if appointments:
            # If there are existing appointments, mark the corresponding time slots as unavailable
            for appointment in appointments:
                for slot in available_slots:
                    if slot["time_slot"] in appointment.TimeSlots:
                        slot["is_available"] = False
        return JsonResponse(available_slots, safe=False)
    else:
        return HttpResponseNotAllowed(["GET"])


#Update appointment
def update_appointment(request, id):
    if request.method == "POST":
        try:
            appointment = Appointment.objects.get(id=id)
            appointment.Date = request.POST.get('date')
            appointment.TimeSlots = request.POST.get('timeSlot')
            appointment.save()
            subject = 'Appointment Updated - VR Chest and Women Care.'
            msg = 'Dear '+ appointment.Name + ', \nWe have updated your appointment request with '+ appointment.Doctor+ ' on '+ str(appointment.Date)+ ' at '+ str(appointment.TimeSlots)+ '. Please arrive 15 minutes early to our hospital. We look forward to seeing you soon.\n\n Regards, \n VR Chest and Women Care'
            # try:
            #     # send_mail(subject, msg, 'support@vrchestandwomencare.com', [appointment.Email])
            # except Exception as e:
            #     return redirect(reverse('show-upcoming-appointments') + '?message=success')
        except Exception as e:
            return redirect(reverse('show-upcoming-appointments') + '?message=error')
    else:
        return redirect('/show-upcoming-appointments')


# Returns respective time slots for doctor
def get_doctor_time_slots(doctor):
    doctor_time_slots = {
        "Dr. Vasunethra Kasargod": [
            {"time_slot": "5pm", "is_available": True},
            {"time_slot": "5:30pm", "is_available": True},
            {"time_slot": "6pm", "is_available": True},
            {"time_slot": "6:30pm", "is_available": True},
            {"time_slot": "7pm", "is_available": True},
            {"time_slot": "7:30pm", "is_available": True},
            {"time_slot": "8pm", "is_available": True},
            {"time_slot": "8:30pm", "is_available": True},
        ],
        "Dr. Veni N": [
            {"time_slot": "11am", "is_available": True},
            {"time_slot": "11:30am", "is_available": True},
            {"time_slot": "12pm", "is_available": True},
            {"time_slot": "12:30pm", "is_available": True},
            {"time_slot": "1pm", "is_available": True},
            {"time_slot": "1:30pm", "is_available": True},
            {"time_slot": "4pm", "is_available": True},
            {"time_slot": "4:30pm", "is_available": True},
            {"time_slot": "5pm", "is_available": True},
            {"time_slot": "5:30pm", "is_available": True},
            {"time_slot": "6pm", "is_available": True},
            {"time_slot": "6:30pm", "is_available": True},
        ],
    }
    return doctor_time_slots[doctor]

@csrf_exempt
def logins(request):
    if request.method=='POST' :
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('staff')
        else :
            messages.info(request,'Invalid Credentials!')
            return redirect('login')
    else :
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'Succesfully logged out!')
    return redirect('/')


@login_required(login_url='/login')
@csrf_exempt
def staff(request):
    return render(request, 'staff.html')


@login_required(login_url = '/login')
def showAppointments (request):
    all_appointments = Appointment.objects.all() 
    return render(request, 'showAppointments.html', {'all_appointments':all_appointments})


@login_required(login_url='/login')
@csrf_exempt
def bookAppointmentStaffVasu(request):
    return render ( request, 'vasuStaff.html')

@login_required(login_url='/login')
@csrf_exempt
def bookAppointmentStaffVeni(request):
    return render ( request, 'veniStaff.html')

@login_required(login_url='/login')
@csrf_exempt
def bookAppointmentStaffConfirm(request):
    if request.method=='POST':
        name=request.POST.get('name')
        contact=request.POST.get('mobileno')
        email=request.POST.get('email')
        date=request.POST.get('date')
        time_slots=request.POST.get('timeSlot')
        doctor=request.POST.get('doctor')
        try:
            obj= Appointment(Name=name,Mobileno=contact, Email=email, Date=date, TimeSlots=time_slots, Doctor=doctor)
            obj.save()
            messages.success(request,'Appointment Request Sent!')
        except Exception as e:
            messages.error(request,'Failed to send the appointment request.')
        return redirect('staff')

@login_required(login_url='/login')
@csrf_exempt
def showTodayAppointments(request):
    all_appointments = Appointment.objects.filter(Date=date.today()) 
    return render(request, 'todayAppointments.html', {'all_appointments':all_appointments})


@login_required(login_url='/login')
@csrf_exempt
def showUpcomingAppointments(request):
    all_appointments = Appointment.objects.all() 
    app_all_new=[]
    for a in all_appointments:
        if a.Date >= date.today():
            app_all_new.append(a)
    return render(request, 'showUpcomingAppointments.html', {'app_all_new':app_all_new})           
   

@login_required(login_url='/login')
@csrf_exempt
def showGalleryImages(request):
    images = Gallery_Image.objects.all()
    return render(request,'showGallery.html',{'images':images})


@login_required(login_url='/login')
@csrf_exempt
def deleteGalleryImages(request):
    try:
        delete_id = request.GET.get('s_id')
        delete_image = Gallery_Image.objects.get(id=delete_id)
        delete_image.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
@csrf_exempt
def addGalleryImages(request):
    if request.method=="POST":   
        img= request.FILES['uploadedImage']
        obj=Gallery_Image(Image=img)
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
@csrf_exempt
def addReviews(request):
    return render(request, 'addReview.html')


@login_required(login_url='/login')
@csrf_exempt
def submitReview(request):
    if request.method=='POST':
        name= request.POST.get("name")
        review= request.POST.get("review")
        rating= request.POST.get("rating")
        obj= Review(Review_text=review, Review_username=name, rating=rating)
        obj.save()
        return redirect('/staff')


@login_required(login_url='/login')
@csrf_exempt
def editOrDeleteReviews(request):
    reviews = Review.objects.all()
    return render(request,'showReview.html',{'reviews':reviews})


@login_required(login_url='/login')
@csrf_exempt
def deleteReview(request):
    try:
        delete_id = request.GET.get('s_id')
        delete_review = Review.objects.get(id=delete_id)
        delete_review.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
@csrf_exempt
def showFeedback(request):
    feedbacks=Feedback.objects.all()
    return render(request,'showFeedback.html' ,{'feedbacks':feedbacks})

@login_required(login_url='/login')
@csrf_exempt
def doctorLeaveApply(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor')
        dates = request.POST.get('dates')

        if doctor_name and dates:
            doctor, _ = Doctor.objects.get_or_create(name=doctor_name)
            dates_list = dates.split(',')
            for date_str in dates_list:
                DoctorLeave.objects.create(doctor=doctor, leave_date=date_str.strip())
            return redirect('staff')

    # Render the form template
    return render(request,'doctorLeaveApply.html')


@login_required(login_url='/login')
@csrf_exempt
def delete_doctor_leave(request, pk):
    doctor_leave = get_object_or_404(DoctorLeave, pk=pk)
    if request.method == 'POST':
        doctor_leave.delete()
    return redirect('show-doctor-leaves')


@login_required(login_url='/login')
@csrf_exempt
def doctorLeaveDisplay(request):
    doctor_leaves= DoctorLeave.objects.all()
    return render(request, 'showDoctorLeave.html',{'doctor_leaves':doctor_leaves})


@login_required(login_url='/login')
@csrf_exempt
def deleteFeedback(request):
    try:
        delete_id = request.GET.get('s_id')
        delete_feedback = Feedback.objects.get(id=delete_id)
        delete_feedback.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
@csrf_exempt
def editReview(request, review_id):
    review= Review.objects.get(id=review_id)
    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid():
        form.save()
        return redirect("edit-or-delete-reviews")
    return render(request, 'editReviews.html',{'review':review, 'form':form})
 

def facilities(request):
    return render(request, 'facilities.html')

def gallery(request):
    images = Gallery_Image.objects.all()
    return render(request,'gallery.html',{'images':images})


@login_required(login_url='/login')
@csrf_exempt
def addArticle(request):
    return render(request, 'addArticle.html')


@login_required(login_url='/login')
@csrf_exempt
def editOrDeleteArticle(request):
    articles= Article.objects.all()
    return render(request, 'showArticles.html',{'articles':articles})


@login_required(login_url='/login')
@csrf_exempt
def deleteArticle(request):
    try:
        delete_id = request.GET.get('a_id')
        delete_article = Article.objects.get(id=delete_id)
        delete_article.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
@csrf_exempt
def editArticle(request, article_id):
    article= Article.objects.get(id=article_id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect("edit-or-delete-article")
    return render(request, 'editArticles.html',{'article':article, 'form':form})


@login_required(login_url='/login')
@csrf_exempt
def submitArticle(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        link = request.POST.get('link')
        slug = slugify(title)
        obj= Article(title=title, content=content,slug=slug, link=link)
        obj.save()
        return redirect('/staff')


def articles(request):
    obj=Article.objects.all()
    return render(request,'articles.html', {'articles':obj})


def individualArticle(request, article_slug):
    obj=Article.objects.get(slug=article_slug)
    l = [obj]
    return render(request, 'individualArticle.html', {'articles':l})

def vasuAppointments(request):
    return render(request,'vasuAppointments.html')

def veniAppointments(request):
    return render(request, 'veniAppointments.html')
        
def pageNotFound(request, exception):
    return render(request, '404.html', status=404)

    