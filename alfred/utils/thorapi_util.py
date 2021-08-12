def validate_action(action_data):
    """
    Ensure actions are valid for the current version of thor. Updates them as necessary.
    """

    if action_data["action"] == "TeleportFull":
        standing_state = action_data.get("standing", "True")
        action_data["standing"] = standing_state
    return action_data
