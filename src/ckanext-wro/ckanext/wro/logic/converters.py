import json
from ckan.plugins import toolkit
# def convert_raw_input_to_geojson(input_text:str)->dict:
#     return json.dumps({ "type": "Point", "coordinates": [16, 32]})
def convert_raw_input_to_geojson(input_text:str)->dict:
    """
        as with the form schema, the user should input
        a text of comma-seprated values, we need to convert
        that to geojson so ckanext-spatial could handle it.

        args
        ----
        input_text - str: a comma seperated values of either a point
        or bounding box, input from ckanext-scheming form

        returns
        -------
        dict: the goejson constructed from the input text values. 
    """
    geojson = None
    try:
        values = input_text.split(",")
        
        if len(values)==2: # a point
            geojson = { "type": "Point", "coordinates": [float(values[0]), float(values[1])]}
        elif len(values)==4:
            geojson = { "type": "Polygon", "coordinates": [[values[0], values[1]]]} ## adress this
        else:
            raise toolkit.Invalid("input should either a point or"\
             " a bounding box, please check your input (see help text below)")
    except:
        raise toolkit.Inavlid("this tool is tested for inputs that are either"\
                "points or bounding box, please check your input (see help text below)"
            )
    geojson = json.dumps(geojson)
    return geojson


















# # import logging

# # from ckan.plugins import toolkit

# # logger = logging.getLogger(__name__)


# # def emc_bbox_converter(value: str) -> str:
# #     error_msg = toolkit._(
# #         "Invalid bounding box. Please provide a comma-separated list of values "
# #         "with upper left lat, upper left lon, lower right lat, lower right lon."
# #     )
# #     logger.debug(f"inside emc_bbox_converter {value=}")
# #     try:  # is it already a geojson?
# #         parsed_value = json.loads(value)
# #         coordinates = parsed_value["coordinates"][0]
# #         upper_lat = coordinates[2][1]
# #         left_lon = coordinates[0][0]
# #         lower_lat = coordinates[0][1]
# #         right_lon = coordinates[1][0]
# #     except json.JSONDecodeError:  # nope, it is a bbox
# #         try:
# #             bbox_coords = [float(i) for i in value.split(",")]
# #         except ValueError:
# #             logger.exception(msg="something failed")
# #             raise toolkit.Invalid(error_msg)
# #         else:
# #             upper_lat = bbox_coords[0]
# #             left_lon = bbox_coords[1]
# #             lower_lat = bbox_coords[2]
# #             right_lon = bbox_coords[3]
# #     except IndexError:
# #         logger.exception(msg="something failed")
# #         raise toolkit.Invalid(error_msg)
# #     parsed = {
# #         "type": "Polygon",
# #         "coordinates": [
# #             [
# #                 [left_lon, lower_lat],
# #                 [right_lon, lower_lat],
# #                 [right_lon, upper_lat],
# #                 [left_lon, upper_lat],
# #                 [left_lon, lower_lat],
# #             ]
# #         ],
# #     }
# #     logger.debug(f"{parsed=}")
# #     return json.dumps(parsed)