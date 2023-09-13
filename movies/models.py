from django.db import models
from django.conf import settings

# Create your models here.


class Movie(models.Model):
    # 영화 정보
    AGE_LIMIT_CHOICES = (
        ('all', '전체관람가'),
        ('12', '12세 이상 관람가'),
        ('15', '15세 이상 관람가'),
        ('rated-R', '청소년 관람불가'),
        ('restricted', '제한상영가'),
    )
    title = models.CharField(max_length=100)    
    duration = models.PositiveIntegerField(default=0)
    age_limit = models.CharField(max_length=10, choices=AGE_LIMIT_CHOICES)
    audience_count = models.PositiveIntegerField(default=0)
    production_company = models.CharField(max_length=100)
    release_year = models.PositiveIntegerField()

    # 2차 수정목록 장르,국가,평점
    participants = models.ManyToManyField('Participant', through='Role')
    # 장르 M:N 으로 수정필요
    # 원래는 char필드였음 genre = models.CharField(max_length=100)
    genres = models.ManyToManyField('Genre', related_name='movies')

    # 제작국가도 M:N으로 수정필요, 나라별 합작/공동제작의 경우를 위해
    countries = models.ManyToManyField('Country')


    # rating은 댓글남기면서 평점을 매기면, 모든 댓글의 평균점수를 나타내는 방향으로 수정필요
    rating = models.FloatField()

    def __str__(self):
        return self.title

class Participant(models.Model):
    # 사람 신상정보
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    ROLE_CHOICES = (
        ('director', '감독'),
        ('leading', '주연'),
        ('supporting', '조연'),
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.movie.title} - {self.participant.name} - {self.get_role_type_display()}"
    
    
class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=5)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie', 'rating'],
                name='one_by_one',
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.content}"

