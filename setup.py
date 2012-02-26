from distutils.core import setup
setup(name="django-jqresources",
      version="0.1.0",
      author="Aleksander Zdyb",
      author_email="azdyb@live.com",
      description="An Django application, which helps managing JavaScript"
                    " and CSS resources",
      long_description=open("README.rst").read(),
      license="GPL",
      url="http://github.com/ojo/django-jqresources",
      packages=["jqresources", "jqresources.templatetags"])
