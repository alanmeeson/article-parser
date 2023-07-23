import io
import numpy as np
import pandas as pd
import layoutparser as lp
import PIL

from typing import List, Dict, Union
from article_parser.text_parser import identify_caption
from img2table.ocr import TesseractOCR
from img2table.document import Image


ocr = TesseractOCR()


def extract_table_blocks(layout: lp.Layout, image: PIL.Image, page_num: int) -> List[Dict]:
    """Extracts all tables from the layout, and finds their captions, and extracts their data"""
    tables = []

    tables_idxs = [idx for idx, b in enumerate(layout) if b.type == 'Table']

    for table_idx in tables_idxs:
        table_block = layout[table_idx]
        table_image = table_block.pad(15, 15, 15, 15).crop_image(np.array(image))
        table_data = extract_table_data(table_image)

        caption = identify_caption(
            table_idx, layout,
            first_pass_offsets=[-1, 1], # The one above, then the one below
            candidates_start_with={'tab', 'table'}
        )

        tables.append({
            'table': table_data,
            'image': table_image,
            'caption': caption,
            'type': table_block.type,
            'coordinates': {
                'x1': table_block.block.coordinates[0],
                'y1': table_block.block.coordinates[1],
                'x2': table_block.block.coordinates[2],
                'y2': table_block.block.coordinates[3]
            },
            'score': table_block.score,
            'page': page_num,
            'block_id': table_idx
        })

    return tables


def extract_table_data(image: Union[np.array, 'PIL.Image']) -> pd.DataFrame:
    """Uses img2table to pull the table data out of the table image"""

    if isinstance(image, np.ndarray):
        image = PIL.Image.fromarray(image)

    buf = io.BytesIO()
    image.save(buf, format='png')
    doc = Image(buf.getvalue())

    extracted_tables = doc.extract_tables(
        ocr,
        implicit_rows=True,
        borderless_tables=True,
        min_confidence=50
    )

    data = None

    if extracted_tables:
        data = extracted_tables[0].df

    return data
