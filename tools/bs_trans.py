"""
Version 2.0 of blendshape_transfer.py
New version uses PyMel instead of maya commands
"""

import os
import pdb
import pymel.core as pm
import dank_tools.vendor.rr_wrap as rr_wrap


def transfer(asset_name="new", sourceUvSpace='DiffuseUV', targetUvSpace='DiffuseUV'):

    """
    Function to transfer blendshapes from driver to driven

    Args:
        asset_name (string, optional): Name of the new asset to transfer to. Defaults to "new"
        sourceUvSpace (string, optional): Defaults to "DiffuseUV"
        targetUvSpace (string, optional): Defaults to "DiffuseUV"

    """

    selection = pm.ls(sl=True)

    if selection:
        driver_model = selection[-2]  # Get driver model from selection
        driven_model = selection[-1]  # Get driven model from selection
        del(selection[-2:])  # Delete driver and driven model from selection

        # If the selection is larger or equal to one, create a blendshape node
        # on the driver model
        if len(selection) >= 1:
            # Take driver targets and rename with "temp_"
            target_list = []
            for t in selection:
                target = pm.rename(t, 'temp_{}'.format(t.name()))
                target_list.append(target)
            pm.blendShape(target_list, driver_model, name="blendShape_Base")
        else:
            pm.warning('No blendshapes selected! Make sure they already are on the driver model')

        # Duplicate the new model and create a blendshape between the base
        # and the new model on the inbetween (duplicate)
        inbetween_model = pm.duplicate(driven_model, rr=True)[0]

        # Transfer attributes from the driver model to the driven model to match UVs
        pm.transferAttributes(driver_model, driven_model, pos=1, transferNormals=0,
                              uvs=2, transferColors=0, sampleSpace=3,
                              sus='DiffuseUV', tus='DiffuseUV', searchMethod=3,
                              fuv=0, colorBorders=1)
        inbetween_attr_model = pm.duplicate(driven_model, rr=True)

        inbetween_blend = pm.blendShape(driven_model, inbetween_model, inbetween_attr_model)[0]
        pm.blendShape(inbetween_blend, edit=True, weight=[(0, 1), (1, 1)])

        # Get blend shape node from the base model
        driver_model_history = pm.listHistory(driver_model)
        driver_model_bs_node = pm.ls(driver_model_history, type='blendShape')[0]

        # Iterate through the base model, activate one blendshape at a time,
        # duplicate it from the duplicate model and  create a blendshape from
        # it on the new model
        new_shapes = []
        for index, target in enumerate(target_list):
            pm.setAttr('{}.{}'.format(driver_model_bs_node, target), 1)
            bs_driven_model = pm.duplicate(inbetween_attr_model, name='{}'.format(target.replace('temp_', '')), rr=True)[0]
            new_shapes.append(bs_driven_model)
            pm.setAttr('{}.{}'.format(driver_model_bs_node, target), 0)
            pm.hide(bs_driven_model)

        print(new_shapes)
        pm.blendShape(new_shapes, inbetween_attr_model, name='{}_bs'.format(asset_name))

        # Create blendshape group for the new model
        bs_group = pm.group(em=True, name=asset_name + '_blendshapes_grp')
        pm.parent(new_shapes, bs_group)

        # Delete the duplicate/inbetween models, when blenshapes transfer is done
        pm.delete([inbetween_model, driven_model])
        pm.rename(inbetween_attr_model, driven_model)
        return new_shapes
    else:
        pm.warning("Nothing selected!")
        return

