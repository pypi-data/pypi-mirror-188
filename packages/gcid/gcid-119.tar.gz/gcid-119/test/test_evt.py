# This file is placed in the Public Domain.


"event"


import unittest


from gcid import Event


class TestEvent(unittest.TestCase):

    def testconstructor(self):
        evt = Event()
        self.assertEqual(type(evt), Event)
