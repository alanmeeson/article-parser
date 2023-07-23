import numpy as np
import layoutparser as lp
import fitz

from tqdm import tqdm
from typing import Dict
from PIL import Image
from article_parser.text_parser import ocr_text_blocks, extract_text_blocks
from article_parser.figure_parser import extract_figure_blocks
from article_parser.table_parser import extract_table_blocks

from layoutparser.models.base_layoutmodel import BaseLayoutModel
from layoutparser.models.detectron2.layoutmodel import Detectron2LayoutModel


def parse_article(pdf: fitz.Document, layout_model: BaseLayoutModel) -> Dict:
    document = {
        'num_pages': len(pdf),
        'text': list(),
        'figures': list(),
        'tables': list()
    }

    for page_num, page in tqdm(enumerate(pdf), total=len(pdf), desc="Processing PDF", unit='pages'):
        image = get_page_image(page)
        layout = layout_model.detect(image)
        layout = sort_layout_by_columns(layout)
        layout = ocr_text_blocks(layout, image)

        page_text_blocks = extract_text_blocks(layout, page_num)
        page_figure_blocks = extract_figure_blocks(layout, image, page_num)
        page_table_blocks = extract_table_blocks(layout, image, page_num)

        document['text'].extend(page_text_blocks)
        document['figures'].extend(page_figure_blocks)
        document['tables'].extend(page_table_blocks)

    return document


def get_page_image(page: fitz.Page) -> Image:
    """Extract an image of a page from a PDF"""

    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

    return img


def sort_layout_by_columns(layout: lp.Layout) -> lp.Layout:
    """Sorts the blocks in the layout by columns."""

    column_width = np.median([block.width for block in layout])
    return layout.sort(
        key=lambda block: (
            block.coordinates[0] // column_width,  # column number
            block.coordinates[1]  # Y position
        )
    )


def load_layout_model(config_path: str, model_path: str = None) -> Detectron2LayoutModel:
    """Load one of the PubLayNet models.

    This should work with any of the PubLayNet models listed on the LayoutParser Model Zoo.
    https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html

    Best results are likely with: lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config

    Args:
        config_path: either a path to a config.yaml, or the lp:// config string.
        model_path: a path to a model_final.pth weights file, or None
    Returns:
        the Detectrion2LayoutModel.
    """

    return lp.Detectron2LayoutModel(
        config_path=config_path,
        model_path=model_path,
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
    )
