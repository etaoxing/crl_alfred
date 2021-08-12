def validate_action(action_data):
    """
    Ensure actions are valid for the current version of thor. Updates them as necessary.
    """

    if action_data["action"] == "TeleportFull":
        standing_state = action_data.get("standing", "True")
        action_data["standing"] = standing_state

        if not action_data.pop("rotateOnTeleport", False):
            action_data.pop("rotation", None)

        action_data["action"] = "Teleport"
    return action_data
