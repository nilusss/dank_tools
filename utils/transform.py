"""Utilities related to transform
"""

import maya.cmds as mc


def zero_ctrl(ctrls=[], t=True, r=True, s=False):
    """Given a number of nurbs controls to zero out

    Arguments:
        ctrls {string,list} -- control(s) to zero out

    Keyword Arguments:
        t {bool} -- translate (default: {True})
        r {bool} -- rotate (default: {True})
        s {bool} -- scale (default: {False})
    """

    # Axises to zero out
    axis = ['x', 'y', 'z']

    # Go through every control and zero every axis
    for c in ctrls:
        for a in axis:
            if t:
                # Zero translate if it isn't locked
                try:
                    mc.setAttr(c + '.t{}'.format(a), 0)
                except:
                    pass

            if r:
                # Zero rotate if it isn't locked
                try:
                    mc.setAttr(c + '.r{}'.format(a), 0)
                except:
                    pass

            if s:
                # Zero scale if it isn't locked
                try:
                    mc.setAttr(c + '.t{}'.format(a), 1)
                except:
                    pass