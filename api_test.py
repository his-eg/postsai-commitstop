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
