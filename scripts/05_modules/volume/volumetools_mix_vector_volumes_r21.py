"""
Copyright: MAXON Computer GmbH
Author: Maxime Adam

Description:
    - Creates 2 vector volume from scratch.
    - Mixes both vector volumes with a cross product to produce a third vector volume.
    - Inserts all 3 volumes into the scene.

Class/method highlighted:
    - maxon.frameworks.volume.VolumeToolsInterface.CreateNewVector32Volume()
    - maxon.frameworks.volume.GridAccessorInterface
    - GridAccessorRef.InitWithWriteAccess()
    - GridAccessorRef.SetValue()
    - maxon.frameworks.volume.VolumeToolsInterface.MixVectorVolumes()
    - c4d.VolumeObject
    - VolumeObject.SetVolume()

Compatible:
    - Win / Mac
    - R21, S22
"""
import c4d
import maxon
from maxon.frameworks import volume


def CreateVectorVolume(vectorValue):
    """
    Creates a VolumeRef defined as a vector volume, with a cube of 100 cm (10* 10) filled with the vector passed.

    :param vectorValue: The vector value to set.
    :type vectorValue: maxon.Vector32
    :return: The created Vector volume with the value defined inside.
    :rtype: maxon.frameworks.volume.VolumeRef
    """
    # Creates volume
    volumeRef = maxon.frameworks.volume.VolumeToolsInterface.CreateNewVector32Volume(maxon.Vector32(0.0))
    if volumeRef is None:
        raise MemoryError("Failed to create a float32 volume.")

    # Creates accessor
    access = maxon.frameworks.volume.GridAccessorInterface.Create(maxon.Vector32)
    if access is None:
        raise RuntimeError("Failed to retrieve the grid accessor.")

    # Initializes the grid for write access
    access.InitWithWriteAccess(volumeRef)

    # Sets values
    size = 10
    step = 10.0
    for x in range(size):
        for y in range(size):
            for z in range(size):
                pos = maxon.IntVector32(x * step, y * step, z * step)
                access.SetValue(pos, vectorValue)

    return volumeRef


def CreateVectorObject(volumeRef, name):
    """
    Creates a c4d.VolumeObject with the VolumeRef passed.
    Names this VolumeObject with the passed argument.
    Inserts the VolumeObject into the current document.

    :param volumeRef: The VolumeRef to use within the VolumeObject.
    :type volumeRef: maxon.frameworks.volume.VolumeRef
    :param name: The name of the inserted object into the scene.
    :type name: str
    """
    # Creates VolumeObject
    volumeObj = c4d.BaseObject(c4d.Ovolume)
    if volumeObj is None:
        raise MemoryError("Failed to create a volume object.")

    # Names the VolumeObject
    volumeObj.SetName(name)

    # Inserts volume in the VolumeObject
    volumeObj.SetVolume(volumeRef)

    # Inserts the volume Object within the scene
    doc.InsertObject(volumeObj, None, None)


def main():
    # Creates a VectorVolume
    volumeRefA = CreateVectorVolume(maxon.Vector32(0, 0, 10))
    volumeRefB = CreateVectorVolume(maxon.Vector32(10.0, 0, 0))

    # Inserts these vector volume into the scene
    CreateVectorObject(volumeRefA, "Volume A")
    CreateVectorObject(volumeRefB, "Volume B")

    # Mixes both vector volume together using cross product
    resultMixVolume = volume.VolumeToolsInterface.MixVectorVolumes(volumeRefA, volumeRefB, c4d.MIXVECTORTYPE_CROSS)

    # Inserts the mixed volume into the scene
    CreateVectorObject(resultMixVolume, "Mixed Volume")

    # Pushes an update event to Cinema 4D
    c4d.EventAdd()


if __name__ == '__main__':
    main()
