from flask import request,  Response, render_template, redirect, url_for, Blueprint
from ckan.plugins import toolkit
import xml.dom.minidom as dom
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

xml_parser_blueprint = Blueprint('xml_parser', __name__, url_prefix='/dataset/xml_parser', template_folder="templates")

@xml_parser_blueprint.route('/', methods=['GET', 'POST'])
def parse_xml_dataset_upload():
    """
        parsing xml file to extract info
        necessary to create a dataset,
        calls dataset create action 
    """
    xml_file = request.files["file"]
    logger.debug("from xml parser blueprint", xml_file)
    logger.info("xml parser blueprint:", xml_file)
    dom_ob = dom.parse(xml_file)
    composite_fields_tags = ["authors", "contact_person", "data_reference_date", "minimum_maximum_extent"]
    date_tags = ["", ""]
    root = dom_ob.firstChild
    fields_ob = {}
    if root.hasChildNodes():
        for field in root.childNodes:
            if field.nodeType != 3 and field.tagName in composite_fields_tags:
                composite_field = handle_composite_field(field)
                fields_ob.update(composite_field)
            
            elif field.nodeType != 3 and field.tagName == "publication_date":
                date_field = handle_date_field(field)
                fields_ob.update(date_field)

            elif field.nodeType != 3: # end of line character is considered an element, skip that
                fields_ob.update({field.tagName:field.childNodes[0].data}) # childNodes[0] is a textNode, data is the actual text
    
    create_action = toolkit.get_action('package_create')
    #scheming_action = toolkit.get_action('scheming_dataset_schema_show')
    fields_ob["type"] = "metadata-form"
    create_action(data_dict = fields_ob)
    #the_schema = scheming_action(data_dict = {"type":"metadata-form"})
    #return json.dumps(the_schema) 
    return "dataset created, check dataset page"

def handle_composite_field(field):
    """
        these fields ["author", "contact_person", 
        "data_reference_date", "minimum_maximum_extent"]
        needs deticated processing, all these composite
        fields have only one level depth.
    """
    #sub_fields_ob = {}
    # ckanext-scheming needs a list of dicts
    sub_fields_holder = []
    tag_name = field.tagName
    for sub_field in field.childNodes:
        if sub_field.nodeType != 3:
            #sub_fields_ob[sub_field.tagName] = sub_field.childNodes[0].data
            if sub_field.tagName in ["data_reference_date_from", "data_reference_date_to"]:
                date_field = handle_date_field(sub_field)
                sub_fields_holder.append(date_field)
            else:        
                sub_fields_holder.append({sub_field.tagName:sub_field.childNodes[0].data})
    #return {tag_name:sub_fields_ob}
    return {tag_name:sub_fields_holder}


def handle_date_field(date_field):
    """
        returns a date from iso- string
        YY-MM-DDTHH:MM:SS
    """
    date_ob = {}
    date_string = date_field.childNodes[0].data
    date_ob["iso_date"] = datetime.fromisoformat(date_string)
    
    return {date_field.tagName:date_ob["iso_date"]}