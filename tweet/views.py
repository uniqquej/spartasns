from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel,TweetComment
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
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag','').split(',') #외부에서 태그를 받아오는 작업
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # 시간 역순으로 저장 -
            context = {'error':'글은 공백일 수 없습니다.',
                       'tweet':all_tweet}
            return render(request,'tweet/home.html',context)
        else:

            my_tweet = TweetModel.objects.create(author=user, content =content)
            for tag in tags: #받아온 태그 분리 작업
                tag = tag.strip() #공백 제거
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')

@login_required
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id = id)
    my_tweet.delete()
    return redirect('/tweet')
@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request,'tweet/tweet_detail.html',{'tweet':my_tweet,'comment':tweet_comment})


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment","")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))

#장고 taggit 사이트에서 제공하는 공식 템플릿
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context