def validate_action(action_data):
    """
    Ensure actions are valid for the current version of thor. Updates them as necessary.
    """

    if action_data["action"] == "TeleportFull" or action_data["action"] == "Teleport":
        standing_state = action_data.get("standing", "True")
        action_data["standing"] = standing_state

        if not action_data.pop("rotateOnTeleport", False):
            action_data.pop("rotation", None)

        action_data["action"] = "Teleport"

    elif action_data["action"] == "GetReachablePositions":
        action_data.pop("gridSize", None)
        """
        Action: "GetReachablePositions" called with invalid argument: 'gridSize'
        Expected arguments: Nullable`1 maxStepCount = , Boolean directionsRelativeAgent = False
        Your arguments: 'gridSize'
        Valid ways to call "GetReachablePositions" action:
                Void GetReachablePositions(Nullable`1 maxStepCount = , Boolean directionsRelativeAgent = False)
        """

    return action_data
