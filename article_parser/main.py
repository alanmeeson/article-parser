import os
import fitz
import argparse

from article_parser.article_parser import parse_article, load_layout_model
from article_parser.output_json import output_json


def parse_single_pdf(pdf_filename: str, out_path: str, config_path: str = None, model_path: str = None):

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


def main():
    parser = argparse.ArgumentParser(
        prog="Article Parser",
        description="Parses academic papers to extract text, figures and tables"
    )

    parser.add_argument('pdf', type=argparse.FileType('rb'), help="The pdf file to parse")
    parser.add_argument('out_path', type=str, help="Dir to write output into")
    parser.add_argument('--config_path', type=str, default=None, help="The config_path for the layout model to use")
    parser.add_argument('--model_path', type=str, default=None, help="The model_path for the layout model to use")

    args = parser.parse_args()

    config_path = args.config_path
    model_path = args.model_path
    if not config_path:
        if os.path.exists('./model/config.yaml'):
            config_path = './model/config.yaml'

            if os.path.exists('./model/model_final.pth'):
                model_path = './model/model_final.pth'

    parse_single_pdf(args.pdf, args.out_path, config_path=config_path, model_path=model_path)
