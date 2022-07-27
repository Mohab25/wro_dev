import xml.dom.minidom as dom
import logging
import json

logger = logging.getLogger(__name__)

def parse_xml_dataset_upload(xml_file):
    """
        parsing xml file to extract info
        necessary to create a dataset,
        calls dataset create action 
    """
    logger.debug("from xml parser blueprint", xml_file)
    logger.info("xml parser blueprint:", xml_file)
    dom_ob = dom.parse(xml_file)
    root = dom_ob.firstChild
    composite_fields_tags = ["authors", "contact_person", "data_reference_date", "minimum_maximum_extent"]
    metadata_fields_keys = [] 
    if root.hasChildNodes():
        fields_ob = {}
        for field in root.childNodes:         
            if field.nodeType != 3 and field.tagName in composite_fields_tags:
                composite_field = handle_composite_field(field, metadata_fields_keys)
                fields_ob.update(composite_field)
            elif field.nodeType != 3: # end of line character is considered an element, skip that
                metadata_fields_keys.append(field.tagName)
                fields_ob.update({field.tagName:field.childNodes[0].data}) # childNodes[0] is a textNode, data is the actual text
        print(json.dumps(fields_ob)) 

def handle_composite_field(field, meta_keys = None):
    """
        these fields ["author", "contact_person", 
        "data_reference_date", "minimum_maximum_extent"]
        needs deticated processing, all these composite
        fields have only one level depth.
    """
    sub_fields_ob = {}
    tag_name = field.tagName
    for sub_field in field.childNodes:
        if sub_field.nodeType != 3:
            sub_fields_ob[sub_field.tagName] = sub_field.childNodes[0].data
            meta_keys.append(tag_name)
    return {tag_name:sub_fields_ob}

parse_xml_dataset_upload('/home/mohab/Main/development/WRO/wro_dataset.xml')