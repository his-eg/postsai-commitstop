# The MIT License (MIT)
# Copyright (c) 2016-2017 HIS e. G.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


from permissions import checkPrivilege

import unittest



class CheckPrivilegeTests(unittest.TestCase):
    """tests for the cache"""


    def test_first_matching_rule_is_accept(self):
        """ensure the first matching rule wins, in case of accept"""

        conf = """
+ .* .* .* .* .* |<| Grant access
- .* .* .* .* .* |<| Deny access
"""
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "user", "", "commitmsg"), (True, "Grant access"), "Grant access")


    def test_first_matching_rule_is_deny(self):
        """ensure the first matching rule wins, in case of deny"""

        conf = """
- .* .* .* .* .* |<| Deny access
+ .* .* .* .* .* |<| Grant access
"""
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "user", "", "commitmsg"), (False, "Deny access"), "Deny access")


    def test_deny_if_no_match(self):
        """ensure access is denied, if no rule matches"""

        conf = """
+ otherrepo .* .* .* .* |<| Grant access
"""
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "user", "", "commitmsg"), (False, "Rejected by default."), "Rejected by default.")


    def test_full_match(self):
        """ensure a rule matches if and only if all subrules match"""

        conf = """
+ repo branch user group 12345 |<| Grant access
"""
        self.assertEqual(checkPrivilege.checkLines(conf, "otherrepo", "branch", "user", "group", "12345"), (False, "Rejected by default."), "Rejected by default.")
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "otherbranch", "user", "group", "12345"), (False, "Rejected by default."), "Rejected by default.")
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "otheruser", "group", "12345"), (False, "Rejected by default."), "Rejected by default.")
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "user", "othergroup", "12345"), (False, "Rejected by default."), "Rejected by default.")
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "user", "group", "other12345"), (False, "Rejected by default."), "Rejected by default.")
        self.assertEqual(checkPrivilege.checkLines(conf, "repo", "branch", "user", "group", "12345"), (True, "Grant access"), "Complete match")



if __name__ == '__main__':
    unittest.main()
