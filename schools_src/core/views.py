import os
import time 
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings as django_settings
from django.contrib import messages  
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from schools.decorators import ajax_required 
from core.forms import ChangePasswordForm, ProfileFormHuman, ProfileFormProducts
from feeds.models import Feed
from feeds.views import FEEDS_NUM_PAGES, feeds
from PIL import Image
from authentication.models import Profile  
from core.forms import ProfilePhotoForm 
from feeds.models import Feed
from activities.models import Activity
       
def home(request):     
    print('inside home, core.view') 
    if request.user.is_authenticated():  
        return redirect('feeds') 
    else:
        return redirect('login')

def introho(request):
    print('inside introho, core.introho.view')
    print('gonna send introho via core.views.introho')
    all_profile_feeds = Feed.objects.all().filter(profile_pk__gt=0).exclude(user__profile__is_product=1)[:5]    
    all_product_profile_feeds = Feed.objects.all().filter(Q(profile_pk__gt=0) 
                                                & Q(user__profile__is_product=1))[:5]
    most_liked_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('likes').reverse()

    feeds = Feed.objects.all()
    if most_liked_challenge_feeds:
        most_liked_feed_today_id = most_liked_challenge_feeds[0].id
        most_liked_feed_today = get_object_or_404(Feed, id=most_liked_feed_today_id)
    elif feeds:
        feed = feeds[0]
        most_liked_feed_today_id = feed.id
        most_liked_feed_today = feed
    else: 
        most_liked_feed_today = None
        most_liked_feed_today_id = None

    if most_liked_feed_today_id:
        style_feeds = Feed.get_feeds().filter(response_for=most_liked_feed_today_id)
    else:
        style_feeds = []

    trending_style_copies = Feed.get_feeds().filter(response_for__gt=0)[:20]
    #schools_feeds = Feed.get_feeds().filter(user__username='schools')[0:20]
    return render(request, 'newsletter/introho.html', {
        'style_feeds': style_feeds,
        'all_profile_feeds': all_profile_feeds,
        'all_product_profile_feeds' : all_product_profile_feeds,
        'most_liked_feed_today': most_liked_feed_today,
        'most_liked_challenge_feeds' : most_liked_challenge_feeds,
        'trending_style_copies' : trending_style_copies,
        #'schools_feeds' : schools_feeds,
        })

@login_required
def network(request):
    print('inside network, core.view')
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try: 
        users = paginator.page(page)
    except PageNotAnInteger: 
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'core/network.html', {'users': users})


@login_required(login_url='/login/')
def profile(request, username):   
    page_user = get_object_or_404(User, username=username)
    print('inside profile, core.view')
    print('gonna send user_profile_feeds via core.views.profile')
    print('profile_pk is %d'%(page_user.profile.pk))
    profile_pk = page_user.profile.pk
    profile_page = 'core/student-profile.html'

    if page_user.profile.is_student:
        profile_page = 'core/student-profile.html'
    elif page_user.profile.is_teacher:
        profile_page = 'core/teacher-profile.html'
    elif page_user.profile.is_product:
        profile_page = 'core/main.html' 
     
    # making profile feeds pagewise
    profile_feeds = Feed.get_feeds().filter(user__id=profile_pk)
    paginator_profile = Paginator(profile_feeds, FEEDS_NUM_PAGES)
    profile_feeds = paginator_profile.page(1)
    for feed in profile_feeds:
        print('feed.pk %d, profile_pk %d'%(feed.pk,profile_pk))
    from_feed = -1
    if profile_feeds:
        from_feed = profile_feeds[0].id
    return render(request, profile_page, {
        'page_user': page_user,
        # 'user_feeds': user_feeds,
        # 'from_feed_user': from_feed_user, I'll make different view for user feeds
        # 'from_feed_profile':from_feed_profile, # no need to do that
        'from_feed':from_feed, # just maintain same name from_feed this will make work of feeds.load view easy
        'profile_feeds':profile_feeds, 
        'page': 1
        })

@login_required
def userfeeds(request, username): 
    print('gonna send user_feeds via core.views.userfeeds')  
    page_user = get_object_or_404(User, username=username)
    # for user specific feed
    user_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(user_feeds, FEEDS_NUM_PAGES)
    user_feeds = paginator.page(1)
    for feed in user_feeds:
        print('feed.pk %d'%(feed.pk))    
    from_feed = -1
    if user_feeds:
        from_feed = user_feeds[0].id

    return render(request, 'core/user_feeds.html', {
        'page_user': page_user,
        'user_feeds': user_feeds,
        'from_feed': from_feed,
        'page': 1
        })



@login_required 
def settings_human(request):
    print('inside settings, core.view')
    # likers = User.objects.all.filter()
    user = request.user
    if request.method == 'POST':
        form = ProfileFormHuman(request.POST) 
        if form.is_valid():
            # csrf_token = form.cleaned_data.get('_token');
            user.profile.status = form.cleaned_data.get('status')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')

            user.profile.want_to_do = form.cleaned_data.get('want_to_do')
            user.profile.likes_most = form.cleaned_data.get('likes_most')
            user.profile.likes_not = form.cleaned_data.get('likes_not') 

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.home = form.cleaned_data.get('home')
            user.profile.job = form.cleaned_data.get('job')
            user.profile.institute = form.cleaned_data.get('institute')
            user.profile.enrolled = form.cleaned_data.get('enrolled')
            user.profile.year = form.cleaned_data.get('year')
            user.profile.completed = form.cleaned_data.get('completed')

            user.email = form.cleaned_data.get('email')
            user.profile.website = form.cleaned_data.get('website')
            user.profile.facebook = form.cleaned_data.get('facebook')
            user.profile.quora = form.cleaned_data.get('quora')
            user.profile.twitter = form.cleaned_data.get('twitter')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileFormHuman(instance=user, initial={
            'job': user.profile.job,
            'website': user.profile.website,
            'email' : user.email,
            'home': user.profile.home,
            'status':user.profile.status,
            'institute': user.profile.institute,
            'birth_date': user.profile.birth_date,
            'facebook' : user.profile.facebook,
            'quora' : user.profile.quora,
            'twitter' : user.profile.twitter,
            'linkedin': user.profile.linkedin,
            'want_to_do' : user.profile.want_to_do,
            'likes_most' : user.profile.likes_most,
            'likes_not' : user.profile.likes_not,
            
            'enrolled' : user.profile.enrolled,
            'year' : user.profile.year,
            'completed' : user.profile.completed,
            'skills' : user.profile.skills,
            })
    return render(request, 'core/settings_human.html', {'form': form, 'page_user':user})

@login_required 
def settings_products(request):
    print('inside settings, core.view')
    user = request.user
    if request.method == 'POST': 
        form = ProfileFormProducts(request.POST)
        if form.is_valid():
            # csrf_token = form.cleaned_data.get('_token');
            user.profile.status = form.cleaned_data.get('status')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.home = form.cleaned_data.get('home')
            user.profile.job = form.cleaned_data.get('job')
            user.profile.company = form.cleaned_data.get('company')
            user.email = form.cleaned_data.get('email')
            user.profile.website = form.cleaned_data.get('website')
            user.profile.facebook = form.cleaned_data.get('facebook')
            user.profile.quora = form.cleaned_data.get('quora')
            user.profile.twitter = form.cleaned_data.get('twitter')
            user.profile.linkedin = form.cleaned_data.get('linkedin')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileFormProducts(instance=user, initial={
            'job': user.profile.job,
            'website': user.profile.website,
            'email' : user.email,
            'home': user.profile.home,
            'status':user.profile.status,
            'company': user.profile.company,
            'birth_date': user.profile.birth_date,
            'facebook' : user.profile.facebook,
            'quora' : user.profile.quora,
            'twitter' : user.profile.twitter,
            'linkedin' : user.profile.linkedin,
            })
    return render(request, 'core/settings_products.html', {'form': form, 'page_user':user})


# @login_required
# def picture(request): 
#     print('inside picture, core.view')  
#     uploaded_picture = False
#     try:
#         if request.GET.get('upload_picture') == 'uploaded':
#             uploaded_picture = True

#     except Exception:
#         pass

#     return render(request, 'core/picture.html',
#                   {'uploaded_picture': uploaded_picture})


@login_required
def password(request):
    print('inside password, core.view')
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('password')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form, 'page_user':user})


# @login_required
# def upload_picture(request): 
#     print('inside upload_picture, core.view')
#     try:
#         profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
#         if not os.path.exists(profile_pictures):
#             os.makedirs(profile_pictures)
#         f = request.FILES['picture']
#         filename = profile_pictures + request.user.username + '_tmp.jpg'
#         with open(filename, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
#         im = Image.open(filename)
#         width, height = im.size

#         if width > 0:
#             new_width = 450
#             new_height = (height * 450) / width
#             new_size = new_width, new_height
#             im.thumbnail(new_size, Image.ANTIALIAS)
#             im.save(filename)
#         return redirect('/settings/picture/?upload_picture=uploaded')

#     except Exception as e:
#         print(e)
#         return redirect('/settings/picture/')


# @login_required
# def save_uploaded_picture(request):
#     print('inside save_uploaded_picture, core.view')
#     try:
#         x = int(request.POST.get('x'))
#         y = int(request.POST.get('y'))
#         w = int(request.POST.get('w'))
#         h = int(request.POST.get('h'))
#         tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
#             request.user.username + '_tmp.jpg'
#         filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
#             request.user.username + '.jpg'
#         im = Image.open(tmp_filename)
#         cropped_im = im.crop((x, y, w+x, h+y))
#         cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
#         cropped_im.save(filename)
#         os.remove(tmp_filename)

#     except Exception:
#         pass
 
#     return redirect('/settings/picture/')

@login_required
def picture(request):
    return render(request,'core/picture.html',{})

@login_required
def profile_pic_upload(request):
    print('inside profile_pic_upload, core.view')
    instance = get_object_or_404(Profile, id=request.user.profile.id)
    form = ProfilePhotoForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        profile = form.save()
        data = {'is_valid': True, 'name': profile.image.name, 'url': profile.image.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)
 
@login_required
def profile_likers(request, username):
    print('inside profile_likers, core.view')
    page_user = get_object_or_404(User, username=username)
    for user in page_user.profile.get_likers():
        print(user.username)

    return render(request, 'core/profile_likers.html', {'page_user': page_user})

@login_required
def likes_to(request, username):
    print('inside likes_to, core.view')
    page_user = get_object_or_404(User, username=username)
    all_users = User.objects.all()
    likes_to_users = []
    for user in all_users:
        if page_user in user.profile.get_likers():
            likes_to_users.append(user)
    for user in likes_to_users:
        print(user.username)

    return render(request, 'core/likes_to.html', {'page_user': page_user,'likes_to_users':likes_to_users})


@login_required
def profile_unlike(request, username): # this username will be of user who had liked you as in notification
    print('inside profile_like, feeds.view')
    user = get_object_or_404(User, username=username)
    profile_pk = request.user.profile.id
    profile= get_object_or_404(Profile, user=request.user)

    like = Activity.objects.filter(activity_type=Activity.LIKE_PROFILE, profile=profile_pk,
                                   user=user)
    if like: # it'll be always true
        user.profile.unotify_liked_profile(profile)
        print('request user: %s had already liked this user so \
            you are gonna be removed from the liker list of this user\
            and It should appear Like text on button'
            %(user.username))
        like.delete()
        
    messages.add_message(request, messages.SUCCESS,'You unliked this user, Like to interact!')
    return redirect('/%s/'%(request.user.username))
