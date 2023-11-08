from user_agents import parse


# Function to parse user agent string
def parse_user_agent(user_agent_str):
    if (
        user_agent_str == "Unknown"
    ):  # If the user_agent_str is "Unknown", return "Unknown" for all values
        return "Unknown", "Unknown", "Unknown"

    user_agent = parse(user_agent_str)

    # Determining the device type
    device_type = (
        "Mobile"
        if user_agent.is_mobile
        else "Tablet"
        if user_agent.is_tablet
        else "Computer"
        if user_agent.is_pc
        else "Bot"
        if user_agent.is_bot
        else "Other"
    )

    # Extracting browser type and version
    browser_type = user_agent.browser.family
    browser_version = ".".join(map(str, user_agent.browser.version))

    return device_type, browser_type, browser_version
