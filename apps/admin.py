from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from apps.form import GroupForm
from .models import Users, Role, Project, ProjectRolesUsers, Resource, Application, Account

# Register your models here.
admin.site.unregister(Group)


# 用户管理
@admin.register(Users)
class UsersAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "display",
        "phone",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    search_fields = ("id", "username", "display", "email", "phone")
    list_display_links = (
        "id",
        "username",
    )
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("认证信息", {"fields": ("username", "password")}),
        (
            "个人信息",
            {
                "fields": (
                    "phone",
                    "display",
                    "email",
                    "ding_user_id",
                    "wx_user_id",
                    "feishu_open_id",
                )
            },
        ),
        (
            "权限信息",
            {
                "fields": (
                    "is_superuser",
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("其他信息", {"fields": ("date_joined", "failed_login_count")}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("认证信息", {"fields": ("username", "password1", "password2")}),
        (
            "个人信息",
            {
                "fields": (
                    "phone",
                    "display",
                    "email",
                    "ding_user_id",
                    "wx_user_id",
                    "feishu_open_id",
                )
            },
        ),
        (
            "权限信息",
            {
                "fields": (
                    "is_superuser",
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups",)


# 用户组管理
@admin.register(Group)
class GroupAdminNew(GroupAdmin):
    form = GroupForm
    fieldsets = (
        ("权限组信息", {"fields": ("name", "permissions")}),
        ("用户信息", {"fields": ("users",)}),
    )

    def save_model(self, request, obj, form, change):
        # save first to obtain id
        super(GroupAdmin, self).save_model(request, obj, form, change)
        obj.user_set.clear()
        for user in form.cleaned_data["users"]:
            obj.user_set.add(user)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields["users"].initial = [o.pk for o in obj.user_set.all()]
        else:
            self.form.base_fields["users"].initial = []
        return GroupForm


# 角色管理
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "role_name", "role_code", "description", "create_time", "update_time", "creator")
    search_fields = ("id", "role_name", "role_code", "description", "create_time", "update_time", "creator")
    list_display_links = ("id", "role_name")
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("角色信息", {"fields": ("role_name", "role_code", "description")}),
        ("创建信息", {"fields": ("creator",)}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("角色信息", {"fields": ("role_name", "role_code", "description")}),
    )
    list_filter = ("create_time", "update_time", "creator")


# 项目管理
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_name", "project_type", "project_code", "description", "create_time", "update_time", "creator")
    search_fields = (
        "project_name", "project_type", "project_code", "description", "create_time", "update_time", "creator")
    list_display_links = ("project_name",)
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("项目信息", {"fields": ("project_name", "project_type", "project_code", "description")}),
        ("创建信息", {"fields": ("creator",)}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("项目信息", {"fields": ("project_name", "project_type", "project_code", "description")}),
    )
    list_filter = ("create_time", "update_time", "creator")


# 资源管理
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("id", "resource_name", "resource_type", "description", "create_time", "update_time", "creator")
    search_fields = ("id", "resource_name", "resource_type", "description", "create_time", "update_time", "creator")
    list_display_links = ("id", "resource_name")
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("应用信息", {"fields": (
            "resource_name",
            "resource_type",
            "resource_ip",
            "resource_cpu",
            "resource_memory",
            "resource_disk",
            "resource_os",
            "description",
            "project"
        )}),
        ("创建信息", {"fields": ("creator",)}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("应用信息", {"fields": (
            "resource_name",
            "resource_type",
            "resource_ip",
            "resource_cpu",
            "resource_memory",
            "resource_disk",
            "resource_os",
            "description"
        )}),
    )
    list_filter = ("create_time", "update_time", "creator")


# 应用管理
@admin.register(Application)
class Application(admin.ModelAdmin):
    list_display = (
        "id", "application_name", "deploy_type", "application_type", "application_code", "description", "create_time",
        "update_time",
        "creator")
    search_fields = (
        "id", "application_name", "deploy_type", "application_type", "application_code", "description", "create_time",
        "update_time",
        "creator")
    list_display_links = ("id", "application_name")
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("应用信息", {"fields": (
            "application_name",
            "deploy_type",
            "application_type",
            "application_code",
            "application_port",
            "resource",
            "description",
            "project"
        )}),
        ("创建信息", {"fields": ("creator",)}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("应用信息", {"fields": (
            "application_name",
            "application_type",
            "application_code",
            "application_port",
            "resource",
            "description",
            "project"
        )}),
    )
    list_filter = ("create_time", "update_time", "creator")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id", "account_name", "account_type", "description", "create_time", "update_time", "creator")
    search_fields = (
        "id", "account_name", "account_type", "description", "create_time", "update_time", "creator")
    list_display_links = ("id", "account_name")
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("账号信息", {"fields": (
            "account_name", "account_password", "resource", "application", "account_type", "description")}),
        ("创建信息", {"fields": ("creator",)}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("账号信息", {"fields": (
            "account_name", "account_password", "resource", "application", "account_code", "description", "project")}),
    )
    list_filter = ("create_time", "update_time", "creator")


# 项目角色管理
@admin.register(ProjectRolesUsers)
class ProjectRolesUsersAdmin(admin.ModelAdmin):
    list_display = (
        "project", "role", "users", "create_time", "update_time")
    search_fields = (
        "project", "role", "users", "create_time", "update_time")
    list_display_links = ("project",)
    ordering = ("id",)
    # 编辑页显示内容
    fieldsets = (
        ("项目角色信息", {"fields": ("project", "role", "users")}),
    )
    # 添加页显示内容
    add_fieldsets = (
        ("项目角色信息", {"fields": ("project", "role", "users")}),
    )
    list_filter = ("create_time", "update_time")
