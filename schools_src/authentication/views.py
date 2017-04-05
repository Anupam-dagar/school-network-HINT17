from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages  
from authentication.forms import SignUpForm
from feeds.models import Feed
from activities.models import Activity
 
def signup_human(request):
    print('inside signup_human, authentication.view') 
    if request.method == 'POST': 
        form = SignUpForm(request.POST) 
        flag = 'human'  
        print('flag',flag)  
        if not form.is_valid():  
            return render(request, 'authentication/signup.html',
                          {'form_human': form, 'flag': flag})
  
        else:  
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            gender = form.cleaned_data.get('gender')
            college_name = form.cleaned_data.get('college_name')
            branch = form.cleaned_data.get('branch')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)           
            profile_pk = user.profile.pk
            print(profile_pk,user.username) 
            like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
            like.save()
            user.profile.gender = gender
            user.profile.college_name = college_name
            user.profile.branch  = branch
            user.profile.is_student = 1
              
            user.save()
            login(request, user)
            # welcome_post = 'Hey {0}, Get ready to show your own flavours!!.'.format(user.username,
            #                                                     user.username)
            # feed = Feed(user=user, post=welcome_post)
            # feed.save()
            messages.add_message(request, 
                                 messages.SUCCESS,
                                 'Get ready to show your own flavours!!'+user.username+
                                 '\n If you want to make people make a special pose for you, \
                                 just share that and see if your friends could make that better?\
                                  you Can visit your friends profile and say something\
                                  about him/her!'
                                 )

            print('inside signup, authentication.views')
            print('user\'s pk %d'%(user.pk))
            return redirect('feeds')
 
    else: 
        return render(request, 'authentication/signup.html',
                      {'form_human': SignUpForm()})

def signup_products(request):
    print('inside signup_products, authentication.view') 
    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        flag = 'products'
        print('flag','products')
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form_products': form, 'flag':flag})
  
        else: 
            college_name = form.cleaned_data.get('college_name')
            is_product = request.POST.get('is_product')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)           
            
            profile_pk = user.profile.pk
            print(profile_pk,user.username) 
            like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
            like.save()
            if is_product:
              print('user is a college')
              user.profile.is_product = 1

            user.profile.college_name = college_name
            user.save()
            login(request, user)
            # welcome_post = 'Hey {0}, Get ready to show your own flavours!!.'.format(user.username,
            #                                                     user.username)
            # feed = Feed(user=user, post=welcome_post)
            # feed.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Hey ,'+user.username+
                                 '\n Its all about products, \
                                 See what people are talking with your friend products\
                                  You are live now you can talk to the people who use you\
                                  and people can talk you on your live profile!'
                                 )

            print('inside signup, authentication.views')
            print('user\'s pk %d'%(user.pk))
            return redirect('feeds') 

    else: 
        return render(request, 'authentication/signup.html',
                      {'form_products': SignUpForm()})


def signup_teachers(request):
    print('inside signup_teachers, authentication.view') 
    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        flag = 'teachers'
        print('flag','teachers')
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form_teachers': form, 'flag':flag})
  
        else: 
            college_name = form.cleaned_data.get('college_name')
            is_product = request.POST.get('is_product')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)           
            
            profile_pk = user.profile.pk
            print(profile_pk,user.username) 
            like = Activity(activity_type=Activity.LIKE_PROFILE, profile=profile_pk, user=user)
            like.save()
            
            user.profile.is_teacher = 1

            user.profile.college_name = college_name
            user.save()
            login(request, user)
            # welcome_post = 'Hey {0}, Get ready to show your own flavours!!.'.format(user.username,
            #                                                     user.username)
            # feed = Feed(user=user, post=welcome_post)
            # feed.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Hey ,'+user.username+
                                 '\n Its all about products, \
                                 See what people are talking with your friend products\
                                  You are live now you can talk to the people who use you\
                                  and people can talk you on your live profile!'
                                 )

            print('inside signup, authentication.views')
            print('user\'s pk %d'%(user.pk))
            return redirect('feeds') 

    else: 
        return render(request, 'authentication/signup.html',
                      {'form_products': SignUpForm()})
