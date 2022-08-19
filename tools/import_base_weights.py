"""
import_base_weights.py is responsible for importing base skin weights onto a "new" model.
The base weights are done on the base mesh.
"""

import pymel.core as pm


def apply_weights(base_mesh_name="base"):
    """

    Args:
        base_mesh_name:

    Returns:

    """

    try:
        selection = pm.ls(sl=True)[0]
        mesh_name = selection
    except:
        pm.error("Nothing selected!")

    bk_mesh_name = mesh_name.name()
    mesh_name.rename(base_mesh_name)
    pm.runtime.ImportSkinWeightMaps()

    mesh_name.rename(bk_mesh_name)

