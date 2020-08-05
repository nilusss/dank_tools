#       correct_bake
#       Version 0.0.1
#       Copyright (C)2020 Nilas Niebuhr
#       Email: niebuhrgfx@gmail.com
#       Last Modified: 19/05/2020
#
#
# correct_bake bakes both fk and ik arms for mocap data
#
# For detailed instructions read the "readme.txt" file
#
import os
import time

import maya.cmds as mc
import maya.mel as mel


def correct_bake(asset_name="", ns=True):
    ns_use = ''
    filepath = mc.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    if not asset_name:
        asset_name = filename.split("_")[0]
    if ns:
        namespaces = mc.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        for n in namespaces:
            if asset_name in n:
                if ":" not in n:
                    ns_use = n + ':'
    else:
        ns_use = ''

    # Change FKIK Blend to IK
    mc.setAttr(ns_use+'l_armIKFKBlend_ctrl.FKIKBlend', 0.5)
    mc.setAttr(ns_use+'r_armIKFKBlend_ctrl.FKIKBlend', 0.5)

    # Set constraint to make IK follow FK - for matching when baking
    # Left side
    l_offset_paconstraint = mc.parentConstraint(ns_use+'l_armEnd_FK_jnt', ns_use+'l_armIKOffset_grp', mo=True)
    l_poleoffset_oconstraint = mc.orientConstraint(ns_use+'l_armLower_FK_jnt', ns_use+'l_armPoleVecOffset_grp', mo=True)
    l_polectrl_pconstraint = mc.pointConstraint(ns_use+'l_armLower_FK_jnt', ns_use+'l_armPoleVec_ctrl', mo=False, o=[0, 0, -3])

    # Right side
    r_offset_paconstraint = mc.parentConstraint(ns_use+'r_armEnd_FK_jnt', ns_use+'r_armIKOffset_grp', mo=True)
    r_poleoffset_oconstraint = mc.orientConstraint(ns_use+'r_armLower_FK_jnt', ns_use+'r_armPoleVecOffset_grp', mo=True)
    r_polectrl_pconstraint = mc.pointConstraint(ns_use+'r_armLower_FK_jnt', ns_use+'r_armPoleVec_ctrl', mo=False, o=[0, 0, -3])

    mel.eval('$gCurrentCharacter = "{}_HIK";'.format(asset_name))
    mel.eval('hikToggleLockDefinition();')

    # Change HumanIK source to the mocap character and main character
    mel.eval('mayaHIKsetCharacterInput( "{}_HIK", "mocap" ) ;'.format(asset_name))

    #mel.eval('hikBakeToControlRig 1;')
    ik_ctrls = [ns_use+'r_armPoleVec_ctrl', ns_use+'l_armPoleVec_ctrl', ns_use+'r_armIK_ctrl', ns_use+'l_armIK_ctrl', ns_use+'r_armIKOffset_grp', ns_use+'l_armIKOffset_grp', ns_use+'r_armPoleVecOffset_grp', ns_use+'l_armPoleVecOffset_grp']
    ctrls = mc.ls(ns_use+"*_ctrl")
    mc.select(ctrls)
    mc.select(ik_ctrls, deselect=True)

    start = mc.playbackOptions(q=True, min=True)
    end = mc.playbackOptions(q=True, max=True)

    mc.bakeResults(simulation=True, t=(start, end), sb=1, at=["rx", "ry", "rz", "tx", "ty", "tz"], dic=True)

    mc.select(ik_ctrls)
    mc.bakeResults(simulation=True, t=(start, end), sb=1, at=["rx", "ry", "rz", "tx", "ty", "tz"], dic=True)

    time.sleep(1)

    mc.setAttr(ns_use+'l_armIKFKBlend_ctrl.FKIKBlend', 1)
    mc.setAttr(ns_use+'r_armIKFKBlend_ctrl.FKIKBlend', 1)

    mc.delete(l_offset_paconstraint)
    mc.delete(l_poleoffset_oconstraint)
    mc.delete(l_polectrl_pconstraint)
    mc.delete(r_offset_paconstraint)
    mc.delete(r_poleoffset_oconstraint)
    mc.delete(r_polectrl_pconstraint)
