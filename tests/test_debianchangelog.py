# Copyright (C) 2015 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,USA.

import os
import subprocess
import unittest


from ddt import ddt, file_data

from test_base import SetVersionBaseTest


def has_dch_executable():
    """the devscripts package is needed to be able to use 'dch'"""
    with open(os.devnull, "wb") as devnull:
        try:
            subprocess.check_call("dch --version",
                                  stdout=devnull, stderr=devnull, shell=True)
        except subprocess.CalledProcessError:
            return False
        else:
            return True


@ddt
@unittest.skipUnless(has_dch_executable(), "'dch' executable not available")
class SetVersionDebianChangelog(SetVersionBaseTest):
    """Test set_version service for debian/changelog files"""

    def _write_debian_changelog(self, version):
        subprocess.check_call("dch --create --empty -v "
                              "%s --package foobar -c debian.changelog" %
                              version, shell=True)
        return os.path.join(self._tmpdir, "debian.changelog")

    @file_data("data_test_from_commandline.json")
    def test_from_commandline(self, data):
        spec_tags, new_version = data
        old_version = "8.8.8"
        changelog_path = self._write_debian_changelog(old_version)
        self._run_set_version(params=['--version', new_version])
        self._check_file_assert_contains(changelog_path, new_version)
        self._check_file_assert_not_contains(changelog_path, old_version)