import os
import json
import numpy as np

from PIL import Image


def output_json(document: str, out_path: str):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # save figures as png
    if document['figures']:
        num_figure_digits = int(np.ceil(np.log10(len(document['figures']))))
        for figure_num, figure in enumerate(document['figures']):
            figure_name = "figure%0*d.png" % (num_figure_digits, figure_num)

            if isinstance(figure['image'], np.ndarray):
                figure_image = Image.fromarray(figure['image'])
            elif isinstance(figure['image'], Image):
                figure_image = figure['image']
            else:
                raise ValueError("Figure %0*d is neither a numpy array or a PIL Image." % (num_figure_digits, figure_num))
            figure_image.save(os.path.join(out_path, figure_name), format='png')

            figure['image'] = figure_name

    # save tables as png/csv
    if document['tables']:
        num_table_digits = int(np.ceil(np.log10(len(document['tables']))))
        for table_num, table in enumerate(document['tables']):
            table_name = "table%0*d" % (num_table_digits, table_num)
            table_image_name = f"{table_name}.png"
            table_csv_name = f"{table_name}.csv"

            if isinstance(table['image'], np.ndarray):
                table_image = Image.fromarray(table['image'])
            elif isinstance(table['image'], Image):
                table_image = table['image']
            else:
                raise ValueError("Image for Table %0*d is neither a numpy array or a PIL Image." % (num_table_digits, table_num))

            table_image.save(os.path.join(out_path, table_image_name), format='png')
            table['image'] = table_image_name

            if table.get('table', None) is not None:
                table['table'].to_csv(os.path.join(out_path, table_csv_name), index=False, header=False)
                table['table'] = table_csv_name

    # output the document as json
    document_json_file = os.path.join(out_path, 'document.json')
    with open(document_json_file, 'w') as fp:
        json.dump(document, fp)
