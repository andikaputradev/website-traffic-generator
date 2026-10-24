"""Setup configuration for Website Traffic Generator."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [
        line.strip() for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="website-traffic-generator",
    version="1.0.0",
    author="Wahyu Andika Putra",
    author_email="wahyuandikaputra.co.id@gmail.com",
    description=(
        "An open-source website traffic generator with realistic human "
        "behavior simulation, proxy rotation, and traffic source spoofing."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andikaputradev/website-traffic-generator",
    project_urls={
        "Author Website": "https://andikadev.com",
        "Author Profile": "https://github.com/andikaputradev",
        "LinkedIn": "https://linkedin.com/in/wahyu-andika-putra",
    },
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "website-traffic-generator=run_traffic:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Networking",
    ],
    keywords=[
        "website traffic generator",
        "traffic generator",
        "web traffic",
        "website visitors",
        "traffic automation",
        "SEO tools",
        "load testing",
        "analytics testing",
        "headless browser",
        "proxy rotation",
    ],
)
