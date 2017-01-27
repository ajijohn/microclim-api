from microclim import MicroclimApiClient

import sys
import unittest

global KEY
global IP


class IsOKTest(unittest.TestCase):

    def test_ok_check(self):
        microclim_client = MicroclimApiClient(KEY,SECRET,IP)
        self.assertEqual(microclim_client.hello(),"ok")



if __name__ == '__main__':
    print("Please enter Microclim api key")
    KEY = sys.stdin.readline().strip()
    print(KEY)
    SECRET = sys.stdin.readline().strip()
    print(SECRET)
    print("Please enter Microclim service IP")
    IP = sys.stdin.readline().strip()
    print(IP)
    unittest.main()
