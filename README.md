# 1차 작업
accounts 앱 : 사이트 로그인 기능은 예전에 수업에서 다룬것을 그대로 가져옴
movies 앱 : models.py를 만드는데 시간이 많이 소요됨

Movie 클래스를 만들었고 그안에 영화정보를 다 때려넣음
연령제한은 단순히 숫자인줄 알고 처음에 int필드로 만들었는데, 더 자세히 검색해보니까 제한상영이라고 숫자랑 관계없는 값도 있고 총 5가지뿐이어서 이중에 하나 고를 수 있도록 CHOICE로 설정함

영화배우정보가 너무 많아서 별도의 클래스로 분리함.
그런데 배우뿐만 아니라 같은 사람인 감독도 함께 분리해놓는게 맞다고 생각해서 actor/director 합쳐서 Participant 참가자라고 뭉뚱그려서 새로운 클래스를 만들었음.

Participant 클래스로 분리했는데, 여기에는 사람 개인의 신상 정보만 나타내고 싶고, 일단 name만 적었음. [참가자 - 영화] 사이를 이어주는 다른 곳에 참가자가 맡은 역할을 저장하는게 맞다고 생각했음. 근데 참가자/participant라는 영단어가 너무 길다. people/person은 너무 포괄적인거같아서 그냥 이걸로 계속 쓰기로 함.

Role 클래스를 만들었고 
감독/주연배우/조연배우 사람의 역할을 3가지 중에 하나를 선택하도록 한정적으로 정해줬음.
참가자 정보는 Participant 클래스와 FK로 연결, 무슨영화를 찍었는지 Movie클래스와 FK로 연결했음.
그래서 샘플로 입력한 첫번째 값은 movie_id(1번, 기생충) participant_id(1번, 봉준호) role_type(director,감독) 이렇게 저장됨

index.html에서 모든 영화제목이 보임. 영화제목을 누르면 a href를 통해 영화 상세정보가 보이도록 설정함. movie_detail.html로 연결되고,movies/숫자/ url로 연결. 영화 상세정보가 보임

관람객수가 출력되는데 12345678로 출력되길래 숫자구별 쉼표를 찍게 하고싶어 찾아보니 |intcomma를 쓰면 되고 앞쪽에 {% load humanize %} 를 적고 settings.py의 앱목록에 'django.contrib.humanize', 를 적음.

admin페이지에 테스트용 값을 넣으려니까 admin.py에다 내가 만든 모델 하나하나를 다 넣어야했는데 이게맞나 싶었음. admin.site.register(Movie) (->이 부분은 3차작업 중 importexport 사용하면서 register([Movie, Country, ... ]) 이런식으로도 사용할 수 있다는 것을 찾아냄)

admin 게시판에서 등록한 데이터 제목이 object(1) (2) 이런식으로 나타나길래, 내가 입력한 값으로 나오게 하는 방법을 찾아보니 클래스안쪽에 def __str__을 쓰면된다고 해서 썼음.

+ 장르,국가를 charfield 말고 M:N으로 만드는게 낫다는 조언을 받음. 장르가 로맨틱/호러 중복될 수 있고, 국가도 한일합작 처럼 중복될 수 있기 때문.
+ 지금은 평점을 고정값으로 넣었는데, 추후 사용자가 댓글로 남기는 평점들을 모두 읽어내고 평균값으로 반영하는 걸로 바꾸는 방향에 대한 조언을 받음
+ 가끔 감독이면서 배우인경우도 있는데 어떻게 할것인지, 별도로 저장해놓을 것인지 고민을해야한다고 조언받음. participants = models.ManyToManyField('Participant', through='Role') 로 해놓긴했는데 내가 그럴려고 넣은게 아니라 연결하려면 넣어야한다고 어디서 보여서 적었던 through인데 얻어걸린거같기도 하고 잘 모르겠음.
+ 영화정보는 admin페이지에서 샘플로 1개만(기생충) 수기로 하나하나 입력했는데, 영화정보는 사용자가 입력하는 값이 아니기도 하고, 모든 정보를 admin에서 굳이 다 넣지말고.. 다른방법을 찾아보라는 조언받음.
나중에 뼈대가 만들어지면 영화정보 api를 이용하고싶음.



# 2차 작업
장르와 국가를 M:N으로 설정하기 위해, Genre 클래스와 Country 클래스를 새로 만들었음.

genres = models.ManyToManyField('Genre', related_name='movies')
'Genre' 라고 따옴표로 감싸면, Genre 클래스가 맨 위에 있지않아도 알아서 찾아서 읽음
movies라고 참조이름을 설정해두는게 가독성이 좋은방향
### 사용예시 - 액션 장르인 영화 
action_genre = Genre.objects.get(name='액션')
action_movies = action_genre.movies.all()

### related_name이 없는경우 사용예시 _set.all()
action_genre = Genre.objects.get(name='액션')
action_movies = action_genre.movie_set.all()

### 사용예시 - 제작국가 한국인 영화
korea = Country.objects.get(name='한국')
korean_movies = Movie.objects.filter(country=korea)

출력해보니 [드라마 애니메이션] 이라고 개별로 나오길래 안에 쉼표로 연결하는 것을 찾아서 {% if not forloop.last %}, {% endif %} 라고 적었음. 마지막루프가 아니면 쉼표넣으라는 뜻이라고 함. [드라마, 애니메이션]으로 내가 원하는 방향에 맞게 출력되었음.

movie_detail.html안에서 사람이름을 누르면 a href를 통해 영화 상세정보가 보이도록 설정함.

participant_detail.html을 새로 만들었음. (계속봐도 participant라는 단어는 어색한듯함.)
participant_detail.html안에서도 영화 제목을 누르면 movie_detail.html로 연결되도록 설정함

참가자 출력시 내가 데이터를 입력한 순서대로, id 순서대로 출력되길래, 감독/주연/조연 순으로 나타나도록 html안에 if문을 아주많이 때려넣었다. 더 간단하게 하고싶었는데, 찾아보니까 distorder인가 그걸 쓰라고 하는데 그게 더 복잡해서 그냥 그대로 if 문만 때려넣으니 코드가 좀 지저분해보임.

views와 각종 html을 수정하는데 계속 변수이름이 role role이 나오니까 게슈탈트붕괴현상이 와서 롤이 뭐지?하고 너무 헷갈렸음. 그래서 role을 movie_role로 고쳐보았음. 예를들어 movie_detail.html에서 
```html
{% for role in movie_roles %}
        {% if role.role_type == 'director' %}
```
이라는 곳이 있는데, role이 엄청 많이 나와서 롤롤롤로 하니까 천천히 꼼꼼히 읽어봐야 이게 무슨뜻인이 이해가 되었음.
내가 Role 클래스를 중개모델로 만들어놓은것이 실수인걸까 다른클래스를 만들어야하나 아니면 Role 클래스를 뜯어고쳐야할까 많이 고민했는데 그냥 써야겠음. 처음부터 설계를 제대로 하고 시작한게 아니라, 먼저 만들어놓고 이상한걸 고치는 식으로 의식의 흐름대로 코드를 작성하다보니 뭔가 두서없는 것 같음.

감독이면서 배우인 경우 어떻게 나타나는지 테스트 해보기 위해 봉준호라는 participant 값을 하나 새로 추가했고 조연으로 설정했는데, 봉준호를 눌러보니까 추가한것처럼 감독/조연 둘다 나왔음. role 테이블을 보니까 [1,1,director]랑 [1,1,supporting] 으로 각각 입력되어있음.

그렇다면 동명이인의 각자 다른 배우를 입력해놓는경우 겹쳐서 출력될 것 같다는 생각이 들었음. Participant 쪽에 현재 name만 받고있는데, 동명이인 구별을 위해 이곳에 사람 정보를 상세하게 더 넣어야하는건가.

더 만들고 싶은 기능
개봉연도, 연령제한, 장르,국가, 제작사도 개별값을 누르면 그 값과 일치하는 모든 영화가 출력
별점도 1점대, 2점대, 3점대... 이렇게 정수값별로 모아보기
관람객수도 1000만관객이상만 모아보기
참조/역참조 다 설정하기 - 복잡할것같아 우선 보류

장르/국가를 별도의 클래스로 분리하고나니, 새로운 영화정보를 저장할때 이미 목록에 있는 장르/국가중에서 선택하도록 되어있고 그외 새로운장르를 누르려면 + 버튼을 통해 팝업으로 추가할 수 있음
participants 도 동일한 ManyToMany 필드인데 선택지가 없는이유는 through='Role' 을 작성해서 Role만 별도로 분리해뒀기 때문에 Role쪽에서 배우정보를 연결해서 입력해줘야하는 것 같음

로그인기능만 가져오고 댓글쓰기 등 기타 기능은 아직 안가져왔음. admin페이지에서 샘플로 미리 입력해둔, 해당 영화에 작성된 코멘트 보기는 가능하게 설정해놨음.

/accounts/<username>/으로 프로필을 볼 수 있는 profile.html을 만들었음.

해야하는일 
코멘트폼 넣기, 별점 남기기, 모든 댓글에 영화별점을 입력받고, 영화마다 평균점수 노출하기, 사용자가 댓글남긴 영화목록과 댓글 전부 보여주고 총 개수 나타내기

현재 코멘트 모델과 코멘트노출 기능은 movie안에 들어있는데 성향이 안어울리는 것 같아 보임. movie에 있는 것을 분리하여 별도의 comments 앱으로 분리하는게 나을지, 분리하면 오히려 더 복잡하고 관리/가독성이 안좋은지? (분리하다가 잘 안돼서 포기함)

# 3차 작업
+ comment기능이 현재 movie 안에 종속되어있는데, 이걸 분리해서 개발할지 지금처럼 개발해나갈지 질문하였고, 선택은 개발자의 취향 차이이지만 comment기능은 영화 게시물 안에 포함된 하위개념이니까 분리하는것보다 movie안에서 개발하는편이 더 낫다는 의견을 듣고 movie안에서 계속 개발하는걸로 둠.

+ 만약 동명이인 배우가 있다면, 그 이름을 클릭했을때 둘다 정보가 노출되는거 아닌지 질문하니, 한 사람당 고유한 키값이 주민등록번호처럼 할당되어있기 때문에 각각 다른 사람으로 취급되니 문제 없다는 답변을 받음
알고보니 내가 테스트로 입력했던 봉준호-감독과 봉준호-조연은 같은사람이 다른역할로 참여한거였고 동명이인과는 관계가 없었음

+ 영화 데이터를 하나하나 입력하기 힘드니 api 활용 등으로 대량으로 데이터를 넣고싶어 찾아봐야한다고 질문하니 정말 다양한 방법이 있지만 django import export 사이트를 권유해주심. 우선 내 db를export해보면 cvs등 양식에 맞춰 파일 하나가 생성될테니까, 그 파일양식에 새로운 데이터를 입력해서 다시 import하는 방법이 당장은 간단할 것이라는 답변을 받아 우선이것부터 시도해보기로함

django import export를 사용해봄. 초기 셋팅과정은 공식홈페이지 가이드라인에 따라 실행하였음. pip install django-import-export 

기능 구현은 admin.py에다가 구현해서 새로웠음. 처음에는 import와 export 두가지의 기능이 admin페이지에 버튼으로 생겼는데, 다른 부가기능을 사용하기 위해서 ExportMixin, ImportMixin 으로 import된 것을 바꾸다보니 버튼 2개중 1개밖에 나오지 않았음. 찾다찾다 왜 안나오는지 이유를 몰라서 그냥 import필요할때 고치고, export필요할때 고쳐놓는 식으로 사용하기로 포기함. 

export해보니까 내가 예상한 것과 다르게 장르,국가,배우이름이 전부 숫자인 id값으로 추출되어 당황했음. 또 열심히 구글링해서 키값이 아니라 필드 네임으로 추출되게 변경했음. 그랬더니 import할때 역시 id 키값을 넣어야 입력이 되길래 키값이 아닌 실제 사람이름을 넣어도 저장될 수 있도록 고쳤음. 그중에 단점이 import시 배우이름이 내 db에 있어야만 자동등록이 되어서 새로운 영화정보를 아무리 import해도 배우가 저장이 안되고 있었음. 만약에 기존 db에 없는 완전히 새로운 데이터가 입력된다면 model에 자동으로 입력되는 기능을 몇시간동안 찾아봤지만 import-export 자체로는 기능을지원하지 않으니 다른툴을 쓰라는 내용이 있어 그냥 포기함. 이상황에서 다른 툴을 배우고 싶지는 않아서 그냥 나무위키에서 배우정보를 모조리 내가 엑셀파일로 만들어서 대량으로 import해서 입력해놨음. 국내외 감독과 배우를 5000명정도 입력함. 사람에 비해 국가/장르는 몇개 되지 않아서 간단히 엑셀로 만들어서 import함.
이과정에서 굉장히 시간이 많이 소요되었음

이전 수업시간에 배운 코멘트입력 폼을 그대로 가져와서 내 프로젝트에 이식했음. 댓글 입력시 해당 영화 id와 연결되어 저장되도록 설정했고 잘 작동함. 댓글 삭제도 이전 수업시간에 배웠던 delete 기능 가져와서 적절히 수정해서 이식했음. 기존에 있던걸 가져와서 사용하니 시간이 별로 걸리지 않았음


# 4차 작업
+ 이전에 조언받은 import export를 활용하여 영화정보 대량 import가 가능하게 구현한 것과, 댓글작성/삭제 기능 버튼을 구현한것을 말했고, 앞으로 별점평가 및 남겨진 별점의 평균점수를 나타내는 것을 보여주는 기능과, 사용자 정보를 들어가면 그 사용자가 어떤 평가를 남겼는지 모아보는 기능을 만들어보고 싶다고 말함. 
+ 큰 틀의 필요한 작업들은 만들어진것같고, 별점기능은 자바스크립트 및 모델로 점수를 보내기 등 다소 복잡한 과정으로 만들어지므로 시간이 오래 소요되니까 우선순위를 나중으로 미루거나 포기하고 사용자로부터 1~10 숫자를 입력받는 것으로 구현하는 것이 좋을 것이라는 답변과, 앞으로 세부적으로 영화 포스터를 보여준다는지 등의 기능과 보기 좋게 꾸미는 것이 있었으면 좋겠다고 조언받음. 
+ 초반에 모델 구축?하는 작업은 2일정도 걸려서 하나하나 타이핑하고 고쳐보고 연결해보고 했던 반면, 후반부로 갈수록 기존에 이미 만들어진 코드를 찾아와 복붙해서 약간 수정하는 형식인데 이렇게 개발하는 방향이 맞는지, 이래도 실력이 느는게 맞는지 걱정된다는 질문을하니 그렇게 하는게 맞다고 0부터 시작해서 일일이 다 만드는사람이 거의 없다고 걱정하지 말라는 답변을 받음

예전에 배운 beautifulsoup으로 영화포스터를 긁어와서 보여주려고 했음. 검색해보니까 대부분 selenium으로 하는데, 지금 이상황에서 새로운걸 배워서 쓰고싶지않아서 BS4관련게시물만 엄청 찾아봤음. 보니까 네이버/다음/구글 등 유명 검색사이트에서는 전부 BS4로 단순히 긁어오는 것이 막혀있어서, 다른 대안을 찾다가 검색 사이트를 바꿔 네이트,줌 다 시도했으나 똑같이 실패. 마지막으로 bing에서는 BS4만으로도 정상작동하길래 포스터를 띄워봤음. 검색결과 중에 가장 첫번째로 나오는 사진을 띄우기로 결정함. 그런데 검색결과가 엉뚱한게 나오는 경우도 있어서, 예를들어 기생충 영화 포스터 검색했는데 진짜 말그대로 '기생충'관련 유튜브 썸네일이 나와서 검색어를 이리 저리 조정해보다가 키워드를 "위키+영화제목+영화포스터" 로 정했음. 의도한 방향은 나무위키 사이트에 등록된 영화포스터가 공식포스터이니 이것을 검색결과에 나오도록 하고싶었는데, 이것조차도 관련없는 엉뚱한 영화포스터가 나오기도 하고 이상했음, bing은 검색엔진으로 적합하지 않은 것을 다시 한번 느낌.

사용자정보를 누르면 그간 작성했던 댓글이 모두 나오게 했음. set all 보다는 comments.all로 표기되는게 가독성이 좋아서 Comment 모델클래스 안의 user 변수에다가 related_name = comments으로 연결되게 했음. 

오래된작성일자>최신순으로 노출되길래 html에서는 역순으로 출력하려니까 안돼서 views파일에서 아예 역순으로 저장되게 한다음에 html에서 출력되게 했더니 1일전, 3일전, 5일전 순으로 잘 출력되었음. .order_by('-created_at') -기호가 역순. 영화정보페이지에서는 오래된순으로 나오는게 맞지만 사용자정보에서는 역순으로 나오는게 맞는 것 같음. empty 를 쓰면 아무것도 없는경우를 분기처리 할 수 있었음.

코멘트 목록에서도 사용자 이름을 클릭해서 사용자 정보를 볼 수 있게 연결하였고, 사용자정보에서도 코멘트를 작성한 영화정보 페이지로 연결하였음.

이것저것 다시 작동해보니까 로그아웃상태에서도 댓글작성폼이 보이길래 로그인상태에서만 댓글을 작성할 수 있게 만들어두었음.

로그아웃했다가다시 새로운 회원가입을 하려고 보니 이상하게 회원가입할때도 '로그인'버튼으로 나옴. 이전에 로그인할때 로그인버튼을 '로그인'으로 표기되도록 고쳐놓았던 것이 생각남. 확인해보니 부트스트랩으로 만든 폼은 둘다 같은표기가 나올수밖에 없다해서 로그인을 포기하고 '제출'로 다시 복구해놓음 .

별점을 정말 별모양을 클릭해서 구동하는 것은 너무나도 복잡하고 어렵고 시간이 촉박하니 포기하고.. 조언받은대로 그냥 버튼으로 점수를 선택할 수 있게 만들어봄. 
comment 폼쪽에 rating 항목을 integer필드로 0~5까지 선택하도록 만들었음. 10까지 하니까 선택지가 너무 길어서 그냥 5까지만 했음.
comment 모델에 rating 항목도 입력받게 수정함. makemigrations 과정에서 기존에 작성된 리뷰들은 rating이 없는데 어쩔거냐고해서 default 5로 설정해서 이전에 작성된 리뷰들은 일괄 5점으로 처리하고 migrate함. 모델쪽은 integer, 뷰쪽은 

버튼을 만들고보니 글자입력칸, 점수선택칸, 제출버튼이 세로로 나열되어 보기 좋지 않았음. 찾아보니 이 세가지 기능을 하나의 div 안에 넣어야 한덩어리 취급 받는 것이었음. 부트스트랩의 flex부분을 참고함. 그런데 제출버튼 하나만 다른것에비해 조금 아래로 내려가있는 것 같은데, 부트스트랩 양식의 버튼이라 그런건지 이건 제대로 고쳐지지 않아서 포기함.

영화 하나당 입력된 댓글들의 갯수와 평균평점을 나타내기로함. 찾아보니 Avg 를 import하고 이것저것 임포트하고 하라는데 import가 너무 많아지는것도 싫고 새로운 함수를 익히기엔 시간이 없어서 그냥 평균내는 함수 average star() 를 만들어서 필요할때 호출해서 사용하게 해놨음.

사용자정보 페이지에서도 본인이 작성했던 댓글을 삭제하는 기능을 만들어야겠다고 생각했음. 로그인한 유저와 댓글작성한 유저가 동일하면 삭제버튼이 보이도록 설정함.
현재 comment 삭제 기능이 있어서 profile쪽에도 끌어와서 썼는데 문제점이 있었음. 기존 삭제기능은 movie_detail 페이지에서 조회했을때 기준으로 만들어진거다보니 삭제하면 영화상세 페이지로 자동 이동함. 그러다보니 내가 내 프로필에서 삭제했는데도 프로필페이지가 아닌 영화상세페이지로 이동하여 불편했음. 이럴경우 comment삭제 함수를 수정해야하는데, 삭제함수를 실행한 곳의 페이지 정보를 comment 삭제 함수에서 받아와서 여기가 영화상세페이지인지, 아니면 유저프로필페이지인지를 받고 페이지마다 if/else로 redirect나 render를 고치면 된다는데 잘 안됐음. 이거하다가 밤 12시가 되어서 포기하고 그냥 잠 


# 5차 작업
평균점수가 제대로 작동하는지 살펴보다가, 1점으로 별점테러하는걸 방지하기 위해 1명당 1개의댓글을 작성하는게 맞다고 생각함. 찾아보니 unique로 설정하면 된다고함. 모델쪽에 메타에 constraints 변수를 만들고 models.UniqueConstraint 설정. 모델이 수정되었으니 다시 migrate해야하는데, makemigrations까지는 문제가 없는데 migrate에서 문제가 발생함. UNIQUE 설정이 실패했나본데 기존에 내가 테스트로 작성해놓은 댓글들이 이미 중복된게 많이 있어서 그랬음. 중복댓글 다 지워주니 migrate성공함.  

모델쪽은 수정했는데 뷰랑 템플릿쪽도 수정해야 제대로 적용이 되는 구조였음. 처음에는 코멘트 기능이니까 comments_create함수쪽에 만들어야지 했는데 문제점이 있었음. 이미 영화평가를 작성한 사람이 새로운 평가+점수를 선택하고 [작성]버튼을 누르면 "이미 평가한 영화입니다." 라고 표기되게 했는데, 이러면 열심히 쓴 글이 날아가버리게 되니까 아예 이미 댓글을 작성했던 사람한테는 입력창자체를 노출하지 않는 것이 맞는 방향이라고 생각했음. 그래서 찾아보니 exist() 함수로 작성된정보에서 user와 movie가 같은게 이미 존재하는 경우를 걸러낼 수 있었음. 만들어놓고 작동시켰으나 여전히 댓글 작성한 이후에서야 동작했음. 곰곰히 생각해보니 이 함수는 사용자가 폼을 입력하고 난 이후 상황을 처리하는 것이라, 영화정포 페이지 보자마자 "이미 평가를 남겼다" 라는 메세지를 보이게 하려면 comments_create 쪽이 아니라 movie_detail 쪽에서 중복작성 여부를 노출하는게 맞았음

영화데이터를 한 20개정도는 더 넣어야 보기 좋을 것 같음. 그런데 영화 포스터를 beautifulsoup으로 읽어오는게 좀 오래걸림. 원래 2개였는데 3개추가해서 5개가 되니 훨씬 로딩이 오래걸림, 영화정보가 많으면 더 오래 걸릴 것 같아서 걱정됨. 그냥 추가하지 않고 써야겠음

전에 썼던 코드를 가져와서 부트스트랩 카드 형태로 담아 영화포스터, 영화제목, 평점, 평가사람숫자 네가지 정보가 보이도록하여 index페이지의 레이아웃을 수정했음

최신영화순으로 정렬해야할듯.

+ 사진은 어떻게 가져온거냐고 해서 get_image함수쪽의 코드 보여드림. 왜 실시간 검색으로 포스터 이미지를 불러왔는지 의아해하심. 나는 시간이 촉박하여 이렇게 만들었다고 답변. 실시간 검색 결과에서 나온 첫번째 사진의 url만 따와서 그걸 그대로 사용자에게 전달함. 그러면 리소스를 너무 많이 잡아먹으니 이미지를 저장해놓고 저장한 이미지를 띄우는 식으로 하는게 맞고, 나중에는 그렇게 만들라고 답변받음. 우선 지금 당장은 사진이 잘 나오니 유지.
+ 평점을 어떻게 계산해서 띄웠는지, 만약 댓글이 없으면 평점이 몇점으로 보이는지 확인해달라 하여 average_stars 함수쪽의 코드 보여드림.
+ 전체적인 구성은 거의다 된 것 같아서 이제 페이지를 예쁘게 꾸며 마무리 지으면 되겠다고 답변받음

만들어둔 함수가 너무 많다보니 설명할 때 어떤코드로 작동했는지 잘 기억이 나지 않는 단점이 있었음

# 6차 작업
부트스트랩에 기존에 있는 탬플릿 가져와서 적용하기
