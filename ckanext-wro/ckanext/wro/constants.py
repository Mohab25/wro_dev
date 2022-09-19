WRO_METADATA_FIELDS = [
    'email', 
    'title', 
    'name', 
    'authors-0-author_name',
    'authors-0-author_surname',
    'authors-0-author_email',
    'authors-0-author_organization',
    'authors-0-author_department',
    'authors-0-contact_same_as_author',
    'contact_person-0-contact_name',
    'contact_person-0-contact_email', 
    'contact_person-0-contact_orgnization', 
    'contact_person-0-contact_department', 
    'notes',
    'owner_org', 
    'citation-0-citation_title', 
    'citation-0-citation_date', 
    'citation-0-citation_identifier', 
    'did_author_or_contact_organization_collect_the_data', 
    'data_collection_organization', 
    'dataset_language', 
    'publisher', 
    'publication_date', 
    'wrc_project_number', 
    'license', 
    'dataset_license_url', 
    'keywords', 
    'spatial', 
    'wro_theme', 
    'data_structure_category', 
    'uploader_estimation_of_extent_of_processing', 
    'data_classification', 
    'data_reference_date-0-data_reference_date_from', 
    'data_reference_date-0-data_reference_date_to', 
    'alternative_identifier', 
    'vertical_extent_datum', 
    'minimum_maximum_extent-0-minimum_vertical_extent', 
    'minimum_maximum_extent-0-maximum_vertical_extent',
    'tags-0-tag_name',
    'tags-0-tag_type',
    'agreement'
    ]

WRO_METADATA_REQUIRED_FIELDS = [
    'email', 
    'title', 
    'name', 
    'authors-0-author_name',
    'contact_person-0-contact_name',
    'contact_person-0-contact_email', 
    'notes',
    'owner_org', 
    'data_collection_organization', 
    'publisher', 
    'publication_date', 
    'license', 
    'keywords', 
    'spatial', 
    'wro_theme', 
    'data_structure_category', 
    'uploader_estimation_of_extent_of_processing', 
    'data_classification', 
    'agreement'
]

PACKAGE_NON_EXTRAS_FIELDS = [
    'title',
    'name',
    'private',
    'author',
    'author_email',
    'maintainer',
    'maintainer_email',
    'license_id',
    'notes',
    'url',
    'version',
    'state',
    'type',
    'extras'
]


#  id                | text                        |           | not null | 
#  name              | character varying(100)      |           | not null | 
#  title             | text                        |           |          | 
#  version           | character varying(100)      |           |          | 
#  url               | text                        |           |          | 
#  notes             | text                        |           |          | 
#  author            | text                        |           |          | 
#  author_email      | text                        |           |          | 
#  maintainer        | text                        |           |          | 
#  maintainer_email  | text                        |           |          | 
#  state             | text                        |           |          | 
#  license_id        | text                        |           |          | 
#  type              | text                        |           |          | 
#  owner_org         | text                        |           |          | 
#  private           | boolean                     |           |          | false
#  metadata_modified | timestamp without time zone |           |          | 
#  creator_user_id   | text                        |           |          | 
#  metadata_created  | timestamp without time zone |           |          | 
