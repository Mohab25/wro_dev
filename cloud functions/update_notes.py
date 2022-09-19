"""
updating notes field, the description
field has been renamed to notes.
"""

import psycopg2

def main():
    """ initiate the connection
    and close it
    """
    conn = psycopg2.connect("dbname=ckan_default user=postgres password=postgres")
    cur = conn.cursor()
    update_notes(cur)
    conn.commit()
    conn.close()

def get_package_ids(cur):
    """
    get the packages ids
    """
    ids = [] 
    q = """ select id from package"""
    cur.execute(q)
    rows = cur.fetchall()
    for row in rows:
        ids.append(row[0])
    return ids

def get_description_data(cur):
    """
    getting the description data
    from desciption field (found
    in package_extra)
    """
    descriptions = []
    package_ids = get_package_ids(cur)
    for id in package_ids:
        q = f""" select value from package_extra where key='dataset_description' and package_id='{id}'"""
        cur.execute(q)
        description = cur.fetchone()
        if description is None:
            description = ""
        else:
            description = description[0].replace("'", '"')
        descriptions.append({"package_id":id,"description":description})
    print(descriptions)
    return descriptions

def update_notes(cur):
    """
    update the notes field
    """
    descriptions = get_description_data(cur)
    for desc_ob in descriptions:
        id = desc_ob.get("package_id")
        desc = desc_ob.get("description")
        q = f""" update package set notes='{desc}' where id='{id}'"""
        cur.execute(q)

main()