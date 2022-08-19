import os
import maya.cmds as mc
import dank_tools.vendor.rr_wrap as rr_wrap


def transfer(asset_name=''):

    # If asset name is not set get the name from file
    if not asset_name:
        # Get asset name from file
        filepath = mc.file(q=True, sn=True)
        if filepath:
            filename = os.path.basename(filepath)
            asset_name = filename.split("_")[0].split(".")[0]
        else:
            mc.warning("No asset name set!")
            return

    sel = mc.ls(sl=True)

    if sel:
        base_model = sel[-2]  # Get base model from selection
        new_model = sel[-1]  # Get new model from selection
        del(sel[-2:])  # Delete the new and base model from selection

        # If the selection is larger or equal to one, create a blendshape
        # between selected blendshapes and the base model
        if len(sel) >= 1:
            # Take base targets and rename with temp_prefix
            target_list = []
            for t in sel:
                target = mc.rename('temp_' + t)
                target_list.append(target)
            mc.blendShape(target_list, base_model, name="blendShape_Base")
        else:
            mc.warning('No blendshapes selected!')
            return

        # Duplicate the new model and create a blendshape between the base
        # and new model on the duplicate
        dup_model = mc.duplicate(new_model, rr=True)[0]

        # Transfer attributes from the base model to the new model to match UVs
        mc.transferAttributes(base_model, new_model, pos=1, transferNormals=0,
                              uvs=2, transferColors=2, sampleSpace=3,
                              sus='map1', tus='map1', searchMethod=3,
                              fuv=0, colorBorders=1)
        dup_tattr_model = mc.duplicate(new_model, rr=True)[0]
        dup_blend = mc.blendShape(new_model, dup_model, dup_tattr_model)[0]
        mc.blendShape(dup_blend, edit=True, w=[(0, 1), (1, 1)])

        # Get blendshape nodes from the base model
        bm_history = mc.listHistory(base_model)
        bm_bshape_node = mc.ls(bm_history, type='blendShape')[0]
        bs_target = mc.listAttr(bm_bshape_node + ".w", m=True)

        # Iterate through the base model, activate one blendshape at a time,
        # duplicate it from the duplicate model and create a blendshape from
        # it on the new model
        new_shapes = []
        for index, target in enumerate(target_list):
            #bm_bshape_name = mc.listAttr(bm_bshape_node + ".w", m=True)[index]
            mc.setAttr('{}.{}'.format(bm_bshape_node, target), 1)
            bs_new_model = mc.duplicate(dup_tattr_model, name='{}'.format(target.replace('temp_', '')), rr=True)[0]
            new_shapes.append(bs_new_model)
            #mc.blendShape(bs_new_model, new_model, name='{}_bs_{}'.format(asset_name, bm_bshape_name))
            mc.setAttr('{}.{}'.format(bm_bshape_node, target), 0)
            mc.hide(bs_new_model)
        print(new_shapes)
        mc.blendShape(new_shapes, dup_tattr_model, name='{}_bs'.format(asset_name))
        # Create blendshape group for the new model
        bs_group = mc.group(em=True, name=asset_name + '_blendshapes_grp')
        mc.parent(new_shapes, bs_group)

        # Delete the duplicated model, when blendshape transfer is done.
        mc.delete(dup_model)
        mc.delete(new_model)
        mc.rename(dup_tattr_model, new_model)
        return new_shapes

    else:
        mc.warning('Nothing selected!')
        return


def wrap_to_blendshapes(model, wrap, asset_name, targets=[], export=''):
    # If asset name is not set get the name from file
    if not asset_name:
        # Get asset name from file
        filepath = mc.file(q=True, sn=True)
        if filepath:
            filename = os.path.basename(filepath)
            asset_name = filename.split("_")[0].split(".")[0]
        else:
            mc.warning("No asset name set!")
    if targets:
        # Take blendshapes and put them on the wrap
        mc.blendShape(targets, wrap, name=asset_name + '_bs')

    # Create a wrap using Ryan Roberts - Wrap Deformer
    wrap_def = rr_wrap.createWrap(wrap, model, exclusiveBind=True)
    mc.hide(wrap)

    wrap_history = mc.listHistory(wrap)
    wrap_bshape_node = mc.ls(wrap_history, type='blendShape')[0]
    wrap_targets = mc.listAttr(wrap_bshape_node + ".w", m=True)

    new_shapes = []
    for index, target in enumerate(wrap_targets):
        #bm_bshape_name = mc.listAttr(bm_bshape_node + ".w", m=True)[index]
        mc.setAttr('{}.{}'.format(wrap_bshape_node, target), 1)
        bs_new_model = mc.duplicate(model, name='{}'.format(target.replace('wrap_', '')), rr=True)[0]
        new_shapes.append(bs_new_model)
        #mc.blendShape(bs_new_model, new_model, name='{}_bs_{}'.format(asset_name, bm_bshape_name))
        mc.setAttr('{}.{}'.format(wrap_bshape_node, target), 0)
        mc.hide(bs_new_model)

    #mc.blendShape(new_shapes, model, name='{}_bs'.format(asset_name))
    # Create blendshape group for the new model
    for t in targets:
        mc.rename(t, t+'_temp')
    bs_group = mc.group(em=True, name=asset_name + '_bs_grp')
    mc.parent(new_shapes, bs_group)
    for s in new_shapes:
        mc.rename(s, s.replace('1', ''))

    if export:
        mc.select(bs_group, replace=True)
        dist = mc.file("{}/{}_blendshapes.ma".format(export, asset_name), es=True, type='mayaAscii')
        print(dist)

    mc.delete(bs_group)
    try:
        mc.delete(wrap + 'Base')
    except:
        pass
    mc.hide(wrap)

    for t in targets:
        mc.rename(t+'_temp', t.replace('_temp', ''))
