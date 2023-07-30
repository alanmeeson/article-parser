from setuptools import setup, find_packages

setup(
    name='ArticleParser',
    version='0.2.0',
    description='A tool for extracting text, figures and tables from academic papers.',
    author="Alan Meeson",
    author_email="alan@carefullycalculated.co.uk",
    install_requires=[
        'PyMuPDF',
        'torch',
        'torchvision',
        'opencv-python-headless',
        'pytesseract',
        'img2table',
        'tqdm',
        'detectron2 @ git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2',
        'layoutparser[ocr]',
        'Pillow==9.0.1'
    ],
    entry_points={
        'console_scripts': [
            'article-parser = article_parser:main'
        ]
    },
    packages=find_packages(
        where='.',
        include=['article_parser'],
        exclude=['data', 'model', 'notebooks']
    )
)
