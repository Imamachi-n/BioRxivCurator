from argparse import ArgumentParser
import yaml


def get_argument():
    argparser = ArgumentParser()
    argparser.add_argument('--yaml_setting_file', type=str,
                           help="yaml setting file", required=True)
    args = argparser.parse_args()

    with open(args.yaml_setting_file) as file:
        obj = yaml.load(file)

    return obj
