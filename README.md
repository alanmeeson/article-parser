# Article Parser

Extracts text, figures and tables from academic journal articles.

## Getting Started

### Install & Use

```bash
pip install -r requirements_prod_pt1.txt
pip install -r requirements_prod_pt2.txt

python -m article_parser paper.pdf out_dir
```

Note: the two separate install files,  this is because Detectron2 will fail to install if torch is not 
already present.

### Setting up a development environment

```bash
pip install -r requirements_dev.txt
pip install -r requirements_prod_pt1.txt
pip install -r requirements_prod_pt2.txt
```
