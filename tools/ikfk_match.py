"""Utility to characterize a rig to be used with HumanIK
"""

import maya.mel as mel
import maya.cmds as mc

import os


def ikFkSwitch_sameOrient(side, limb, charNS=''):
    '''This command should be used in the cases where all the controls and joints, including the
    ik control are oriented in the exact same way.'''
    if mc.getAttr(charNS+"{}_{}IKFKBlend_ctrl.FKIKBlend".format(side, limb)):
        # From IK to FK
        mc.delete(mc.orientConstraint(charNS+"{}_{}Upper_IK_jnt".format(side, limb),
                                      charNS+"{}_{}Upper_FK_ctrl".format(side, limb)))
        mc.delete(mc.orientConstraint(charNS+"{}_{}Lower_IK_jnt".format(side, limb),
                                      charNS+"{}_{}Lower_FK_ctrl".format(side, limb)))
        mc.delete(mc.orientConstraint(charNS+"{}_{}End_IK_jnt".format(side, limb),
                                      charNS+"{}_{}End_FK_ctrl".format(side, limb)))

        mc.setAttr(charNS+"{}_{}IKFKBlend_ctrl.FKIKBlend".format(side, limb), 0)
    else:
        # From FK to IK
        mc.delete(mc.parentConstraint(charNS+"{}_{}End_FK_ctrl".format(side, limb),
                                      charNS+"{}_{}IK_ctrl".format(side, limb)))

        arm01Vec = [mc.xform(charNS+"{}_{}Lower_FK_jnt".format(side, limb), t=1, ws=1, q=1)[i] - mc.xform(charNS+"{}_{}Upper_FK_jnt".format(side, limb), t=1, ws=1, q=1)[i] for i in range(3)]
        arm02Vec = [mc.xform(charNS+"{}_{}Lower_FK_jnt".format(side, limb), t=1, ws=1, q=1)[i] - mc.xform(charNS+"{}_{}End_FK_jnt".format(side, limb), t=1, ws=1, q=1)[i] for i in range(3)]

        mc.xform(charNS+"{}_{}PoleVec_ctrl".format(side, limb), t=[mc.xform(charNS+"{}_{}Lower_FK_jnt".format(side, limb), t=1, q=1, ws=1)[i] + arm01Vec[i] * .75 + arm02Vec[i] * .75 for i in range(3)], ws=1)

        mc.setAttr(charNS+"{}_{}IKFKBlend_ctrl.FKIKBlend".format(side, limb), 1)
