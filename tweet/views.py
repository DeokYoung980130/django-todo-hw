# tweet/views.py
from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

@login_required()
def tweet(request):
    if request.method == 'GET':
        all_tweet = TweetModel.objects.all().order_by('-created_at')
        return render(request, 'tweet/home.html', {'tweet': all_tweet})
    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다.', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            my_tweet.save()
            return redirect('/tweet')


def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')
    