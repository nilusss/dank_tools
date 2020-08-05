#       hik_prep
#       Version 0.0.1
#       Copyright (C)2020 Nilas Niebuhr
#       Email: niebuhrgfx@gmail.com
#       Last Modified: 19/05/2020
#
#
# hik_prep makes it easier for prepping the rig for mocap in humanik
#
# For detailed instructions read the "readme.txt" file
#
import os

import maya.cmds as mc

import dank_tools.tools.set_tpose as set_tpose
import dank_tools.tools.characterize as chrtze

reload(set_tpose)
reload(chrtze)


def prep(rokoko=False, asset_name='', ns=False, new_name=False):
    """[summary]
    """

    try:
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
                        ns_use = n
        else:
            ns_use = ''

        set_tpose.tpose(rokoko=rokoko, charNS=ns_use)
        chrtze.create(charName=asset_name + '_HIK', charNS=ns_use, rokoko=new_name)
    except Exception as e:
        mc.warning('Couldn\'t prep the rig. Make sure the rig is in the scene. EXCEPTION: ' + str(e))
