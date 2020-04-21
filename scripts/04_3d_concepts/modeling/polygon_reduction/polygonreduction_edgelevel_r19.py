"""
Copyright: MAXON Computer GmbH
Author: Yannick Puech

Description:
    - Reduces the active PolygonObject to the given edge count.

Class/method highlighted:
    - c4d.utils.PolygonReduction

Compatible:
    - Win / Mac
    - R19, R20, R21, S22
"""
import c4d


def main():
    # Checks if selected object is valid
    if op is None:
        raise ValueError("op is none, please select one object.")

    # Check if it's a polygon object
    if not op.IsInstanceOf(c4d.Opolygon):
        raise TypeError("Selected object is not a polygon Object.")

    # Defines settings for PolygonReduction.PreProcess()
    settings = c4d.BaseContainer()
    settings[c4d.POLYREDUXOBJECT_PRESERVE_3D_BOUNDARY] = True
    settings[c4d.POLYREDUXOBJECT_PRESERVE_UV_BOUNDARY] = True

    # Defines data for PolygonReduction.PreProcess()
    data = dict()
    data['_op'] = op
    data['_doc'] = doc
    data['_settings'] = settings
    data['_thread'] = None

    # Creates PolygonReduction object
    polyReduction = c4d.utils.PolygonReduction()
    if polyReduction is None:
        raise RuntimeError("Failed to create the PolygonReduction.")

    # Pre-process the data
    if not polyReduction.PreProcess(data):
        raise RuntimeError("Failed to Pre-Process the PolygonReduction with data.")

    # Asks for number of edges level
    while True:
        # Opens a Dialog where user can enter a text
        userInput = c4d.gui.InputDialog("Enter number of edges level:")

        # Checks if operation was cancelled
        if userInput == "":
            return

        # Tries to convert to integer
        try:
            edgesLevel = int(userInput)
            break
        except ValueError:
            c4d.gui.MessageDialog("Please enter a number.")

    # Sets edges level number
    polyReduction.SetRemainingEdgesLevel(min(edgesLevel, polyReduction.GetMaxRemainingEdgesLevel()))
    polyReduction.SetRemainingEdgesLevel(min(edgesLevel, polyReduction.GetMaxRemainingEdgesLevel()))

    # Retrieves edges level count after reduction
    realEdgeResult = polyReduction.GetRemainingEdgesLevel()
    print("Edge Result: {0}".format(realEdgeResult))

    # Updates the original PolygonObject
    op.Message(c4d.MSG_UPDATE)

    # Pushes an update event to Cinema 4D
    c4d.EventAdd()


if __name__ == '__main__':
    main()