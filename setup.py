try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # if setuptools breaks


# Dynamically calculate the version
def get_version():
    with open("django_rest_webhooks/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


print(get_version())

setup(
    name="django-rest-webhooks",
    description="A powerful mechanism for sending real time API notifications via a new subscription model.",
    version=get_version(),
    author="Bohdan Datsko",
    author_email="bohdan.datsko8888@gmail.com",
    url="https://github.com/leanrank/django-web-hooks",
    install_requires=["Django>=1.8", "requests>=2.25.1"],
    packages=["django_rest_webhooks"],
    package_data={"django_rest_webhooks": ["migrations/*.py"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
