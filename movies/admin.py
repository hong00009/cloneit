from django.contrib import admin
from .models import Movie, Participant, Role, Genre, Country, Comment

from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget
from import_export import fields, resources
from import_export.admin import ExportMixin, ImportMixin
import re

# Register your models here.
    
class MovieResource(ModelResource):
    title = fields.Field(attribute='title')
    genres = fields.Field(
        attribute='genres', 
        widget=ManyToManyWidget(Genre, field='name')
    )
    countries = fields.Field(
        attribute='countries', 
        widget=ManyToManyWidget(Country, field='name')
    )
    participants = fields.Field(
        attribute='participants', 
        widget=ManyToManyWidget(Participant, field='name')
    )

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'duration',
            'age_limit', 'audience_count',
            'production_company', 'release_year', 
            'participants__name',
            'genres__name', 
            'countries', 'rating'
        )

        import_id_fields = ('participants__name', 'genres__name')

    
    def get_export_order(self):
        return ['id', 'title', 'duration', 
                'age_limit', 'audience_count', 
                'production_company', 'release_year', 
                'participants', 'genres', 
                'countries', 'rating']
    
class RoleResource(resources.ModelResource):
    class Meta:
        model = Role

# @admin.register(Movie)
class MovieAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    resource_class = MovieResource

    resource_class.related_resources = {
        'participants': RoleResource,
    }

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('id')
    
    def before_import_row(self, row, **kwargs):
         # import 전 row 처리
        participant_names = row.get('participants')

        if participant_names:
            if isinstance(participant_names, str):
                participant_names = participant_names.split(",")

                participants = []
                for participant_info in participant_names.split(","):
                    match = re.search(r'(.+)/(.+)', participant_info)
                    if match:
                        participant_name = match.group(1).strip()
                        role_type_input = match.group(2).strip()

                        # 매핑된 role_type 찾기
                        role_type_map = dict(Role.ROLE_CHOICES)
                        role_type = role_type_map.get(role_type_input)

                        if role_type:
                            participant, _ = Participant.objects.get_or_create(name=participant_name)
                            role, _ = Role.objects.get_or_create(movie=row.instance, participant=participant, role_type=role_type)
                            participants.append(participant)

                row['participants'] = participants
                # for name in participant_names:
                #     participant, _ = Participant.objects.get_or_create(name=name.strip())
                #     participants.append(participant)

                # row['participants'] = participants

        return super().before_import_row(row, **kwargs)
    
    def before_import_row(self, row, **kwargs):
        participant_names = row.get('participants')

        if participant_names:
            if isinstance(participant_names, str):
                participants = []
                for participant_info in participant_names.split(","):
                    match = re.search(r'(.+)\((.+)\)', participant_info)
                    if match:
                        participant_name = match.group(1).strip()
                        role_type = match.group(2).strip()
                        participant, _ = Participant.objects.get_or_create(name=participant_name)
                        role, _ = Role.objects.get_or_create(movie=row.instance, participant=participant, role_type=role_type)
                        participants.append(participant)

                row['participants'] = participants

        return super().before_import_row(row, **kwargs)
 
# Participant, Genre, Country 모델에 대한 리소스 클래스 정의
class PaResource(ModelResource):
    class Meta:
        model = Participant
        # import_id_fields = ('participants__name',)  
        # Import할 때 genres 필드에 name 값을 사용

class GeResource(ModelResource):
    class Meta:
        model = Genre
        # import_id_fields = ('genres__name',)  
        # Import할 때 genres 필드에 name 값을 사용
        
class CoResource(ModelResource):
    class Meta:
        model = Country
        # import_id_fields = ('country__name',)  
        # Import할 때 genres 필드에 name 값을 사용


# Participant, Genre, Country 모델에 대한 Admin 클래스
class PaAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = PaResource
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('id')

class GeAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = GeResource
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('id')

class CoAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = CoResource
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('id')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Participant, PaAdmin)
admin.site.register(Genre, GeAdmin)
admin.site.register(Country, CoAdmin)

admin.site.register([Role, Comment])
# admin.site.register(Role)
# admin.site.register(Genre)
# admin.site.register(Country)
# admin.site.register(Comment)


    # # 중복 데이터 처리
    # def import_row(self, row, instance_loader, **kwargs):
    #     instance, new = instance_loader.get_instance(row)

    #     if not new:
    #         # 기존 데이터 스킵, 다음 row 이동
    #         return RowResult()

    #     # 새로운 데이터 처리
    #     title = row.get('title')

    #     if title and Movie.objects.filter(title=title).exists():
    #         # 중복 데이터 스킵, 다음 row 이동
    #         return RowResult()
    
    #     return super().before_import_row(row, **kwargs)