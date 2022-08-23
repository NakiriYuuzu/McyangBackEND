from django.apps import AppConfig

class FooConfig(AppConfig):
    name = 'full.python.path.to.your.app.foo'
    label = 'my.foo'  # <-- this is the important line - change it to anything other than the default, which is the module name ('foo' in this case)
    default_app_config = 'full.python.path.to.your.app.foo.apps.FooConfig'