# FMSPy - Copyright (c) 2009 Andrey Smirnov.
#
# See COPYRIGHT for details.

"""
Tests for L{fmspy.application.room}.
"""

# w/o these imports twisted.trial fails
import decimal, sets

from twisted.trial import unittest

from fmspy.application.room import Room

class ApplicationMock(object):
    """
    Mock for application.
    """

    def __init__(self):
        self.empty_room = None

    def room_empty(self, room):
        self.empty_room = room

class ClientMock(object):
    """
    Mock for room client (generally protocol).
    """

class RoomTestCase(unittest.TestCase):
    """
    Testcase for L{fmspy.application.room.Room}.
    """

    def setUp(self):
        self.a = ApplicationMock()
        self.r = Room(self.a)
        self.c1 = ClientMock()
        self.c2 = ClientMock()

    def test_enter(self):
        self.r.enter(self.c1)
        self.failUnlessRaises(AssertionError, self.r.enter, self.c1)

        self.failUnlessEqual([self.c1], list(self.r))

        self.r.enter(self.c2)
        self.failUnlessEqual(sorted([self.c1, self.c2]), sorted(list(self.r)))

    def test_leave(self):
        self.failUnlessRaises(AssertionError, self.r.leave, self.c1)
        self.r.enter(self.c1)
        self.r.enter(self.c2)

        self.r.leave(self.c1)
        self.failUnlessEqual([self.c2], list(self.r))
        self.failUnlessIdentical(None, self.a.empty_room)

        self.r.leave(self.c2)
        self.failUnlessIdentical(self.r, self.a.empty_room)
