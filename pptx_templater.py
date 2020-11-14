import csv
import logging
import os
import json

from pptx import Presentation
from pptx_template.cli import process_all_slides

from jinja2 import FileSystemLoader, Environment
import click

log = logging.getLogger()


def get_model_template(filename):
    template_loader = FileSystemLoader(searchpath=os.path.dirname(filename))
    template_env = Environment(loader=template_loader)
    model_template = template_env.get_template(os.path.split(filename)[-1])
    return model_template


def get_csv_data_file(filename):
    data = []
    with open(filename, 'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


DEFAULT_TEMPLATE = 'template.pptx'
DEFAULT_MODEL_TEMPLATE = 'model.json'
DEFAULT_DATA = 'data.csv'


@click.command()
@click.option('--template', nargs=1, type=click.Path(exists=True), help='template pptx file (required)')
@click.option('--model-template', nargs=1, type=click.Path(exists=True),
              help='model object with .json or .xlsx format (required) -> jinja2 templating encouraged here')
@click.option('--data', nargs=1, type=click.Path(exists=True), help='csv data file passed to model template')
@click.option('--out', nargs=1, type=click.Path(exists=False), help='created pptx file (required)', required=True)
@click.option('--skip-model-not-found/--raise', default=True, type=bool,
              help='skip if specified key is not found in the model')
@click.option('--debug/--live', default=False, type=bool, help='output verbose log')
def cli(template, model_template, data, out, skip_model_not_found, debug):
    """
    When you need a template for your pptx-template
    """

    if not len(log.handlers):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        log.addHandler(handler)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    line = '-------------------------------------------'
    if template[-5:] != '.pptx':
        click.echo('--template extension must be .pptx')
        return

    log.info(f'{line}\nLoading model template: {model_template}')
    model_template_ = get_model_template(model_template)

    if out[-5:] != '.pptx':
        click.echo('--out extension must be .pptx')
        return

    if data:
        if data[-4:] != '.csv':
            click.echo('--data extension must be .csv (for the time being)')
            return

        log.info(f'Loading csv file: {data}')
        data = get_csv_data_file(data)
    else:
        data = ['0']

    for i, elem in enumerate(data):
        # elem should be a dict or list
        # or a str == '0' (this happens when no --data is input - same behavior as ppt-template)

        log.info(f'{line}\nLoading pptx template: {template}')
        ppt = Presentation(template)

        log.info(f'Rendering model template {i}')
        rendered_model_template = model_template_.render(data=elem)

        # this model var passed directly to pptx-template cli
        model = json.loads(rendered_model_template)
        slides = model['slides']

        if elem != '0':
            log.info(f'Processing {elem}')
        process_all_slides(slides, ppt, skip_model_not_found=skip_model_not_found)

        if elem == '0':
            out_file = out
        else:
            out_file = out[:-5] + f'{i}' + out[-5:]

        log.info(f'Saving pptx: {out_file}')
        ppt.save(out_file)
