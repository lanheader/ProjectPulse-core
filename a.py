# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppsApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    application_name = models.CharField(unique=True, max_length=50)
    application_type = models.CharField(max_length=50)
    application_code = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    application_port = models.IntegerField(blank=True, null=True)
    creator = models.ForeignKey("AppsUsers", models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey("AppsProject", models.DO_NOTHING, blank=True, null=True)
    resource = models.ForeignKey(
        "AppsResource", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apps_application"


class AppsProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(unique=True, max_length=50)
    project_type = models.CharField(max_length=50)
    project_code = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    creator = models.ForeignKey("AppsUsers", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apps_project"


class AppsProjectMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(AppsProject, models.DO_NOTHING)
    users = models.ForeignKey("AppsUsers", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apps_project_members"
        unique_together = (("project", "users"),)


class AppsResource(models.Model):
    id = models.BigAutoField(primary_key=True)
    resource_name = models.CharField(unique=True, max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_ip = models.CharField(max_length=39, blank=True, null=True)
    resource_cpu = models.IntegerField(blank=True, null=True)
    resource_memory = models.IntegerField(blank=True, null=True)
    resource_disk = models.IntegerField(blank=True, null=True)
    resource_os = models.CharField(max_length=50)
    description = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    creator = models.ForeignKey("AppsUsers", models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(AppsProject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apps_resource"


class AppsRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)
    role_code = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    creator = models.ForeignKey("AppsUsers", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apps_roles"


class AppsRolesMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(AppsRoles, models.DO_NOTHING)
    users = models.ForeignKey("AppsUsers", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apps_roles_members"
        unique_together = (("role", "users"),)


class AppsUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    display = models.CharField(max_length=50)
    ding_user_id = models.CharField(max_length=64)
    wx_user_id = models.CharField(max_length=64)
    feishu_open_id = models.CharField(max_length=64)
    failed_login_count = models.IntegerField()
    last_login_failed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apps_users"


class AppsUsersGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    users = models.ForeignKey(AppsUsers, models.DO_NOTHING)
    group = models.ForeignKey("AuthGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apps_users_groups"
        unique_together = (("users", "group"),)


class AppsUsersUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    users = models.ForeignKey(AppsUsers, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apps_users_user_permissions"
        unique_together = (("users", "permission"),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
