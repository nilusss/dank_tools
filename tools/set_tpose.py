"""Tool for setting the rig in a perfect T Pose stance
"""

import maya.cmds as mc
import dank_tools.utils.transform as trns
import dank_tools.tools.ikfk_match as match

reload(trns)


def get_y_from_origin(ctrl):
    """[summary]
    """
    ty = False
    if mc.objExists(ctrl):
        tmp_grp = mc.group(em=True)
        mc.delete(mc.pointConstraint(ctrl, tmp_grp))
        ty = mc.getAttr(tmp_grp + '.ty')
        mc.delete(tmp_grp)

        return ty
    else:
        mc.error("No object matches: \"{}\"".format(ctrl))


def tpose_set(ctrl, rx, ry, rz):
    """[summary]
    """
    if mc.objExists(ctrl):
        # Create empty group and rotate it, so the control will point straight
        tmp_grp = mc.group(em=True)

        mc.setAttr(tmp_grp + '.rx', rx)
        mc.setAttr(tmp_grp + '.ry', ry)
        mc.setAttr(tmp_grp + '.rz', rz)

        # Rotate control to match the temp group
        mc.orientConstraint(tmp_grp, ctrl)
        mc.delete(tmp_grp)


def tpose(rokoko=False, charNS=''):
    """[summary]
    """
    if charNS: charNS+=':'
    # Zero all controls
    ctrls = mc.ls("*_ctrl")
    trns.zero_ctrl(ctrls)

    ty_org = get_y_from_origin(charNS+'l_legEnd_FK_ctrl')

    tpose_set(charNS+"l_legUpper_FK_ctrl", 90, 0, -90)
    tpose_set(charNS+"l_legLower_FK_ctrl", 90, 0, -90)
    tpose_set(charNS+"l_legEnd_FK_ctrl", 90, -30, -90)
    tpose_set(charNS+"l_legFootBallFK_ctrl", 0, 0, 0)

    tpose_set(charNS+"r_legUpper_FK_ctrl", -90, 0, 90)
    tpose_set(charNS+"r_legLower_FK_ctrl", -90, 0, 90)
    tpose_set(charNS+"r_legEnd_FK_ctrl", -90, 30, 90)
    tpose_set(charNS+"r_legFootBallFK_ctrl", 0, 0, 0)

    if rokoko:
        tpose_set(charNS+"l_armScapula_ctrl", -105, 0, 0)
        mc.setAttr(charNS+'l_armScapula_ctrl.rx', 0)
        mc.setAttr(charNS+'l_armScapula_ctrl.ry', 0)
        mc.setAttr(charNS+'l_armScapula_ctrl.rz', -15)
        tpose_set(charNS+"l_armUpper_FK_ctrl", -90, 0, 0)
        tpose_set(charNS+"l_armLower_FK_ctrl", -90, 0, 0)

        tpose_set(charNS+"r_armScapula_ctrl", 105, 0, 0)
        mc.setAttr(charNS+'r_armScapula_ctrl.rx', 0)
        mc.setAttr(charNS+'r_armScapula_ctrl.ry', 0)
        mc.setAttr(charNS+'r_armScapula_ctrl.rz', -15)
        tpose_set(charNS+"r_armUpper_FK_ctrl", 90, 0, 0)
        tpose_set(charNS+"r_armLower_FK_ctrl", 90, 0, 0)
    else:
        tpose_set(charNS+"l_armUpper_FK_ctrl", -90, 0, 0)
        tpose_set(charNS+"l_armLower_FK_ctrl", -90, 0, 0)

        tpose_set(charNS+"r_armUpper_FK_ctrl", 90, 0, 0)
        tpose_set(charNS+"r_armLower_FK_ctrl", 90, 0, 0)

    ty_new = get_y_from_origin(charNS+'l_legEnd_FK_ctrl')
    offset = (ty_org - ty_new)

    mc.setAttr(charNS+'COM_ctrl.ty', offset)
    mc.setAttr(charNS+"l_legIKFKBlend_ctrl.FKIKBlend", 0)
    mc.setAttr(charNS+"r_legIKFKBlend_ctrl.FKIKBlend", 0)
    mc.setAttr(charNS+"l_armIKFKBlend_ctrl.FKIKBlend", 0)
    mc.setAttr(charNS+"r_armIKFKBlend_ctrl.FKIKBlend", 0)

    match.ikFkSwitch_sameOrient('l', 'arm', charNS=charNS)
    match.ikFkSwitch_sameOrient('r', 'arm', charNS=charNS)
    match.ikFkSwitch_sameOrient('l', 'leg', charNS=charNS)
    match.ikFkSwitch_sameOrient('r', 'leg', charNS=charNS)

    trns.zero_ctrl([charNS+'l_legIK_ctrl'], t=False, r=True, s=False)
    trns.zero_ctrl([charNS+'r_legIK_ctrl'], t=False, r=True, s=False)

    mc.setAttr(charNS+"l_armPoleVec_ctrl.tz", 0)
    mc.setAttr(charNS+"r_armPoleVec_ctrl.tz", 0)
    mc.setAttr(charNS+"l_legPoleVec_ctrl.tz", 0)
    mc.setAttr(charNS+"r_legPoleVec_ctrl.tz", 0)

    tpose_set(charNS+"l_legIK_ctrl", 0, 0, 0)
    tpose_set(charNS+"r_legIK_ctrl", 0, 0, 0)

    try:
        s2 = mc.xform(charNS+"l_armLower_result_jnt", sp=True , q=True , ws=True)
    except ValueError:
        s2 = mc.xform(charNS+"LeftForeArm", sp=True , q=True , ws=True)
    mc.move(s2[0], s2[1], s2[2], charNS+"l_armPoleVecOffset_grp" + '.scalePivot', charNS+"l_armPoleVecOffset_grp" + '.rotatePivot', absolute=True)

    try:
        s2 = mc.xform(charNS+"r_armLower_result_jnt", sp=True , q=True , ws=True)
    except ValueError:
        s2 = mc.xform(charNS+"RightForeArm", sp=True , q=True , ws=True)
    mc.move(s2[0], s2[1], s2[2], charNS+"r_armPoleVecOffset_grp" + '.scalePivot', charNS+"r_armPoleVecOffset_grp" + '.rotatePivot', absolute=True)

    try:
        s2 = mc.xform(charNS+"l_legLower_result_jnt", sp=True , q=True , ws=True)
    except ValueError:
        s2 = mc.xform(charNS+"LeftShin", sp=True , q=True , ws=True)
    mc.move(s2[0], s2[1], s2[2], charNS+"l_legPoleVecOffset_grp" + '.scalePivot', charNS+"l_legPoleVecOffset_grp" + '.rotatePivot', absolute=True)

    try:
        s2 = mc.xform(charNS+"r_legLower_result_jnt", sp=True , q=True , ws=True)
    except ValueError:
        s2 = mc.xform(charNS+"RightShin", sp=True , q=True , ws=True)
    mc.move(s2[0], s2[1], s2[2], charNS+"r_legPoleVecOffset_grp" + '.scalePivot', charNS+"r_legPoleVecOffset_grp" + '.rotatePivot', absolute=True)
