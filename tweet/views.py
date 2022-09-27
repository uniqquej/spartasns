from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required

def home(request):
    user = request.user.is_authenticated #사용자가 로그인 되어 있는지 확인
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated

        # 로그인한 사용자만 접근 가능
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at') # 시간 역순으로 저장 -
            return render(request,'tweet/home.html',{'tweet':all_tweet}) #dict 형태로 데이터 넘겨줌
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user #로그인 되어 있는 사용자의 전체 정보를 가져옴
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.content = request.POST.get('my-content','')
        my_tweet.save()
        return redirect('/tweet')

@login_required
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id = id)
    my_tweet.delete()
    return redirect('/tweet')
