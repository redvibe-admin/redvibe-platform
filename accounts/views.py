from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from core.models import Post, Comment, Report
from core.forms import CommentForm  # Ensure this exists in core/forms.py

from moviepy.editor import VideoFileClip
import tempfile, os
import json

# ----------------------------
# Helper: check if file is video
# ----------------------------
def _is_video_file(file_field):
    if not file_field:
        return False
    name = str(getattr(file_field, 'name', '')).lower()
    return name.endswith(('.mp4', '.mov', '.avi', '.webm', '.m4v'))


# ----------------------------
# Home / Feed
# ----------------------------
def home(request):
    watched = request.session.get('watched_posts', [])
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(creator=request.user).order_by('-created_at')
        others_posts = Post.objects.exclude(id__in=watched).exclude(creator=request.user).order_by('-created_at')
        posts = list(user_posts) + list(others_posts)
    else:
        posts = list(Post.objects.exclude(id__in=watched).order_by('-created_at'))

    for post in posts:
        post.is_video = _is_video_file(post.file)

    return render(request, 'core/home.html', {'posts': posts})


# ----------------------------
# Reels Page
# ----------------------------
def reels_view(request):
    watched = request.session.get('watched_posts', [])
    posts_qs = Post.objects.exclude(id__in=watched).order_by('-created_at')
    posts = list(posts_qs)
    for post in posts:
        post.is_video = _is_video_file(post.file)
    return render(request, 'core/reels.html', {'posts': posts})


# ----------------------------
# Upload Page
# ----------------------------
@login_required
def upload_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in ['.mp4', '.mov', '.jpg', '.jpeg', '.png', '.webm']:
            messages.error(request, "Unsupported file type.")
            return redirect('upload')

        if file.size > 100 * 1024 * 1024:
            messages.error(request, "File size exceeds 100MB.")
            return redirect('upload')

        if ext in ['.mp4', '.mov', '.webm']:
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in file.chunks():
                        temp_file.write(chunk)
                    temp_path = temp_file.name

                clip = VideoFileClip(temp_path)
                if clip.duration > 120:
                    messages.error(request, "Video duration exceeds 120 seconds.")
                    clip.close()
                    os.remove(temp_path)
                    return redirect('upload')

                clip.close()
                os.remove(temp_path)
            except Exception as e:
                messages.error(request, f"Error processing video: {e}")
                return redirect('upload')

        Post.objects.create(
            creator=request.user,
            file=file,
            description=request.POST.get('description', '')
        )
        messages.success(request, "Upload successful!")
        return redirect('home')

    return render(request, 'core/upload.html')


# ----------------------------
# Mark watched (AJAX)
# ----------------------------
@require_POST
def mark_watched(request):
    try:
        data = json.loads(request.body.decode('utf-8')) if request.content_type == 'application/json' else request.POST
        post_id = int(data.get('post_id'))
    except Exception:
        return HttpResponseBadRequest("Invalid post_id")

    watched = request.session.get('watched_posts', [])
    if post_id not in watched:
        watched.append(post_id)
        request.session['watched_posts'] = watched
        request.session.modified = True

    return JsonResponse({'status': 'ok', 'watched_count': len(watched)})


# ----------------------------
# Signup
# ----------------------------
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created and logged in.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


# ----------------------------
# View single post
# ----------------------------
def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.is_video = _is_video_file(post.file)
    comment_form = CommentForm()
    return render(request, 'core/view_post.html', {'post': post, 'comment_form': comment_form})


# ----------------------------
# Comment on post
# ----------------------------
@login_required
def comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(post=post, user=request.user, text=form.cleaned_data['text'])
    return redirect(f'/post/{pk}/')


# ----------------------------
# Like / Unlike
# ----------------------------
@login_required
def like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        status = 'unliked'
    else:
        post.likes.add(request.user)
        status = 'liked'
    return JsonResponse({'status': status})


# ----------------------------
# Report post
# ----------------------------
@login_required
def report_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        Report.objects.create(
            post=post,
            reporter=request.user,
            reason=request.POST.get('reason'),
            details=request.POST.get('details', '')
        )
        messages.info(request, "Thank you for your report.")
        return redirect(f'/post/{pk}/')
    return redirect('/')


# ----------------------------
# Admin Dashboard
# ----------------------------
def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'core/admin_dashboard.html', {'reports': reports})


# ----------------------------
# About / Contact
# ----------------------------
def about(request):
    return render(request, 'core/about.html')


def contact_view(request):
    return render(request, 'core/contact.html')


# ----------------------------
# Profile
# ----------------------------
@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(creator=profile_user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'profile_user': profile_user, 'posts': posts})
