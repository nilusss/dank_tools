"""Utility to characterize a rig to be used with HumanIK
"""

import maya.mel as mel
import maya.cmds as mc

import os


def init():
    '''
    Load required commands and plugins
    '''
    # Get Maya App Location
    MAYA_LOCATION = os.environ['MAYA_LOCATION']

    # Source Mel Files
    mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikGlobalUtils.mel"')
    mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikCharacterControlsUI.mel"')
    mel.eval('source "'+MAYA_LOCATION+'/scripts/others/hikDefinitionOperations.mel"')
    mel.eval('source "'+MAYA_LOCATION+'/scripts/others/CharacterPipeline.mel"')
    mel.eval('source "'+MAYA_LOCATION+'/scripts/others/characterSelector.mel"')

    # Load Plugins
    if not mc.pluginInfo('mayaHIK',q=True,l=True):
        mc.loadPlugin('mayaHIK')
    if not mc.pluginInfo('mayaCharacterization',q=True,l=True):
        mc.loadPlugin('mayaCharacterization')
    if not mc.pluginInfo('retargeterNodes',q=True,l=True):
        mc.loadPlugin('retargeterNodes')

    # HIK Character Controls Tool
    mel.eval('HIKCharacterControlsTool')

def isCharacterDefinition(char):
    '''
    '''
    # Check Node Exists
    if not mc.objExists(char): return False

    # Check Node Type
    if mc.objectType(char) != 'HIKCharacterNode': return False

    # Return Result
    return True

def isCharacterDefinitionLocked(char):
    '''
    '''
    # Check Character Definition
    if not isCharacterDefinition(char):
        raise Exception('Invalid character definition node! Object "'+char+'" does not exist or is not a valid HIKCharacterNode!')

    # Check Lock
    lock = mc.getAttr(char+'.InputCharacterizationLock')

    # Return Result
    return lock

def characterDefinitionLock(char,lockState=True,saveStance=True):
    '''
    '''
    # Check Character Definition
    if not isCharacterDefinition(char):
        raise Exception('Invalid character definition node! Object "'+char+'" does not exist or is not a valid HIKCharacterNode!')

    # Check Lock State
    isLocked = isCharacterDefinitionLocked(char)

    # Set Lock State
    if lockState != isLocked: mel.eval('hikToggleLockDefinition')
    #mel.eval('mayaHIKcharacterLock("'+char+'",'+str(int(lockState))+','+str(int(saveStance))+')')

    # Return State
    return int(lockState)


def create(charName, charNS='', lock=True, rokoko=True):
    '''
    '''
    # ==========
    # - Checks -
    # ==========

    if charNS: charNS+=':'

    # ===============================
    # - Create Character Definition -
    # ===============================
    # Open HumanIK Tab

    mel.eval('HIKCharacterControlsTool')

    # Create character definition
    charDef = mel.eval('hikCreateCharacter("{}");'.format(charName))
    mel.eval('hikUpdateCharacterList();')
    mel.eval('hikSelectDefinitionTab();')
    #charDef = mel.eval('CreateHIKCharacterWithName "'+charName+'"')
    setCurrentCharacter(charDef)

    try:
        mel.eval('hikUpdateCharacterList()')
        mel.eval('hikSelectDefinitionTab()')
    except:
        pass

    # Apply Temmplate
    if rokoko:
        setCharacterObject(charDef, charNS+'Hips', 1, 0)
        setCharacterObject(charDef, charNS+'Head', 15, 0)
        setCharacterObject(charDef, charNS+'LeftArm', 9, 0)
        #setCharacterObject(charDef, charNS+'LeftArmRoll', 45, 0)
        setCharacterObject(charDef, charNS+'LeftFoot', 4, 0)
        setCharacterObject(charDef, charNS+'LeftForeArm', 10, 0)
        #setCharacterObject(charDef, charNS+'LeftForeArmRoll', 46, 0)
        setCharacterObject(charDef, charNS+'LeftHand', 11, 0)
        setCharacterObject(charDef, charNS+'LeftFinger2Proximal', 54, 0)
        setCharacterObject(charDef, charNS+'LeftFinger2Medial', 55, 0)
        setCharacterObject(charDef, charNS+'LeftFinger2Distal', 56, 0)
        setCharacterObject(charDef, charNS+'LeftFinger3Proximal', 58, 0)
        setCharacterObject(charDef, charNS+'LeftFinger3Medial', 59, 0)
        setCharacterObject(charDef, charNS+'LeftFinger3Distal', 60, 0)
        setCharacterObject(charDef, charNS+'LeftFinger5Proximal', 66, 0)
        setCharacterObject(charDef, charNS+'LeftFinger5Medial', 67, 0)
        setCharacterObject(charDef, charNS+'LeftFinger5Distal', 68, 0)
        setCharacterObject(charDef, charNS+'LeftFinger4Proximal', 62, 0)
        setCharacterObject(charDef, charNS+'LeftFinger4Medial', 63, 0)
        setCharacterObject(charDef, charNS+'LeftFinger4Distal', 64, 0)
        setCharacterObject(charDef, charNS+'LeftFinger1Metacarpal', 50, 0)
        setCharacterObject(charDef, charNS+'LeftFinger1Distal', 51, 0)
        setCharacterObject(charDef, charNS+'LeftFinger1Proximal', 52, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandIndex', 147, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandMiddle', 148, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandPinky', 150, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandRing', 149, 0)
        setCharacterObject(charDef, charNS+'LeftShin', 3, 0)
        #setCharacterObject(charDef, charNS+'LeftLegRoll', 42, 0)
        setCharacterObject(charDef, charNS+'LeftShoulder', 18, 0)
        setCharacterObject(charDef, charNS+'LeftToe', 16, 0)
        setCharacterObject(charDef, charNS+'LeftThigh', 2, 0)
        #setCharacterObject(charDef, charNS+'LeftUpLegRoll', 41, 0)
        setCharacterObject(charDef, charNS+'Neck', 20, 0)
        setCharacterObject(charDef, charNS+'Neck2', 32, 0)
        setCharacterObject(charDef, charNS+'global_ctrl', 0, 0)
        setCharacterObject(charDef, charNS+'RightArm', 12, 0)
        #setCharacterObject(charDef, charNS+'RightArmRoll', 47, 0)
        setCharacterObject(charDef, charNS+'RightFoot', 7, 0)
        setCharacterObject(charDef, charNS+'RightForeArm', 13, 0)
        #setCharacterObject(charDef, charNS+'RightForeArmRoll', 48, 0)
        setCharacterObject(charDef, charNS+'RightHand', 14, 0)
        setCharacterObject(charDef, charNS+'LeftFinger2Proximal', 78, 0)
        setCharacterObject(charDef, charNS+'LeftFinger2Medial', 79, 0)
        setCharacterObject(charDef, charNS+'LeftFinger2Distal', 80, 0)
        setCharacterObject(charDef, charNS+'LeftFinger3Proximal', 82, 0)
        setCharacterObject(charDef, charNS+'LeftFinger3Medial', 83, 0)
        setCharacterObject(charDef, charNS+'LeftFinger3Distal', 84, 0)
        setCharacterObject(charDef, charNS+'LeftFinger5Proximal', 90, 0)
        setCharacterObject(charDef, charNS+'LeftFinger5Medial', 91, 0)
        setCharacterObject(charDef, charNS+'LeftFinger5Distal', 92, 0)
        setCharacterObject(charDef, charNS+'LeftFinger4Proximal', 86, 0)
        setCharacterObject(charDef, charNS+'LeftFinger4Medial', 87, 0)
        setCharacterObject(charDef, charNS+'LeftFinger4Distal', 88, 0)
        setCharacterObject(charDef, charNS+'LeftFinger1Metacarpal', 74, 0)
        setCharacterObject(charDef, charNS+'LeftFinger1Distal', 75, 0)
        setCharacterObject(charDef, charNS+'LeftFinger1Proximal', 76, 0)
        #setCharacterObject(charDef, charNS+'RightInHandIndex', 153, 0)
        #setCharacterObject(charDef, charNS+'RightInHandMiddle', 154, 0)
        #setCharacterObject(charDef, charNS+'RightInHandPinky', 156, 0)
        #setCharacterObject(charDef, charNS+'RightInHandRing', 155, 0)
        setCharacterObject(charDef, charNS+'RightShin', 6, 0)
        #setCharacterObject(charDef, charNS+'RightLegRoll', 44, 0)
        setCharacterObject(charDef, charNS+'RightShoulder', 19, 0)
        setCharacterObject(charDef, charNS+'RightToe', 17, 0)
        setCharacterObject(charDef, charNS+'RightThigh', 5, 0)
        #setCharacterObject(charDef, charNS+'RightUpLegRoll', 43, 0)
        setCharacterObject(charDef, charNS+'Spine1', 8, 0)
        setCharacterObject(charDef, charNS+'Spine2', 23, 0)
        setCharacterObject(charDef, charNS+'Spine3', 24, 0)
        setCharacterObject(charDef, charNS+'Spine4', 25, 0)
        setCharacterObject(charDef, charNS+'Spine5', 26, 0)
        setCharacterObject(charDef, charNS+'Spine6', 27, 0)
    else:
        setCharacterObject(charDef, charNS+'c_pelvis_result_jnt', 1, 0)
        setCharacterObject(charDef, charNS+'c_headA_result_jnt', 15, 0)
        setCharacterObject(charDef, charNS+'l_armUpper_result_jnt', 9, 0)
        #setCharacterObject(charDef, charNS+'LeftArmRoll', 45, 0)
        setCharacterObject(charDef, charNS+'l_legEnd_result_jnt', 4, 0)
        setCharacterObject(charDef, charNS+'l_armLower_result_jnt', 10, 0)
        #setCharacterObject(charDef, charNS+'LeftForeArmRoll', 46, 0)
        setCharacterObject(charDef, charNS+'l_armEnd_result_jnt', 11, 0)
        setCharacterObject(charDef, charNS+'l_indexFA_result_jnt', 54, 0)
        setCharacterObject(charDef, charNS+'l_indexFB_result_jnt', 55, 0)
        setCharacterObject(charDef, charNS+'l_indexFC_result_jnt', 56, 0)
        setCharacterObject(charDef, charNS+'l_middleFA_result_jnt', 58, 0)
        setCharacterObject(charDef, charNS+'l_middleFB_result_jnt', 59, 0)
        setCharacterObject(charDef, charNS+'l_middleFC_result_jnt', 60, 0)
        setCharacterObject(charDef, charNS+'l_pinkyFA_result_jnt', 66, 0)
        setCharacterObject(charDef, charNS+'l_pinkyFB_result_jnt', 67, 0)
        setCharacterObject(charDef, charNS+'l_pinkyFC_result_jnt', 68, 0)
        setCharacterObject(charDef, charNS+'l_ringFA_result_jnt', 62, 0)
        setCharacterObject(charDef, charNS+'l_ringFB_result_jnt', 63, 0)
        setCharacterObject(charDef, charNS+'l_ringFC_result_jnt', 64, 0)
        setCharacterObject(charDef, charNS+'l_thumbFA_result_jnt', 50, 0)
        setCharacterObject(charDef, charNS+'l_thumbFB_result_jnt', 51, 0)
        setCharacterObject(charDef, charNS+'l_thumbFC_result_jnt', 52, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandIndex', 147, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandMiddle', 148, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandPinky', 150, 0)
        #setCharacterObject(charDef, charNS+'LeftInHandRing', 149, 0)
        setCharacterObject(charDef, charNS+'l_legLower_result_jnt', 3, 0)
        #setCharacterObject(charDef, charNS+'LeftLegRoll', 42, 0)
        setCharacterObject(charDef, charNS+'l_clavicle_result_jnt', 18, 0)
        setCharacterObject(charDef, charNS+'l_footLower_result_jnt', 16, 0)
        setCharacterObject(charDef, charNS+'l_legUpper_result_jnt', 2, 0)
        #setCharacterObject(charDef, charNS+'LeftUpLegRoll', 41, 0)
        setCharacterObject(charDef, charNS+'c_neckA_result_jnt', 20, 0)
        setCharacterObject(charDef, charNS+'c_neckB_result_jnt', 32, 0)
        setCharacterObject(charDef, charNS+'global_ctrl', 0, 0)
        setCharacterObject(charDef, charNS+'r_armUpper_result_jnt', 12, 0)
        #setCharacterObject(charDef, charNS+'RightArmRoll', 47, 0)
        setCharacterObject(charDef, charNS+'r_legEnd_result_jnt', 7, 0)
        setCharacterObject(charDef, charNS+'r_armLower_result_jnt', 13, 0)
        #setCharacterObject(charDef, charNS+'RightForeArmRoll', 48, 0)
        setCharacterObject(charDef, charNS+'r_armEnd_result_jnt', 14, 0)
        setCharacterObject(charDef, charNS+'l_indexFA_result_jnt', 78, 0)
        setCharacterObject(charDef, charNS+'l_indexFB_result_jnt', 79, 0)
        setCharacterObject(charDef, charNS+'l_indexFC_result_jnt', 80, 0)
        setCharacterObject(charDef, charNS+'l_middleFA_result_jnt', 82, 0)
        setCharacterObject(charDef, charNS+'l_middleFB_result_jnt', 83, 0)
        setCharacterObject(charDef, charNS+'l_middleFC_result_jnt', 84, 0)
        setCharacterObject(charDef, charNS+'l_pinkyFA_result_jnt', 90, 0)
        setCharacterObject(charDef, charNS+'l_pinkyFB_result_jnt', 91, 0)
        setCharacterObject(charDef, charNS+'l_pinkyFC_result_jnt', 92, 0)
        setCharacterObject(charDef, charNS+'l_ringFA_result_jnt', 86, 0)
        setCharacterObject(charDef, charNS+'l_ringFB_result_jnt', 87, 0)
        setCharacterObject(charDef, charNS+'l_ringFC_result_jnt', 88, 0)
        setCharacterObject(charDef, charNS+'l_thumbFA_result_jnt', 74, 0)
        setCharacterObject(charDef, charNS+'l_thumbFB_result_jnt', 75, 0)
        setCharacterObject(charDef, charNS+'l_thumbFC_result_jnt', 76, 0)
        #setCharacterObject(charDef, charNS+'RightInHandIndex', 153, 0)
        #setCharacterObject(charDef, charNS+'RightInHandMiddle', 154, 0)
        #setCharacterObject(charDef, charNS+'RightInHandPinky', 156, 0)
        #setCharacterObject(charDef, charNS+'RightInHandRing', 155, 0)
        setCharacterObject(charDef, charNS+'r_legLower_result_jnt', 6, 0)
        #setCharacterObject(charDef, charNS+'RightLegRoll', 44, 0)
        setCharacterObject(charDef, charNS+'r_clavicle_result_jnt', 19, 0)
        setCharacterObject(charDef, charNS+'r_footLower_result_jnt', 17, 0)
        setCharacterObject(charDef, charNS+'r_legUpper_result_jnt', 5, 0)
        #setCharacterObject(charDef, charNS+'RightUpLegRoll', 43, 0)
        setCharacterObject(charDef, charNS+'c_spineA_result_jnt', 8, 0)
        setCharacterObject(charDef, charNS+'c_spineB_result_jnt', 23, 0)
        setCharacterObject(charDef, charNS+'c_spineC_result_jnt', 24, 0)
        setCharacterObject(charDef, charNS+'c_spineD_result_jnt', 25, 0)
        setCharacterObject(charDef, charNS+'c_spineE_result_jnt', 26, 0)
        setCharacterObject(charDef, charNS+'c_spineF_result_jnt', 27, 0)


    mel.eval('hikUpdateContextualUI;')

    # ===============================
    # - Custom Rig Definition -
    # ===============================

    # Create custom rig button
    mel.eval('hikCreateCustomRig(" {} ");'.format(charName))

    retargeter = RetargeterGetName(charName)
    try:
        """RetargeterAddMapping(retargeter, "Head", "R", "c_head_ctrl", "15")
        RetargeterAddMapping(retargeter, "Head", "T", "c_head_ctrl", "15")
        RetargeterAddMapping(retargeter, "Neck", "R", "c_neckFK_ctrl", "20")
        RetargeterAddMapping(retargeter, "Spine2", "R", "c_spineF_result_ctrl", "1000")
        RetargeterAddMapping(retargeter, "Spine2", "T", "c_spineF_result_ctrl", "1000")
        RetargeterAddMapping(retargeter, "Spine1", "R", "c_spineD_FK_ctrl", "23")
        RetargeterAddMapping(retargeter, "Spine", "R", "c_spineB_FK_ctrl", "8")
        RetargeterAddMapping(retargeter, "Hips", "T", "COM_ctrl", "1")
        RetargeterAddMapping(retargeter, "Hips", "R", "COM_ctrl", "1")
        RetargeterAddMapping(retargeter, "LeftUpLeg", "R", "l_legUpper_FK_ctrl", "2")
        RetargeterAddMapping(retargeter, "LeftLeg", "R", "l_legLower_FK_ctrl", "3")
        RetargeterAddMapping(retargeter, "LeftFoot", "R", "l_legEnd_FK_ctrl", "4")
        RetargeterAddMapping(retargeter, "RightUpLeg", "R", "r_legUpper_FK_ctrl", "5")
        RetargeterAddMapping(retargeter, "RightLeg", "R", "r_legLower_FK_ctrl", "6")
        RetargeterAddMapping(retargeter, "RightFoot", "R", "r_legEnd_FK_ctrl", "7")
        RetargeterAddMapping(retargeter, "LeftShoulder", "R", "l_armScapula_ctrl", "18")
        RetargeterAddMapping(retargeter, "LeftArm", "R", "l_armUpper_FK_ctrl", "9")
        RetargeterAddMapping(retargeter, "LeftForeArm", "R", "l_armLower_FK_ctrl", "10")
        RetargeterAddMapping(retargeter, "LeftHand", "R", "l_armEnd_FK_ctrl", "11")
        RetargeterAddMapping(retargeter, "RightShoulder", "R", "r_armScapula_ctrl", "19")
        RetargeterAddMapping(retargeter, "RightArm", "R", "r_armUpper_FK_ctrl", "12")
        RetargeterAddMapping(retargeter, "RightForeArm", "R", "r_armLower_FK_ctrl", "13")
        RetargeterAddMapping(retargeter, "RightHand", "R", "r_armEnd_FK_ctrl", "14")"""

        RetargeterAddMapping(retargeter, "Head", "R", charNS+"c_head_ctrl", "15")
        #RetargeterAddMapping(retargeter, "Head", "T", charNS+"c_head_ctrl", "15")
        RetargeterAddMapping(retargeter, "Neck", "R", charNS+"c_neckFK_ctrl", "20")
        RetargeterAddMapping(retargeter, "Spine2", "R", charNS+"c_spineF_IK_ctrl", "1000")
        RetargeterAddMapping(retargeter, "Spine2", "T", charNS+"c_spineF_IK_ctrl", "1000")
        RetargeterAddMapping(retargeter, "Spine1", "R", charNS+"c_spineD_FK_ctrl", "23")
        RetargeterAddMapping(retargeter, "Spine", "R", charNS+"c_spineB_FK_ctrl", "8")
        RetargeterAddMapping(retargeter, "Hips", "T", charNS+"COM_ctrl", "1")
        RetargeterAddMapping(retargeter, "Hips", "R", charNS+"COM_ctrl", "1")
        #RetargeterAddMapping(retargeter, "LeftUpLeg", charNS+"R", "l_legUpper_FK_ctrl", "2")
        RetargeterAddMapping(retargeter, "LeftLeg", "R", charNS+"l_legPoleVecOffset_grp", "3")
        RetargeterAddMapping(retargeter, "LeftLeg", "T", charNS+"l_legPoleVecOffset_grp", "3")
        RetargeterAddMapping(retargeter, "LeftFoot", "R", charNS+"l_legIK_ctrl", "4")
        RetargeterAddMapping(retargeter, "LeftFoot", "T", charNS+"l_legIK_ctrl", "4")
        #RetargeterAddMapping(retargeter, "RightUpLeg", "R", charNS+"r_legUpper_FK_ctrl", "5")
        RetargeterAddMapping(retargeter, "RightLeg", "R", charNS+"r_legPoleVecOffset_grp", "6")
        RetargeterAddMapping(retargeter, "RightLeg", "T", charNS+"r_legPoleVecOffset_grp", "6")
        RetargeterAddMapping(retargeter, "RightFoot", "R", charNS+"r_legIK_ctrl", "7")
        RetargeterAddMapping(retargeter, "RightFoot", "T", charNS+"r_legIK_ctrl", "7")
        RetargeterAddMapping(retargeter, "LeftShoulder", "R", charNS+"l_armScapula_ctrl", "18")

        ### FK ###
        RetargeterAddMapping(retargeter, "LeftArm", "R", charNS+"l_armUpper_FK_ctrl", "9")
        RetargeterAddMapping(retargeter, "LeftForeArm", "R", charNS+"l_armLower_FK_ctrl", "10")
        RetargeterAddMapping(retargeter, "LeftHand", "R", charNS+"l_armEnd_FK_ctrl", "11")

        ### IK ###
        """
        RetargeterAddMapping(retargeter, "LeftForeArm", "R", charNS+"l_armPoleVecOffset_grp", "10")
        RetargeterAddMapping(retargeter, "LeftForeArm", "T", charNS+"l_armPoleVecOffset_grp", "10")
        RetargeterAddMapping(retargeter, "LeftHand", "R", charNS+"l_armIK_ctrl", "11")
        RetargeterAddMapping(retargeter, "LeftHand", "T", charNS+"l_armIK_ctrl", "11")
        """

        RetargeterAddMapping(retargeter, "RightShoulder", "R", charNS+"r_armScapula_ctrl", "19")

        ### FK ###
        RetargeterAddMapping(retargeter, "RightArm", "R", charNS+"r_armUpper_FK_ctrl", "12")
        RetargeterAddMapping(retargeter, "RightForeArm", "R", charNS+"r_armLower_FK_ctrl", "13")
        RetargeterAddMapping(retargeter, "RightHand", "R", charNS+"r_armEnd_FK_ctrl", "14")

        ### IK ###
        """
        RetargeterAddMapping(retargeter, "RightForeArm", "R", charNS+"r_armPoleVecOffset_grp", "13")
        RetargeterAddMapping(retargeter, "RightForeArm", "T", charNS+"r_armPoleVecOffset_grp", "13")
        RetargeterAddMapping(retargeter, "RightHand", "R", charNS+"r_armIK_ctrl", "14")
        RetargeterAddMapping(retargeter, "RightHand", "T", charNS+"r_armIK_ctrl", "14"
        """
    except:
        pass

    mel.eval('hikUpdateCustomRigUI();')

    # =======================================
    # - Set Character Definition Properties -
    # =======================================

    # Get Character Definition Properties Node
    propertyNode = getPropertiesNode(charDef)

    # Match Source
    mc.setAttr(propertyNode+'.ForceActorSpace', 0)  # OFF
    # Action Space Comp Mode
    mc.setAttr(propertyNode+'.ScaleCompensationMode', 1)  # AUTO
    # Mirror Animation
    mc.setAttr(propertyNode+'.Mirror', 0)  # OFF
    # Hips Level Mode
    mc.setAttr(propertyNode+'.HipsHeightCompensationMode', 1)  # AUTO
    # Feet Spacing Mode
    mc.setAttr(propertyNode+'.AnkleProximityCompensationMode', 1)  # AUTO
    # Ankle Height Compensation
    mc.setAttr(propertyNode+'.AnkleHeightCompensationMode', 0)  # OFF
    # Mass Center Comp Mode
    mc.setAttr(propertyNode+'.MassCenterCompensationMode', 1)  # ON

    # ===================
    # - Lock Definition -
    # ===================

    if lock:
        #characterDefinitionLock(charDef,lockState=True,saveStance=True)
        mel.eval('hikToggleLockDefinition();')

    # =================
    # - Return Result -
    # =================

    return charDef


def setCharacterObject(charDef, charBone, boneId, deleteBone=False):
    '''
    '''
    mel.eval('setCharacterObject("'+charBone+'","'+charDef+'",'+str(boneId)+','+str(int(deleteBone))+')')


def getCurrentCharacter():
    '''
    '''
    char = mel.eval('hikGetCurrentCharacter()')
    return char


def setCurrentCharacter(char):
    '''
    '''
    mel.eval('hikSetCurrentCharacter("'+char+'")')
    mel.eval('hikUpdateCharacterList()')
    mel.eval('hikSetCurrentSourceFromCharacter("'+char+'")')
    mel.eval('hikUpdateSourceList()')


def getPropertiesNode(char):
    '''
    '''
    # Check Node
    if not isCharacterDefinition(char):
        raise Exception('Invalid character definition node! Object "'+char+'" does not exist or is not a valid HIKCharacterNode!')

    propertyNode = ''
    try:
        propertyNode = mel.eval('getProperty2StateFromCharacter("'+char+'")')
    except:

        # Get propertyState Connections
        conn = mc.listConnections(char+'.propertyState',s=True,d=False)
        if not conn:
            raise Exception('Unable to determine HIKProperty2State node from character definition node "'+char+'"!')

        # Check Number of Results
        if len(conn) > 1:
            print('Multiple HIKProperty2State nodes found for character definition "'+char+'"! Returning first item only...')

        # Assign Property Node
        propertyNode = conn[0]

    # Return Result
    return propertyNode


def RetargeterGetName(character):
    """Return the name of the retargeter associated with a given character
    whatIs RetargeterGetName;
    """

    getName = mel.eval('RetargeterGetName("{}")'.format(character))

    return getName


def RetargeterAddMapping(retargeter, body, variant, rig, index):
    """Add a mapping to the named retargeter, with options provided as arguments
    whatIs RetargeterAddMapping;
    """

    addMapping = mel.eval('RetargeterAddMapping("{}", "{}", "{}", "{}", "{}")'.format(retargeter, body, variant, rig, index))

    return addMapping
