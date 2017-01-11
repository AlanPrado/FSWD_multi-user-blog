import os
from jinja2 import Environment, FileSystemLoader

SECRET = 'ABCDEF'

def set_templates(template_dir):
    return Environment(
        loader = FileSystemLoader(template_dir),
        autoescape = True
    )
