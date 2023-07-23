import argparse
import os

from article_parser.main import main


if __name__ == "__main__":
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
        if os.path.exists('./model/config.yml'):
            config_path = './model/config.yml'

            if os.path.exists('./model/model_final.pth'):
                model_path = './model/model_final.pth'

    main(args.pdf, args.out_path, config_path, model_path)
