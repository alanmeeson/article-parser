import os
import fitz

from article_parser.article_parser import parse_article, load_layout_model
from article_parser.output_json import output_json


def main(pdf_filename: str, out_path: str, config_path: str = None, model_path: str = None):

    if not config_path:
        # If no config provided, default to a sensible one and implicitly download it if first time it's used.
        config_path = 'lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config'
        model_path = None

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    model = load_layout_model(config_path, model_path)

    pdf = fitz.open(pdf_filename)
    document = parse_article(pdf, model)
    output_json(document, out_path)
