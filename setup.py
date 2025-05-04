from setuptools import setup, find_packages

setup(
    name="dramatiq_task_history_middleware",
    version="0.1.0",
    packages=["dramatiq_task_history_middleware"],
    install_requires=[
        "django>=4.2.0",
        "dramatiq>=1.12.0",
    ],
    author="Ahmet Can Ogreten",
    author_email="ahmetcan@lidyagenomics.com",
    description="A dramatiq task history middleware package for Lidya",
    keywords="dramatiq, task, history, middleware",
    url="https://github.com/LidyaGenomics/dramatiq_task_history_middleware.git",
    python_requires=">=3.10",
)