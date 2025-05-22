from setuptools import setup, find_packages

setup(
    name="dramatiq_task_history_middleware",
    version="0.4.10",
    package_dir={"": "dramatiq_task_history_middleware"},
    packages=find_packages(where="dramatiq_task_history_middleware"),
    install_requires=[
        "django>=3.0.0",
        "dramatiq>=1.12.0",
        "djangorestframework>=3.15.0",
        "django-filter>=24",
        "drf-nested-routers>=0.90.2",
        "psycopg2-binary==2.9.10",
    ],
    author="Ahmet Can Ogreten",
    author_email="ahmetcan@lidyagenomics.com",
    description="A dramatiq task history middleware package for Lidya",
    keywords="dramatiq, task, history, middleware",
    url="https://github.com/LidyaGenomics/dramatiq_task_history_middleware.git",
    python_requires=">=3.10",
)