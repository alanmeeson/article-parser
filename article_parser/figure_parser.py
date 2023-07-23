import numpy as np
import layoutparser as lp

from typing import List, Dict
from article_parser.text_parser import identify_caption
from PIL import Image


def extract_figure_blocks(layout: lp.Layout, image: Image, page_num: int) -> List[Dict]:
    """Extracts all figures from the layout, and finds their captions"""
    figures = []

    figure_idxs = [idx for idx, b in enumerate(layout) if b.type == 'Figure']

    for figure_idx in figure_idxs:
        figure_block = layout[figure_idx]
        figure_image = figure_block.pad(15, 15, 15, 15).crop_image(np.array(image))
        caption = identify_caption(
            figure_idx, layout,
            first_pass_offsets=[1, -1],  # The block below and the block above.
            candidates_start_with={'fig', 'figure'}
        )

        figures.append({
            'image': figure_image,
            'caption': caption,
            'type': figure_block.type,
            'coordinates': {
                'x1': figure_block.block.coordinates[0],
                'y1': figure_block.block.coordinates[1],
                'x2': figure_block.block.coordinates[2],
                'y2': figure_block.block.coordinates[3]
            },
            'score': figure_block.score,
            'page': page_num,
            'block_id': figure_idx
        })

    return figures
