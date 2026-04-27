from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ExamFormSubmission


# ─── LOGIN ────────────────────────────────────────────────────────────────────
def login_view(request):
    """
    Handles GET (show form) and POST (validate credentials).
    If already logged in, redirect straight to dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'exams/login.html')


# ─── LOGOUT ───────────────────────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
@login_required(login_url='login')   # Redirects to login if not authenticated
def dashboard(request):
    """
    Simple dashboard. Shows student name and a button to fill the exam form.
    Also shows previously submitted forms.
    """
    user_forms = request.user.exam_forms.all().order_by('-submitted_at')
    return render(request, 'exams/dashboard.html', {'user_forms': user_forms})


# ─── EXAM FORM ────────────────────────────────────────────────────────────────
@login_required(login_url='login')
def exam_form_view(request):
    """
    GET  → Show the blank exam form.
    POST → Validate and save to DB, then redirect to success page.
    """
    if request.method == 'POST':
        form = ExamFormSubmission(request.POST)
        if form.is_valid():
            exam_entry = form.save(commit=False)   # Don't hit DB yet
            exam_entry.student = request.user      # Attach the logged-in student
            exam_entry.save()                      # Now save to DB
            messages.success(request, 'Exam form submitted successfully!')
            return redirect('success')
    else:
        # Pre-fill Full Name from the user's profile if available
        initial_data = {
            'full_name': request.user.get_full_name() or request.user.username
        }
        form = ExamFormSubmission(initial=initial_data)

    return render(request, 'exams/exam_form.html', {'form': form})


# ─── SUCCESS PAGE ─────────────────────────────────────────────────────────────
@login_required(login_url='login')
def success_view(request):
    return render(request, 'exams/success.html')
