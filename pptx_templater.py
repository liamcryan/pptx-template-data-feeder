import csv
import logging
import json
import re

from pptx import Presentation
from pptx_template.cli import process_all_slides

from jinja2 import Template
import click

log = logging.getLogger()


def jinja_sub(jinja_str: str):
    # >>> import re
    # >>> re.sub(r'{{([a-z]+)}}', r'{{data.\1}}', 'my-output-file-{{name}}-{{company}}.pptx')
    # 'my-output-file-{{data.name}}-{{data.company}}.pptx'
    # {{_}}
    # {{_asdf_asdf_asdf123213ffd_f3ef____1}}
    return re.sub(r'{{(_*\D\w*)}}', r'{{data.\1}}', jinja_str)


def get_model_template(filename):
    with open(filename, 'rt') as f:
        return Template(jinja_sub(f.read()))


def get_csv_data_file(filename):
    with open(filename, 'rt') as f:
        reader = csv.DictReader(f)
        return list(reader)


@click.command()
@click.option('--template', nargs=1, type=click.Path(exists=True), help='template pptx file (required)')
@click.option('--model-template', nargs=1, type=click.Path(exists=True),
              help='model object with .json or .xlsx format (required) -> jinja2 templating encouraged here')
@click.option('--data', nargs=1, type=click.Path(exists=True), help='csv data file passed to model template')
@click.option('--out', nargs=1, type=click.Path(exists=False), help='created pptx file (required)', required=True)
@click.option('--skip-model-not-found/--raise', default=True,
              help='skip if specified key is not found in the model')
@click.option('--debug/--live', default=False, help='output verbose log')
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
        # ...this is kind of an odd way of doing things...

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
            output_file_template = Template(jinja_sub(out))
            out_file = output_file_template.render(data=elem)
            if out == out_file:  # this means that user did not use output file templating
                out_file = out[:-5] + f'{i}' + out[-5:]

        log.info(f'Saving pptx: {out_file}')
        ppt.save(out_file)
