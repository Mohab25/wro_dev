from flask import render_template, redirect, url_for, Blueprint
from ckan.plugins import toolkit

map_blueprint = Blueprint('map', __name__, url_prefix='/map', template_folder="templates")

@map_blueprint.route('/')
def custom_map():
    """
        renders a custom map enables the user to draw
        a bounding box or pick up a geographic location,
        the actual handling of map input is via js module.
    """
    return render_template('blueprints_templates/custom_map.html')