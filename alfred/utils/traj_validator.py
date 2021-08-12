

class TrajValidator(object):
    """
    Ensure trajectories are valid for the current version of thor. Updates them as necessary.
    """

    @staticmethod
    def validate_action(action_data):
        if action_data["action"] == "TeleportFull":
            standing_state = action_data.get("standing", "True")
            action_data["standing"] = standing_state

        return action_data

    @staticmethod
    def validate_trajectory(traj_data):
        pass
