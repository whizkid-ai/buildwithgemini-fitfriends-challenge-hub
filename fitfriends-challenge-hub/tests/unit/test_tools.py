"""Unit tests for FitFriends Challenge Hub tools and store."""

import json
from app.tools import (
    sync_health_metrics,
    get_user_health_profile,
    create_challenge,
    join_challenge,
    get_challenge_details,
    get_leaderboard,
    calculate_leaderboard_stats,
    generate_badge_or_recap,
    manage_account_settings,
)


def test_get_user_health_profile():
    res = json.loads(get_user_health_profile())
    assert res["user_id"] == "current_user"
    assert "Garmin Forerunner 955" in res["connected_devices"]
    assert "August Steps Challenge" in res["active_challenges"]


def test_sync_health_metrics():
    res = json.loads(sync_health_metrics(steps=12000, calories=2500, date="2026-08-14"))
    assert res["status"] == "success"
    assert res["synced_metrics"]["steps"] == 12000


def test_get_leaderboard_and_stats():
    lb = json.loads(get_leaderboard("august-steps-2026"))
    assert lb["title"] == "August Steps Challenge"
    assert len(lb["leaderboard"]) >= 2

    stats = json.loads(calculate_leaderboard_stats("august-steps-2026"))
    assert stats["current_user_rank"] == 2
    assert "daily_metric_needed_to_catch_up" in stats
    assert stats["daily_metric_needed_to_catch_up"] > 0


def test_create_and_join_challenge():
    create_res = json.loads(
        create_challenge(
            title="September Marathon",
            metric="steps",
            goal=400000,
            start_date="2026-09-01",
            end_date="2026-09-30",
        )
    )
    assert create_res["status"] == "created"
    assert "september-marathon" in create_res["challenge"]["id"]

    join_res = json.loads(join_challenge(create_res["challenge"]["id"]))
    assert join_res["status"] in ("joined", "already_member")


def test_generate_badge():
    badge_res = json.loads(
        generate_badge_or_recap(
            challenge_id_or_event="august-steps-2026",
            badge_type="trophy",
            title="Step Leader Champion",
        )
    )
    assert badge_res["status"] == "generated"
    assert badge_res["badge"]["title"] == "Step Leader Champion"


def test_manage_account_settings():
    res = json.loads(
        manage_account_settings(
            display_name="Sarah J.",
            preferences="running, hiking, swimming",
            connected_devices="Garmin, Oura Ring",
        )
    )
    assert res["status"] == "success"
    assert res["display_name"] == "Sarah J."
    assert "Oura Ring" in res["connected_devices"]
