# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.paginatedrpm_rpm_repository_response_list import PaginatedrpmRpmRepositoryResponseList  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestPaginatedrpmRpmRepositoryResponseList(unittest.TestCase):
    """PaginatedrpmRpmRepositoryResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedrpmRpmRepositoryResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.paginatedrpm_rpm_repository_response_list.PaginatedrpmRpmRepositoryResponseList()  # noqa: E501
        if include_optional :
            return PaginatedrpmRpmRepositoryResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?offset=400&limit=100', 
                previous = 'http://api.example.org/accounts/?offset=200&limit=100', 
                results = [
                    pulpcore.client.pulp_rpm.models.rpm/rpm_repository_response.rpm.RpmRepositoryResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        versions_href = '0', 
                        pulp_labels = {
                            'key' : '0'
                            }, 
                        latest_version_href = '0', 
                        name = '0', 
                        description = '0', 
                        retain_repo_versions = 1, 
                        remote = '0', 
                        autopublish = True, 
                        metadata_signing_service = '0', 
                        retain_package_versions = 0, 
                        metadata_checksum_type = null, 
                        package_checksum_type = null, 
                        gpgcheck = 0, 
                        repo_gpgcheck = 0, 
                        sqlite_metadata = True, )
                    ]
            )
        else :
            return PaginatedrpmRpmRepositoryResponseList(
        )

    def testPaginatedrpmRpmRepositoryResponseList(self):
        """Test PaginatedrpmRpmRepositoryResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
