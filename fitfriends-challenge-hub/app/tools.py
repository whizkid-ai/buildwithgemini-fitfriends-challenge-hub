"""Tools for FitFriends Challenge Hub ADK Agent."""

import json
from app.fitfriends_store import store


def sync_health_metrics(
    steps: int = 0,
    sleep_hours: float = 0.0,
    active_hours: float = 0.0,
    calories: int = 0,
    date: str = "",
) -> str:
    """Sync or log health metrics (steps, sleep hours, active hours, calories burned) for the user.

    Args:
        steps: Number of steps logged (e.g., 10000).
        sleep_hours: Total sleep hours (e.g., 7.5).
        active_hours: Active exercise hours (e.g., 1.5).
        calories: Total active/burned calories (e.g., 2200).
        date: Date in YYYY-MM-DD format. Leave blank for today.

    Returns:
        JSON string confirming the synced health metrics.
    """
    res = store.sync_metrics(
        user_id="current_user",
        steps=steps,
        sleep_hours=sleep_hours,
        active_hours=active_hours,
        calories=calories,
        date_str=date,
    )
    return json.dumps(res, indent=2)


def get_user_health_profile(user_id: str = "current_user") -> str:
    """Get connected health profile, Garmin/Google Health status, activity preferences, active challenges, and daily trends.

    Args:
        user_id: User identifier, defaults to "current_user".

    Returns:
        JSON string with health profile details.
    """
    profile = store.get_user_profile(user_id)
    return json.dumps(profile, indent=2)


def create_challenge(
    title: str,
    metric: str,
    goal: int,
    start_date: str,
    end_date: str,
    is_private: bool = False,
    description: str = "",
) -> str:
    """Create a new public or private fitness challenge and return a shareable invite URL.

    Args:
        title: Title of the challenge (e.g., "August Steps Challenge", "Cycle Sprint").
        metric: Target metric ("steps", "calories", "distance", or "active_hours").
        goal: Total metric goal to reach (e.g., 300000).
        start_date: Start date in YYYY-MM-DD format (e.g., "2026-08-01").
        end_date: End date in YYYY-MM-DD format (e.g., "2026-08-31").
        is_private: Whether the challenge requires an invite code or private link.
        description: Brief summary of rules and goals.

    Returns:
        JSON string with created challenge details and shareable invite URL.
    """
    res = store.create_challenge(
        title=title,
        metric=metric,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
        is_private=is_private,
        description=description,
        owner_id="current_user",
    )
    return json.dumps(res, indent=2)


def join_challenge(challenge_id_or_invite: str) -> str:
    """Join an existing fitness challenge using a challenge ID or shareable invite URL.

    Args:
        challenge_id_or_invite: Challenge ID (e.g. "august-steps-2026") or invite link.

    Returns:
        JSON string confirming membership.
    """
    res = store.join_challenge(challenge_id_or_invite, user_id="current_user")
    return json.dumps(res, indent=2)


def get_challenge_details(challenge_id: str) -> str:
    """Get challenge rules, dates, metric goals, shareable invite URL, and participant roster.

    Args:
        challenge_id: ID or title of the challenge (e.g. "august-steps-2026").

    Returns:
        JSON string with challenge details.
    """
    res = store.get_challenge_details(challenge_id)
    return json.dumps(res, indent=2)


def get_leaderboard(challenge_id: str) -> str:
    """Get the live real-time leaderboard table with rankings, totals, daily averages, and gaps.

    Args:
        challenge_id: ID or title of the challenge (e.g. "august-steps-2026").

    Returns:
        JSON string containing the sorted leaderboard table.
    """
    res = store.get_leaderboard(challenge_id)
    return json.dumps(res, indent=2)


def calculate_leaderboard_stats(
    challenge_id: str, custom_handicap: float = 1.0
) -> str:
    """Calculate advanced leaderboard analytics: completion percentages, projected finishes, handicap adjustments, and daily steps/metrics needed to catch up to 1st place.

    Args:
        challenge_id: Challenge ID or title (e.g. "august-steps-2026").
        custom_handicap: Handicap multiplier adjustment (default 1.0).

    Returns:
        JSON string with exact calculation formulas, daily requirement to win, and projected standings.
    """
    res = store.calculate_leaderboard_stats(
        challenge_id=challenge_id, user_id="current_user", custom_handicap=custom_handicap
    )
    return json.dumps(res, indent=2)


def generate_badge_or_recap(
    challenge_id_or_event: str,
    badge_type: str = "achievement",
    title: str = "Challenge Hero",
) -> str:
    """Generate personalized achievement badges, milestone trophy images, or weekly challenge recap banners.

    Args:
        challenge_id_or_event: Challenge ID or event name.
        badge_type: Type of badge ("achievement", "trophy", or "recap").
        title: Title/headline for the badge (e.g. "Step Master", "Top 3 Finish").

    Returns:
        JSON string with badge asset metadata and image URL.
    """
    res = store.generate_badge(
        challenge_id_or_event=challenge_id_or_event,
        badge_type=badge_type,
        title=title,
        user_id="current_user",
    )
    return json.dumps(res, indent=2)


def manage_account_settings(
    display_name: str = "",
    preferences: str = "",
    connected_devices: str = "",
) -> str:
    """Manage and update account settings, display name, activity preferences, and connected health hardware/apps.

    Args:
        display_name: Updated display name (e.g. "Sarah Jenkins").
        preferences: Comma-separated activity preferences (e.g. "running, hiking, swimming").
        connected_devices: Comma-separated hardware/apps (e.g. "Garmin Forerunner, Google Health").

    Returns:
        JSON string with updated settings.
    """
    pref_list = [p.strip() for p in preferences.split(",")] if preferences else None
    dev_list = [d.strip() for d in connected_devices.split(",")] if connected_devices else None

    res = store.update_user_settings(
        user_id="current_user",
        display_name=display_name or None,
        preferences=pref_list,
        connected_devices=dev_list,
    )
    return json.dumps(res, indent=2)
