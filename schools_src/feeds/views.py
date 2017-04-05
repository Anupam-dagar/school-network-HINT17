import json  
import time, datetime 
from django.contrib.auth.models import User 
from os.path import splitext, basename
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.template.loader import render_to_string

from activities.models import Activity
from schools.decorators import ajax_required
from feeds.models import Feed 
from feeds.forms import PhotoForm,FeedForm  
from authentication.models import Profile 

  
FEEDS_NUM_PAGES = 10     
     
@login_required 
def feeds(request):
    print('inside feeds, feeds.view')
    print('gonna send style_feeds via feeds.views.feeds') 
    all_feeds = Feed.objects.all()

    return render(request, 'feeds/all_feeds.html', {
        'all_feeds' : all_feeds,
        'page': 1,
        })

@login_required 
def specialfeeds(request,id):
    print('inside feeds, feeds.view')
    print('gonna send special style_feeds via feeds.views.feeds')
    online_users = User.objects.all().exclude(is_active=True)
    challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                )
    response_for = id
    print('response_for id : %s'%response_for)
    style_feeds = Feed.get_feeds().filter(response_for=response_for)# 2nd lookup excludes all challenge feeds as they have is_challenge set to 1

    paginator = Paginator(style_feeds, FEEDS_NUM_PAGES)
    style_feeds = paginator.page(1)

    for feed in style_feeds:
        print('feed.pk %d, is_challenge %d, feed.response_for %s'%(feed.pk,feed.is_challenge,feed.response_for))
    from_feed = -1
    if style_feeds:
        from_feed = style_feeds[0].id
    for feed in challenge_feeds:
        print('challenge_feeds id : %d, feed.response_for %s'%(feed.pk,feed.response_for))
    for user in online_users:
        print('user.screen_name', user.username)

    response_for_feed = get_object_or_404(Feed, id=response_for)
    return render(request, 'feeds/special_feeds.html', {
        'style_feeds': style_feeds, 
        'challenge_feeds': challenge_feeds,
        'online_users' : online_users,
        'from_feed': from_feed,
        'response_for_feed' : response_for_feed,
        'page': 1,
        })


@login_required 
def challengefeeds(request):
    print('inside challengefeeds, feeds.view')
    print('gonna send challenge_feeds via feeds.views.challengefeeds')
    challenge_feeds = Feed.get_feeds().filter(is_challenge=1)
    paginator = Paginator(challenge_feeds, FEEDS_NUM_PAGES)
    challenge_feeds = paginator.page(1)

    for feed in challenge_feeds:
        print('feed.pk %d, feed.is_challenge :%s, feed.response_for :%s'%(feed.pk, feed.is_challenge, feed.response_for))
    from_feed = -1
    if challenge_feeds:
        from_feed = challenge_feeds[0].id
    most_liked_challenge_feeds = Feed.get_feeds().filter(Q(is_challenge=1)
                                              # & Q(date=datetime.date.today())
                                                ).order_by('likes').reverse()[:6]

    return render(request, 'feeds/challenge_feeds.html', {
        'challenge_feeds': challenge_feeds, 
        'from_feed': from_feed,
        'most_liked_challenge_feeds' : most_liked_challenge_feeds,
        'page': 1,
        })


@login_required 
def profilefeeds(request):
    print('inside profilefeeds, feeds.view')
    print('gonna send all_profile_feeds via feeds.views.profilefeeds')
    all_profile_feeds = Feed.objects.all().filter(profile_pk__gt=0).exclude(user__profile__is_product=1)
    paginator = Paginator(all_profile_feeds, FEEDS_NUM_PAGES)
    all_profile_feeds = paginator.page(1) # still to be made
    
    for feed in all_profile_feeds: 
        print('feed.pk %d'%(feed.pk))
    
    from_feed = -1
    if all_profile_feeds:
        from_feed = all_profile_feeds[0].id 
    print('from_feed %d' %(from_feed))

    return render(request, 'feeds/all_profile_feeds.html', {
        'all_profile_feeds' : all_profile_feeds, # profile feeds list
        'from_feed': from_feed, # for the second page on feeds_profile related
        'page': 1,
        })

@login_required 
def product_profilefeeds(request):
    print('inside product_profilefeeds, feeds.view')
    print('gonna send all_product_profile_feeds via feeds.views.product_profilefeeds')
    all_product_profile_feeds = Feed.objects.all().filter(Q(profile_pk__gt=0)
                                                & Q(user__profile__is_product=1)
                                                    )
    paginator = Paginator(all_product_profile_feeds, FEEDS_NUM_PAGES)
    all_product_profile_feeds = paginator.page(1) # still to be made
    
    for feed in all_product_profile_feeds: 
        print('feed.pk %d'%(feed.pk))
    
    from_feed = -1
    if all_product_profile_feeds:
        from_feed = all_product_profile_feeds[0].id 
    print('from_feed %d' %(from_feed))

    return render(request, 'feeds/all_product_profile_feeds.html', {
        'all_product_profile_feeds' : all_product_profile_feeds, # profile feeds list
        'from_feed': from_feed, # for the second page on feeds_profile related
        'page': 1,
        }) 


def feed(request, id):
    print('inside feed, feeds.view')
    feed = get_object_or_404(Feed, id=id)
    return render(request, 'feeds/feed.html', {'feed': feed})


@login_required
@ajax_required
def load(request):
    print('inside load, feeds.view')
    partial_feed_page = 'feeds/partial_feed.html' # setting default
    page = request.GET.get('page')
    print('page',page)
    # this is for user specific feeds

    # is_product_feed = request.GET.get('is_product_feed')
    from_feed = request.GET.get('from_feed') 
    all_feeds = Feed.get_feeds(from_feed) # to load the feeds older to feed with id from_feeds
    feed_source = request.GET.get('feed_source')   
    profile_pk = request.GET.get('profile_pk') # it will come through only on  profile_feeds, Product_profile_feeds pages
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    if page_user_name:
        page_user = get_object_or_404(User, username=page_user_name)
    # following for main feed line, that is styles copy feed
    # actually theres no need to get feed_from differently from all pages
    # just use same name from_feed for every page, it'll make the job of load function easy
    # from_feed_profile = request.GET.get('from_feed_profile')

    if feed_source == 'all_profile_feeds':
        print('feed_source is : all_profile_feeds')
        partial_feed_page = 'feeds/partial_feed_profile.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0)
                                         & Q(user__profile__is_product=0)
                                        )
    elif feed_source == 'all_product_profile_feeds':
        print('feed_source is: all_product_profile_feeds')
        partial_feed_page = 'feeds/partial_feed_profile.html'
        all_feeds = all_feeds.filter(Q(profile_pk__gt=0)
                                         & Q(user__profile__is_product=1)
                                        )
    elif feed_source == 'user_profile_feeds':  # come from profile.html page
        print('feed_source is: user_profile_feeds')
        all_feeds = all_feeds.filter(profile_pk=profile_pk)
        partial_feed_page = 'feeds/partial_feed_profile.html' # this all_feeds list has all the feeds related profile page he'/she's is on now
     
    elif feed_source == 'user_feeds': # comes from user's activity page
        print('feed_source is: user_feeds')
        all_feeds = all_feeds.filter(user__id=page_user.id) # all feeds by anyuser containing styles if any shown by user and the feeds user said anything about their friends profiles
        partial_feed_page = 'feeds/partial_feed.html'
    
    elif feed_source == 'challenge_feeds': # come from challenge_feeds page
        print('feed_source is: challenge_feeds')
        all_feeds = all_feeds.filter(is_challenge=1) # else all_feeds will be for style feedline which means it should not have any profile feedlines feed
        partial_feed_page = 'feeds/partial_challenge_feed.html'
    
    elif feed_source == 'special_feeds': 
        if response_for_feed_id:
            print('feed_source is: special_feeds with response_for_id:', response_for_feed_id)
            all_feeds = all_feeds.filter(id=response_for_feed_id)
            partial_feed_page = 'feeds/partial_feed.html'
        else:
            all_feeds = []
    for feed in all_feeds:
        print(feed.pk,feed.profile_pk,feed_source, feed.is_challenge)

    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
        
    html = ''
    csrf_token = (csrf(request)['csrf_token'])
    for feed in feeds:
        html = '{0}{1}'.format(html,
                               render_to_string(partial_feed_page,
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token,
                                                    }))

    return HttpResponse(html)


# now this method is being used only in case of posting on uers profile, that is for profile feeds
def _html_feeds(last_feed, user, csrf_token, feed_source=0):
    print('inside _html_feeds, feeds.view')
    feeds = Feed.get_feeds_after(last_feed)
    # if feed_source != 'all':
    #     feeds = feeds.filter(user__id=feed_source)
    # print(feed_source)
    print('the feed_source is :')
    print(feed_source)
    # partial_feed_page = 'feeds/partial_feed.html' 
    # its not gonna happen as I've changed the post method, which is not gonna use it
    # changing the feeds and partial feed page if user is on profile feed page
    if feed_source: 
        feeds = feeds.filter(profile_pk=feed_source)[:1]
        partial_feed_page = 'feeds/partial_feed_profile.html'
    for feed in feeds:
        print(feed.pk,feed.profile_pk, feed_source)
    html = ''
    for feed in feeds:
        html = '{0}{1}'.format(html,
                               render_to_string(partial_feed_page,
                                                {
                                                    'feed': feed,
                                                    'user': user,
                                                    'csrf_token': csrf_token
                                                    }))

    return html


@login_required
@ajax_required
def load_new(request):
    print('inside load_new, feeds.view')
    user = request.user
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    # is_product_feed = request.GET.get('is_product_feed')
    profile_pk = request.GET.get('profile_pk')
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    if page_user_name:
        page_user = get_object_or_404(User, username=page_user_name) 

    feeds = Feed.get_feeds_after(last_feed)
    
    if feed_source == 'all_profile_feeds':
        partial_feed_page = 'feeds/partial_feed_profile.html'
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            &Q(user__profile__is_product=1)
                            )

    for feed in feeds:
        print(feed.pk,feed.profile_pk,feed_source, feed.is_challenge)

    html = ''    
    csrf_token = (csrf(request)['csrf_token'])
    for feed in feeds:
       html = '{0}{1}'.format(html,
                               render_to_string(partial_feed_page,
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token,
                                                    }))

    return HttpResponse(html)
 

@login_required
@ajax_required
def check(request): 
    print('inside remove, feeds.view')
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    # is_product_feed = request.GET.get('is_product_feed')
    profile_pk = request.GET.get('profile_pk')
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    if page_user_name:
        page_user = get_object_or_404(User, username=page_user_name) 

    feeds = Feed.get_feeds_after(last_feed)
    if feed_source == 'all_profile_feeds':
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            &Q(user__profile__is_product=1)
                            )
    elif feed_source == 'all_product_profile_feeds':
        feeds = feeds.filter(Q(profile_pk__gt=0)
                                & Q(user__profile__is_product=0)
                                )
    elif feed_source == 'user_profile_feeds':
        feeds = feeds.filter(profile_pk=profile_pk)
    
    elif feed_source == 'special_feeds':
        feeds = feeds.filter(response_for=response_for_feed_id)
    
    elif feed_source == 'challenge_feeds':
        feeds = feeds.filter(is_challenge=1)
    
    elif feed_source == 'user_feeds':
        feeds = feeds.filter(user__id=page_user.id)
    
    for feed in feeds:
        print(feed.pk,feed.profile_pk, feed_source)
    count = feeds.count()
    return HttpResponse(count)

@login_required
@ajax_required 
def post(request):
    print('inside post, feeds.view')
    to_user = request.POST.get('to_user')
    profile_pk = request.POST.get('profile_pk')
    print('profile_pk :%s',profile_pk)
    last_feed = request.POST.get('last_feed')
    to_user = get_object_or_404(User, username=to_user)
    user = request.user
    csrf_token = (csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    feed.to_user = to_user
    feed.profile_pk = profile_pk
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0:
        feed.post = post[:255]
        feed.save()
    html = _html_feeds(last_feed, user, csrf_token, profile_pk)
    return HttpResponse(html)

@login_required
def new_post(request): #post with images and require page refresh
    print('inside new_post, feeds.view')
    # profile_pk = request.POST.get('profile_pk')
    # print('profile_pk :%s',profile_pk)
    user = request.user
    form = FeedForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        profile_pk = request.POST.get('profile_pk')
        is_challenge = request.POST.get('is_challenge')
        response_for_id = request.POST.get('response_for_id')
        print('is_challenge :%s'%is_challenge)
        print('response_for',response_for_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            instance.post = post[:255]
            instance.save()
            print('is_challenge : %s'%instance.is_challenge)
            print('response_for ',instance.response_for)
            if is_challenge == '1':
                return redirect('challenge_feeds')
            elif response_for_id:
                return redirect('/feeds/challenge/%s'%(response_for_id))
    return redirect('feeds')
 

@login_required(login_url='/login/')
@ajax_required
def like(request):
    print('inside like, feeds.view')
    if not request.user.is_authenticated:
        return redirect('signup_human')
    else:
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        user = request.user
        like = Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id,
                                   user=user)
        if like:
            user.profile.unotify_liked(feed)
            like.delete()

        else:
            like = Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
            like.save()
            user.profile.notify_liked(feed)

        return HttpResponse(feed.calculate_likes())


@login_required
@ajax_required
def profile_like(request):
    print('inside profile_like, feeds.view')
    profile_pk = request.POST['profile_pk']
    profile = Profile.objects.get(pk=profile_pk)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE_PROFILE, profile=profile_pk,
                                   user=user)
    if like:
        user.profile.unotify_liked_profile(profile)
        print('request user: %s had already liked this user so \
            you are gonna be removed from the liker list of this user\
            and It should appear Like text on button'
            %(request.user.username))
        like.delete()

    else:
        like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
        print('request user: %s had not liked this user so \
            you are gonna be added in liker list of this user\
            and It should appear UnLike on button'
            %(request.user.username))        
        like.save()
        user.profile.notify_liked_profile(profile)

    return HttpResponse(profile.calculate_likes())

@login_required
@ajax_required
def comment(request):
    print('inside comment, feeds.view')
    if request.method == 'POST':
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            feed.comment(user=user, post=post)
            user.profile.notify_commented(feed)
            user.profile.notify_also_commented(feed)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})

    else:
        feed_id = request.GET.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})


@login_required
@ajax_required
def update(request):
    print('inside update, feeds.view')
    first_feed = request.GET.get('first_feed')
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    # is_product_feed = request.GET.get('is_product_feed')
    profile_pk = request.GET.get('profile_pk')
    response_for_feed_id = request.GET.get('response_for_feed_id')
    page_user_name = request.GET.get('page_user_name')
    page_user = get_object_or_404(User, username=page_user_name)

    feeds = Feed.get_feeds().filter(id__range=(last_feed, first_feed))
    
    if feed_source == 'all_profile_feeds':
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            &Q(user__profile__is_product=1)
                            )
    elif feed_source == 'all_product_profile_feeds':    
        feeds = feeds.filter(Q(profile_pk__gt=0)
                            & Q(user__profile__is_product=0)
                            )
    elif feed_source == 'user_profile_feeds':
        feeds = feeds.filter(profile_pk=profile_pk)
    
    elif feed_source == 'special_feeds':
        feeds = feeds.filter(response_for=response_for_feed_id)
 
    elif feed_source == 'challenge_feeds':
        feeds = feeds.filter(is_challenge=1)
 
    elif feed_source == 'user_feeds':
        feeds = feeds.filter(user__id=page_user.id)

    dump = {}
    for feed in feeds:
        dump[feed.pk] = {'likes': feed.likes, 'comments': feed.comments,}

    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')

# Not required because this is single of its type on any page, so no need to update profile likes, cuz they
# get updated when u go to any profile 
@ajax_required   
def profile_update(request):
    print('inside profile_update, feeds.view')
    profile_pk = request.GET.get('profile_pk')
    profile = Profile.objects.get(pk=profile_pk)
    profile_likes = profile.likes
    return HttpResponse(profile_likes)



@login_required
@ajax_required
def track_comments(request):
    print('inside track_comments view')
    feed_id = request.GET.get('feed')
    feed = Feed.objects.get(pk=feed_id)
    return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})


@login_required
@ajax_required
def remove(request):
    print('inside remove, feeds.view')
    try:
        feed_id = request.POST.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        if feed.user == request.user:
            likes = feed.get_likes()
            parent = feed.parent
            for like in likes:
                like.delete()
            feed.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()

