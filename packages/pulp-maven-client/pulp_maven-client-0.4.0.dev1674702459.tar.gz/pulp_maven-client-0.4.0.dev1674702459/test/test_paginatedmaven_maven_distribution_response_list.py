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

import pulpcore.client.pulp_maven
from pulpcore.client.pulp_maven.models.paginatedmaven_maven_distribution_response_list import PaginatedmavenMavenDistributionResponseList  # noqa: E501
from pulpcore.client.pulp_maven.rest import ApiException

class TestPaginatedmavenMavenDistributionResponseList(unittest.TestCase):
    """PaginatedmavenMavenDistributionResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedmavenMavenDistributionResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_maven.models.paginatedmaven_maven_distribution_response_list.PaginatedmavenMavenDistributionResponseList()  # noqa: E501
        if include_optional :
            return PaginatedmavenMavenDistributionResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?offset=400&limit=100', 
                previous = 'http://api.example.org/accounts/?offset=200&limit=100', 
                results = [
                    pulpcore.client.pulp_maven.models.maven/maven_distribution_response.maven.MavenDistributionResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        base_path = '0', 
                        base_url = '0', 
                        content_guard = '0', 
                        pulp_labels = {
                            'key' : '0'
                            }, 
                        name = '0', 
                        repository = '0', 
                        remote = '0', )
                    ]
            )
        else :
            return PaginatedmavenMavenDistributionResponseList(
        )

    def testPaginatedmavenMavenDistributionResponseList(self):
        """Test PaginatedmavenMavenDistributionResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
