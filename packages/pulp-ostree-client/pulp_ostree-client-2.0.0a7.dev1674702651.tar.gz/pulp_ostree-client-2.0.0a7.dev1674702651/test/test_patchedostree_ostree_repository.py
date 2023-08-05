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

import pulpcore.client.pulp_ostree
from pulpcore.client.pulp_ostree.models.patchedostree_ostree_repository import PatchedostreeOstreeRepository  # noqa: E501
from pulpcore.client.pulp_ostree.rest import ApiException

class TestPatchedostreeOstreeRepository(unittest.TestCase):
    """PatchedostreeOstreeRepository unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PatchedostreeOstreeRepository
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ostree.models.patchedostree_ostree_repository.PatchedostreeOstreeRepository()  # noqa: E501
        if include_optional :
            return PatchedostreeOstreeRepository(
                pulp_labels = {
                    'key' : '0'
                    }, 
                name = '0', 
                description = '0', 
                retain_repo_versions = 1, 
                remote = '0'
            )
        else :
            return PatchedostreeOstreeRepository(
        )

    def testPatchedostreeOstreeRepository(self):
        """Test PatchedostreeOstreeRepository"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
