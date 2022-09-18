from google.cloud import bigquery
import json
from ckan.plugins import toolkit
from pyproj import Proj, transform


def make_query(bigquery_project:str = "wrc-wro",bigquery_dataset:str = "" , bigquery_table:str = "", offset:int=0, limit:int=0) -> list:
    """
    initalize the connection and
    pass the query to the client

    returns 
    -------
    data: list
        a list of json objects
        each holds column name
        and data. 

    todo
    ---
    support picking specific columns
    (should be introduced as kwargs)
    """
    credentials = '/home/mohab/Main/development/googleAuthKeys/wro project/bigquery admin/wrc-wro-7a61a964dfbd.json'
    client = bigquery.Client.from_service_account_json(credentials)
    data = []
    query = f"""
        SELECT * FROM `{bigquery_project}.{bigquery_dataset}.{bigquery_table}`
    """
    
    query_job = client.query(query)

    for row in query_job:
        data.append((dict(row)))
    return data


def make_spatial_query(bigquery_project:str = "wrc-wro", bigquery_dataset:str = "" , bigquery_table:str = "", offset:int=0, limit:int=0) -> dict:
    """
    making a spatial query using bigquery
    ST_ASGEOJSON, returns a geojson holding
    a spatial table
    """
    credentials = '/home/mohab/Main/development/googleAuthKeys/wro project/bigquery admin/wrc-wro-7a61a964dfbd.json'
    client = bigquery.Client.from_service_account_json(credentials)
    geojson_ob_list = []
    query = f"""
        select ST_ASGEOJSON(ST_GEOGPOINT(LAT, LON)) as feature,
        *
        from `{bigquery_project}.{bigquery_dataset}.{bigquery_table}`
    """
    query_job = client.query(query)

    for row in query_job:
        row_dict = dict(row)
        feat = json.loads(row_dict["feature"]) # this is encoded twice
        props = {k: v for k, v in row_dict.items() if k not in ["feature"]}
        feat.update({"properties":props})
        geojson_ob_list.append(feat)



    def transform(x1,y1):
        """
        properties need to transform from
        epsg:4326 wgs84 to epsg:3857 web mercator
        """

        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:3857')
        x2,y2 = transform(inProj,outProj,x1,y1)
        return f'LAT:{x2},LON:{y2}'



    return json.dumps(geojson_ob_list)
