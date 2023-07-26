import numpy as np
import pytesseract
import layoutparser as lp

from typing import List, Dict, Set, Union
from PIL import Image


TEXT_BLOCKS = {'Text', 'Title', 'List'}  # Types of block to be considered as text


def ocr_text_blocks(layout: lp.Layout, image: Image) -> lp.Layout:
    """Applies TesseractOCR to each text block"""

    for block in layout:
        if block.type in TEXT_BLOCKS:
            text_image = block.pad(15, 5, 15, 5).crop_image(np.array(image))
            text = pytesseract.image_to_string(text_image, config='--oem 3 --psm 6')
            text = text.replace("-\n", '').replace('\n', ' ').strip()
            block.set(text=text, inplace=True)

    return layout


def extract_text_blocks(layout: lp.Layout, page_num: int) -> List[Dict]:
    return [
        {
            'text': block.text,
            'type': block.type,
            'coordinates': {
                'x1': block.block.coordinates[0],
                'y1': block.block.coordinates[1],
                'x2': block.block.coordinates[2],
                'y2': block.block.coordinates[3]
            },
            'score': block.score,
            'page': page_num,
            'block_id': block_idx
        } for block_idx, block
        in enumerate(layout)
        if block.type in TEXT_BLOCKS
    ]


def identify_caption(
        target_idx: lp.TextBlock,
        layout: lp.Layout,
        first_pass_offsets: List = None,
        candidates_start_with: Set = None
) -> Union[str, None]:
    """Identifies the text block most likely to contain the caption for the target block, and returns its text.

    Args:
        target_idx: the index of the target block in the layout list
        layout: the list of all blocks
        first_pass_offsets: a list of offsets relative to the target_idx to look at first. Eg: [1, -1] the one below and one above.
        candidates_start_with: a set of strings to require that captions start with one of.
    Return:
        The caption text.
    """

    candidate_captions = None

    if first_pass_offsets:
        # first try the blocks immediately below and above the image, remembering to handle boundary cases
        num_blocks = len(layout)
        candidate_caption_idxs = [target_idx + offset for offset in first_pass_offsets]
        candidate_caption_idxs = [idx for idx in candidate_caption_idxs if ((idx >= 0) & (idx < num_blocks))]
        candidate_captions = [layout[idx] for idx in candidate_caption_idxs]

        if candidates_start_with:
            candidate_captions = [
                candidate_caption
                for candidate_caption
                in candidate_captions
                if candidate_caption.text and any(map(candidate_caption.text.lower().startswith, candidates_start_with))
            ]

    # Then failing that, try all text blocks by distance
    if not candidate_captions:
        # find those that have plausible text
        candidate_captions = [block for block in layout if block.type in TEXT_BLOCKS]

        if candidate_captions and candidates_start_with:
            candidate_captions = [
                candidate_caption
                for candidate_caption
                in candidate_captions
                if candidate_caption.text and any(map(candidate_caption.text.lower().startswith, candidates_start_with))
            ]

        if candidate_captions:
            target_block = layout[target_idx]
            candidate_captions = candidate_captions.sort(
                key=lambda block: sum(
                    pow(a - b, 2) for a, b in zip(block.block.center, target_block.block.center)
                )
            )

    return candidate_captions[0].text if candidate_captions else None
