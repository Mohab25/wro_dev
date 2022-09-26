import json
import logging
import typing
from shapely import geometry
from ckan.plugins import toolkit
import json

logger = logging.getLogger(__name__)

def get_default_spatial_search_extent(
    padding_degrees: typing.Optional[float] = None,
) -> typing.Dict:
    """
    Return GeoJSON polygon with bbox to use for default view of spatial search map widget.
    """
    configured_extent = toolkit.config.get(
        "ckan.dalrrd_emc_dcpr.default_spatial_search_extent"
    )
    if padding_degrees and configured_extent:
        parsed_extent = json.loads(configured_extent)
        result = _pad_geospatial_extent(parsed_extent, padding_degrees)
    else:
        result = configured_extent
    return result


def get_default_bounding_box() -> typing.Optional[typing.List[float]]:
    """Return the default bounding box in the form upper left, lower right
    This function calculates the default bounding box from the
    `ckan.dalrrd_emc_dcpr.default_spatial_search_extent` configuration value. Note that
    this configuration value is expected to be in GeoJSON format and in GeoJSON,
    coordinate pairs take the form `lon, lat`.
    This function outputs a list with upper left latitude, upper left latitude, lower
    right latitude, lower right longitude.
    """

    configured_extent = toolkit.config.get(
        "default_spatial_search_extent"
    )
    #parsed_extent = json.loads(configured_extent)
    return convert_geojson_to_bbox(configured_extent)
    
def convert_geojson_to_bbox(
    geojson: typing.Dict,
) -> typing.Optional[typing.List[float]]:
    try:
        geojson = json.loads(geojson)
        coords = geojson["coordinates"][0]
    except TypeError as e:
        result = None
    else:
        min_lon = min(c[0] for c in coords)
        max_lon = max(c[0] for c in coords)
        min_lat = min(c[1] for c in coords)
        max_lat = max(c[1] for c in coords)
        result = [max_lat, min_lon, min_lat, max_lon]
    return result

def _pad_geospatial_extent(extent: typing.Dict, padding: float) -> typing.Dict:
    geom = geometry.shape(extent)
    padded = geom.buffer(padding, join_style=geometry.JOIN_STYLE.mitre)
    oriented_padded = geometry.polygon.orient(padded)
    return geometry.mapping(oriented_padded)


def get_bigquery_table_name(resource):
    """
    when a bigquery table is given,
    there is no name in the packge
    resources list, we need to 
    retrive the table name and provide
    it in the package resources_info
    """
    if resource["is_bigquery_table"] == True:
        resource["name"] = resource["resource_name"]
        return resource["resource_name"] 
    return ""
    

def get_package_name(package_id:str)-> str: 
    """
    get the package name from the id,
    it's useful while retrieving packages
    from resources.
    """
    package_show_action = toolkit.get_action("package_show")
    package_name = package_show_action(data_dict={"id":package_id})["title"]
    return package_name
