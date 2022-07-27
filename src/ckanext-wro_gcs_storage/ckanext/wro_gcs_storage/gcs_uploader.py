import os.path
import pathlib

import ckan
from ckan.common import config # change here
import ckan.plugins.toolkit as toolkit # and here
from ckan import model
from ckan.lib import munge
import ckan.plugins as p

from .gcs_functions import upload_blob

from werkzeug.datastructures import FileStorage as FlaskFileStorage
from tempfile import SpooledTemporaryFile
import cgi

_get_or_bust = ckan.logic.get_or_bust

ALLOWED_UPLOAD_TYPES = (cgi.FieldStorage, FlaskFileStorage)


def _get_underlying_file(wrapper):
    if isinstance(wrapper, FlaskFileStorage):
        return wrapper.stream
    return wrapper.file

class ResourceCloudStorage():
    def __init__(self, resource):
        """
        Support for uploading resources to any storage provider
        implemented by the apache-libcloud library.
        :param resource: The resource dict.
        """

        self.filename = None
        self.old_filename = None
        self.file = None
        self.resource = resource
        upload_field_storage = resource.pop('upload', None)
        self._clear = resource.pop('clear_upload', None)
        try: 
            self.is_resource_link = self.resource['is_link']
        except KeyError:
            self.is_resource_link = False
        # Check to see if a file has been provided
        if isinstance(upload_field_storage, (ALLOWED_UPLOAD_TYPES)):
            self.filename = munge.munge_filename(upload_field_storage.filename)
            self.file_upload = _get_underlying_file(upload_field_storage)
            resource['url_type'] = 'upload'
        elif self._clear and resource.get('id'):
            # Apparently, this is a created-but-not-commited resource whose
            # file upload has been canceled. We're copying the behaviour of
            # ckaenxt-s3filestore here.
            old_resource = model.Session.query(model.Resource).get(resource['id'])
            self.old_filename = old_resource.url
            resource['url_type'] = ''

    def path_from_filename(self, rid, filename):
        """
        Returns a bucket path for the given resource_id and filename.
        :param rid: The resource ID.
        :param filename: The unmunged resource filename.
        """
        # mohab, you can get "wro theme" here, agriculture, water, ..etc.
        # and construct dynamic urls inisde the container
        
        # get the wro_theme
        #pack = toolkit.get_action('package_show')(data_dict={'id':self.resource['package_id']})
        res = toolkit.get_action('resource_show')(data_dict={'id':rid})
        # we need to generate unique names inside the container
        name = pathlib.Path(filename).stem
        ext = pathlib.Path(filename).suffix
        file_name = name+'_id_'+rid+ext
        # the actual return
        return os.path.join(
            res['cloud_path'],
            self.resource['package_id'],
            file_name
        )

    def upload(self, id, max_size=10):
        """
        Complete the file upload, or clear an existing upload.
        :param id: The resource_id.
        :param max_size: Ignored.
        """
        if self.is_resource_link is False:
            if self.filename:
                if isinstance(self.file_upload, SpooledTemporaryFile):
                    self.file_upload.next = self.file_upload._file  # changed here
                    upload_path = self.path_from_filename(id,self.filename)
                    self.resource['url'] = f'https://storage.cloud.google.com/{upload_path}'
                    bucket_name = config.get('container_name')
                    upload_blob(bucket_name, self.file_upload, upload_path)

        # this is when the user change the file to a url via "remove" button
        # elif self._clear and self.old_filename:  # and not self.leave_files
        #     # This is only set when a previously-uploaded file is replace
        #     # by a link. We want to delete the previously-uploaded file.
        #     try:
        #        delete_blob(self.old_filename)
        #     except:
        #         # It's possible for the object to have already been deleted, or
        #         # for it to not yet exist in a committed state due to an
        #         # outstanding lease.
        #         return

    def get_path(self,id):
        return ''



    @property
    def package(self):
        return model.Package.get(self.resource['package_id'])