from django.contrib import admin  # type: ignore

from base.models import Config, Frame, Message, Movie, MovieRun, Run, User


@admin.register(Run)
class RunCustomAdmin(admin.ModelAdmin):
    list_display = [  # noqa: RUF012
        'user',
        'current_hint',
        'movies_left',
        'total_points',
    ]

    search_fields = [  # noqa: RUF012
        'user__username',
        'user__email',
    ]
    
    readonly_fields = [  # noqa: RUF012
        'updated',
        'created'
    ]
    
@admin.register(Movie)
class MovieCustomAdmin(admin.ModelAdmin):
    list_display = [  # noqa: RUF012
        'id',
        'name',
        'year',
        'director',
        'hints_amount',
        'total_hits',
        'total_misses',
        'total_hints_used',
        'difficulty_level'
    ]

    search_fields = [  # noqa: RUF012
        'name',
        'year',
        'director',
        'difficulty_level'
    ]
    
    readonly_fields = [  # noqa: RUF012
        'updated',
        'created'
    ]

@admin.register(Frame)
class FrameCustomAdmin(admin.ModelAdmin):
    list_display = [  # noqa: RUF012
        'id',
        'movie',
        'hint_index',
        'image'
    ]

    search_fields = [  # noqa: RUF012
        'movie__name',
        'movie__difficulty_level',
        'hint_index'
    ]
    
    readonly_fields = [  # noqa: RUF012
        'updated',
        'created'
    ]

@admin.register(MovieRun)
class MovieRunCustomAdmin(admin.ModelAdmin):
    list_display = [  # noqa: RUF012
        'id',
        'run',
        'user',
        'original_movie',
        'has_hit',
        'has_missed',
        'points',
        'difficulty'
    ]

    @admin.display()
    def user(self, obj):
        return obj.run.user

    @admin.display()
    def difficulty(self, obj):
        return obj.original_movie.difficulty_level
    
    search_fields = [  # noqa: RUF012
        'run__user__username',
        'original_movie__name',
        'original_movie__year',
        'original_movie__director',
        'original_movie__difficulty_level',
    ]
    
    readonly_fields = [  # noqa: RUF012
        'updated',
        'created'
    ]
    
@admin.register(Config)
class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = [  # noqa: RUF012
        'name',
        'value'
    ]

@admin.register(User)
class UserCustomAdmin(admin.ModelAdmin):
    search_fields = [  # noqa: RUF012
        'username',
        'email'
    ]

    readonly_fields = [  # noqa: RUF012
        'updated',
        'created'
    ]

@admin.register(Message)
class MessagesCustomAdmin(admin.ModelAdmin):
    search_fields = [  # noqa: RUF012
        'user__username',
        'text'
    ]

    readonly_fields = [  # noqa: RUF012
        'updated',
        'created'
    ]