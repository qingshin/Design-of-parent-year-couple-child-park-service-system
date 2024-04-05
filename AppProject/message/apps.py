from django.apps import AppConfig

"""
包含应用程序的配置信息，如应用程序的名称、标签等。
"""


class MessageAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "message"
