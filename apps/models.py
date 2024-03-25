from django.contrib.auth.models import AbstractUser
from django.db import models
from mirage import fields

from .utils.const import ResourceType, DeployType


# Create your models here.
class Users(AbstractUser):
    """
    用户信息扩展
    """
    phone = models.CharField("手机号", max_length=11, blank=True)
    display = models.CharField("显示的中文名", max_length=50, default="")
    ding_user_id = models.CharField("钉钉UserID", max_length=64, blank=True)
    wx_user_id = models.CharField("企业微信UserID", max_length=64, blank=True)
    feishu_open_id = models.CharField("飞书OpenID", max_length=64, blank=True)
    failed_login_count = models.IntegerField("失败计数", default=0)
    last_login_failed_at = models.DateTimeField("上次失败登录时间", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.failed_login_count = min(127, self.failed_login_count)
        self.failed_login_count = max(0, self.failed_login_count)
        super(Users, self).save(*args, **kwargs)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def __str__(self):
        if self.display:
            return self.display
        return self.username

    class Meta:
        managed = True
        db_table = "apps_users"
        verbose_name = "用户管理"
        verbose_name_plural = "用户管理"


class Role(models.Model):
    """
    角色信息
    """

    role_name = models.CharField("角色名称", max_length=50, unique=True)
    role_code = models.CharField("角色代码", max_length=50, unique=True)
    description = models.TextField("角色描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    creator = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="role_creator")

    def __str__(self):
        return self.role_name

    class Meta:
        managed = True
        db_table = "apps_roles"
        verbose_name = "角色管理"
        verbose_name_plural = "角色管理"


class Project(models.Model):
    """
    项目信息
    """

    project_name = models.CharField("项目名称", max_length=50, unique=True)
    project_type = models.CharField("项目类型", max_length=50, default="default")
    project_code = models.CharField("项目代码", max_length=50, unique=True)
    description = models.TextField("项目描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    creator = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="creator")

    def __str__(self):
        return self.project_name

    class Meta:
        managed = True
        db_table = "apps_project"
        verbose_name = "项目管理"
        verbose_name_plural = "项目管理"


class Resource(models.Model):
    """
    资源信息
    """

    resource_name = models.CharField("资源名称", max_length=50, unique=True)
    resource_type = models.IntegerField("资源类型", choices=ResourceType.choices, default=1)
    resource_ip = models.GenericIPAddressField("资源IP", blank=True, null=True)
    resource_cpu = models.IntegerField("资源CPU", blank=True, null=True)
    resource_memory = models.IntegerField("资源内存", blank=True, null=True)
    resource_disk = models.IntegerField("资源磁盘", blank=True, null=True)
    resource_os = models.CharField("资源操作系统", max_length=50, blank=True)
    description = models.TextField("资源描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    creator = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="resource_creator")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="resource_project")

    def __str__(self):
        return self.resource_name

    class Meta:
        managed = True
        db_table = "apps_resource"
        verbose_name = "资源管理"
        verbose_name_plural = "资源管理"


# 应用表
class Application(models.Model):
    """
    应用信息
    """

    application_name = models.CharField("应用名称", max_length=50, unique=True)
    application_type = models.CharField("应用类型", max_length=50, default="default")
    deploy_type = models.IntegerField("部署类型", choices=DeployType.choices, default=0)
    application_code = models.CharField("应用代码", max_length=50, unique=True)
    description = models.TextField("应用描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    creator = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="application_creator")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="application_project")
    application_port = models.IntegerField("应用端口", blank=True, null=True)
    webhook = models.CharField("Webhook", max_length=255, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, related_name="application_resource")

    def __str__(self):
        return self.application_name

    class Meta:
        managed = True
        db_table = "apps_application"
        verbose_name = "应用管理"
        verbose_name_plural = "应用管理"


class ProjectRolesUsers(models.Model):
    """
    项目角色信息
    """
    role = models.ForeignKey(Role, models.DO_NOTHING, verbose_name="角色")
    users = models.ForeignKey('Users', models.DO_NOTHING, verbose_name="用户")
    project = models.ForeignKey(Project, models.DO_NOTHING, verbose_name="项目")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'apps_project_roles'
        managed = True
        unique_together = (('role', 'users', 'project'),)
        verbose_name = "项目角色管理"
        verbose_name_plural = "项目角色管理"


# 账号密码管理
class Account(models.Model):
    """
    账号信息
    """
    account_name = models.CharField("账号名称", max_length=200)
    account_password = fields.EncryptedCharField(verbose_name="账号密码", max_length=300)
    account_type = models.IntegerField("账号类型", choices=ResourceType.choices, null=True, blank=True)
    description = models.TextField("账号描述", blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    creator = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="account_creator",
                                verbose_name="创建人")
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="account_resource",
                                 verbose_name="资源")
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="account_application", verbose_name="应用")

    def __str__(self):
        return self.account_name

    class Meta:
        managed = True
        db_table = "apps_account"
        verbose_name = "账号管理"
        verbose_name_plural = "账号管理"
