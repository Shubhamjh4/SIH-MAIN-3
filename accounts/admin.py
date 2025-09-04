from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from courses.models import Enrollment, Progress
from .models import UserProfile


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    verbose_name = 'Enrolled Course'
    verbose_name_plural = 'Enrolled Courses'


class CourseProgressInline(admin.TabularInline):
    model = Progress
    fk_name = 'user'
    extra = 0
    fields = ('course', 'percentage', 'completed', 'points', 'last_accessed')
    readonly_fields = ('last_accessed',)
    verbose_name = 'Course Progress'
    verbose_name_plural = 'Course Progress'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, EnrollmentInline, CourseProgressInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('userprofile__role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'userprofile__school_name')

    def get_role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else '-'
    get_role.short_description = 'Role'


# Re-register UserAdmin once
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
