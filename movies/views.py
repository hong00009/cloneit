from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Participant, Role, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
    movies = Movie.objects.all()

    for movie in movies:
        poster_url = get_image(movie.title)
        movie.image = poster_url
        
        comments = Comment.objects.filter(movie=movie)

        movie.average_rating = average_stars(comments)


    context = {
        'movies': movies,
        'poster_url': poster_url,
    }

    return render(request, 'movies/index.html', context)

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    # Movie모델에서 object 찾는데, 없으면 404페이지
    # 들어온 id와 일치하는 것 찾아서 movie에 저장

    movie_roles = Role.objects.filter(movie=movie)
    # 제목 - 참가자이름 - 역할 로 Role에 저장된것을 가져옴

    genres = movie.genres.all()
    countries = movie.countries.all()
    comments = Comment.objects.filter(movie=movie)

    average_rating = average_stars(comments)

    poster_url = get_image(movie.title)

    # 이미 평가한 유저는 폼 안보여줌
    already_done = Comment.objects.filter(user=request.user, movie=movie).exists()

    if already_done:
        comment_form = None
    else:
        comment_form = CommentForm()

    context = {
        'movie': movie,
        'movie_roles': movie_roles,
        'genres': genres,
        'countries': countries,
        'comments': comments,
        'comment_form': comment_form,
        'poster_url': poster_url,
        'average_rating': average_rating,
        'already_done': already_done,
    }
    return render(request, 'movies/movie_detail.html', context)

def participant_detail(request, id):
    participant = get_object_or_404(Participant, id=id)

    roles = participant.role_set.all()
    # models.py 에서 movie클래스안에 participants related_name='roles'로 설정함

    context = {
        'participant': participant,
        'roles': roles,
    }

    return render(request, 'movies/participant_detail.html', context)

def comments_create(request, id):
    movie = get_object_or_404(Movie, id=id)


    if request.method == 'POST':
        form = CommentForm(request.POST)
        user = request.user
        

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            print('댓글저장됨')
            
            return redirect('movies:movie_detail', id=id)
    else:
        form = CommentForm()
    
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'movies/movie_detail.html', context)



@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('movies:movie_detail', id=comment.movie.id)
    


def get_image(query):
    URL = f"https://www.bing.com/images/search?q=위키+{query}+영화포스터&first=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    urls_result = soup.find_all("img",class_="mimg", limit=5)


    image_urls = []
    for image in urls_result:
        if "src" in image.attrs:
            image_urls.append(image["src"])

    if urls_result:
        first_image_url = urls_result[0]["src"]
        # print('검색결과 첫번째이미지:',first_image_url)
        return first_image_url


def average_stars(comments):
    rating_sum = 0
    count = 0

    for comment in comments:
        rating_sum += comment.rating
        count += 1
    # 전체 코멘트 불러들여서, 처음부터 끝까지 별점 다 더해서 rating_sum에 저장
    # 카운트는 전체 코멘트 숫자

    if count == 0:
        average_star = 0
        # 코멘트가 아무것도 없으면 평점도 0
    else:
        average_star = round(rating_sum / count, 2)
        # 전체점수 / 코멘트수 => 소수점2자리까지반올림
    return average_star
