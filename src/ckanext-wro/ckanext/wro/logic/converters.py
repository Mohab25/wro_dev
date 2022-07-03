import json
import logging
from ckan.plugins import toolkit
# def convert_raw_input_to_geojson(input_text:str)->dict:
#     return json.dumps({ "type": "Point", "coordinates": [16, 32]})

logger = logging.getLogger(__name__)

def convert_raw_input_to_geojson(input_text:str)->dict:
    """
        the user should input
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
    #try:
    if input_text == "": # empty input, set default bounding to south africa
        input_text = "-22.1265, 16.4699, -34.8212, 32.8931"  
    logger.debug("======, 'inside convert_raw_input_to_geojson', input_text", input_text)
    
    # the converter is called mutiple times during dataset creation, this if statement 
    # is used to handle an error when the value is missing with the call to this converter
    # after resrouce upload form sumitted.
    if input_text == toolkit.missing:
        default_geojson = {"type": "Polygon", "coordinates": [[[16.4699, -22.1265], [32.8931, -22.1265], [32.8931, -34.8212], [16.4699, -34.8212], [16.4699, -22.1265]]]}
        return json.dumps(default_geojson)
    values = input_text.split(",")
    if len(values)==2: # a point
        geojson = { "type": "Point", "coordinates": [float(values[1]), float(values[0])]}
        return json.dumps(geojson)
    elif len(values)==4:
        """ goejson has the coords as long, lat and exterior ring going coutner clockwise
            while holes are clock wise(right hand role). 
            see the spect https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.1
            see https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.6
        """
        values = [float(i) for i in values]
        c1 = [values[1],values[0]]
        c2 = [values[3],values[0]]
        c3 = [values[3],values[2]]
        c4 = [values[1],values[2]] 
        
        geojson = {"type": "Polygon", "coordinates": [[ c1, c2, c3, c4, c1 ]]}
        return json.dumps(geojson)
    else:
        coords = values[1:]
        coords = ",".join(coords)
        values = values[0] + "," + coords
        values = eval(values)
        try:
            if type(values)== 'dict':
                return values
        except:
            raise toolkit.Invalid("the first bings input should either a point or"\
            " a bounding box, please check your input (see help text below)")
    #except Exception:
    #    raise RuntimeError(Exception)
        # raise toolkit.Invalid("the second bings this tool is tested for inputs that are either "\
        #         "points or bounding box, please check your input (see help text below)"
        #     )
    #geojson = json.dumps(geojson)
    #return geojson


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

