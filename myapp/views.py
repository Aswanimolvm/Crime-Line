from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Complaint, UserProfile, Feedback


# Guest Page
def guest_page(request):
    total_complaints = Complaint.objects.count()
    return render(request, 'user_guest.html', {'total_complaints': total_complaints})


# Signup
def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        UserProfile.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            date_of_birth=date_of_birth,
            email=email,
            password=make_password(password),
        )
        messages.success(request, "Sign-up successful! Please log in.")
        return redirect('login')

    return render(request, 'user_register.html')


# Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email

                if email == 'admin@gmail.com' and password == 'admin':
                    request.session['is_admin'] = True
                    return redirect('admin_dashboard')
                else:
                    return redirect('home_page')
            else:
                messages.error(request, "Incorrect password.")
        except UserProfile.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, 'user_login.html')


# Logout
def logout_view(request):
    request.session.flush()
    return redirect('guest')


# Delete User
def delete_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = UserProfile.objects.get(id=user_id)
        user.delete()
        request.session.flush()
        messages.success(request, "User deleted successfully.")
        return redirect('guest')
    except UserProfile.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('home_page')


# Home Page
def home_page(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        user_id = request.session.get('user_id')
        suggestion = request.POST.get('suggestion')

        if user_id and suggestion:
            user = UserProfile.objects.get(id=user_id)
            Feedback.objects.create(user=user, suggestion=suggestion)
            messages.success(request, "Thank you for your feedback!")
            return redirect('home_page')

    feedbacks = Feedback.objects.filter(is_visible=True).order_by('-submitted_at')
    total_complaints = Complaint.objects.count()

    return render(request, 'user_home.html', {
        'feedbacks': feedbacks,
        'total_complaints': total_complaints
    })



# Report Issue
def report_issue(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = UserProfile.objects.get(id=user_id)
        description = request.POST.get('description')
        complaint_type = request.POST.get('type')
        location = request.POST.get('location')
        proof = request.FILES.get('proof')

        Complaint.objects.create(
            user=user,
            description=description,
            complaint_type=complaint_type,
            location=location,
            proof=proof
        )

        return redirect('success')

    return render(request, 'user_complaint.html')


# Success Page
def success_view(request):
    return render(request, 'success.html')


# All Complaints by User
def all_complaints(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserProfile.objects.get(id=user_id)
    complaints = Complaint.objects.filter(user=user).order_by('-submitted_at')
    return render(request, 'all_complaints.html', {'complaints': complaints})


# About Page
def about(request):
    return render(request, 'about.html')


# Contact Page
def contact(request):
    return render(request, 'contact.html')


# Admin Dashboard
@login_required
def admin_dashboard(request):
    total = Complaint.objects.count()
    pending=Complaint.objects.filter(status='pending').count()
    resolved=Complaint.objects.filter(status='resolved').count()
    in_progress=Complaint.objects.filter(status='in_progress').count()
    status={
        'total_complaints': total,
        'pending_complaints': pending,
        'resolved_complaints': resolved,
        'in_progress_complaints': in_progress,
    }
    
    
        
    
    return render(request, 'admin_dashboard.html',status)


# Admin Complaints View
@login_required
def admin_complaints(request):
    complaints = Complaint.objects.all().order_by('-submitted_at')
    return render(request, 'admin_complaints.html', {'complaints': complaints})


# Feedback Page with Pagination (User Side)
def feedback_view(request):
    feedback_list = Feedback.objects.filter(is_visible=True).order_by('-submitted_at')
    paginator = Paginator(feedback_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'feedback.html', {'page_obj': page_obj})


# Admin Feedback List
@login_required
def admin_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'feedback_admin.html', {'feedbacks': feedback_list})


# Admin Toggle Feedback Visibility
@login_required
def toggle_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.is_visible = not feedback.is_visible
        feedback.save()
    return redirect('admin_feedback')


# Admin Delete Feedback
@login_required
def delete_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
    return redirect('admin_feedback')


# Edit Profile
@login_required
def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserProfile.objects.get(id=user_id)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.mobile_number = request.POST.get('mobile_number')
        user.email = request.POST.get('email')
        user.id_proof_number=request.POST.get('id_proof_number')
        user.address=request.POST.get('address')
        user.state=request.POST.get('state')
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('home_page')

    return render(request, 'user_profile.html', {'user': user})


def update_status(request, complaint_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserProfile.objects.get(id=user_id)

    if not user.is_admin:
        return redirect('home_page')  # or return 403 response

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Complaint.STATUS_CHOICES):  # If STATUS_CHOICES exists
            complaint.status = new_status
            complaint.save()

    return redirect('admin_complaints')

#delete Complaint
@login_required
def delete_complaint(request,complaint_id):
    if request.method == "POST":
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.delete()
    return redirect('admin_complaints')