"""In-memory and persistent data store for FitFriends Challenge Hub."""

from datetime import datetime, date
import math


class FitFriendsStore:
    def __init__(self):
        self.users = {
            "current_user": {
                "id": "current_user",
                "name": "Sarah",
                "display_name": "Sarah Jenkins",
                "connected_devices": ["Garmin Forerunner 955", "Google Health Connect"],
                "activity_preferences": ["running", "hiking", "swimming", "cycling", "yoga"],
                "roles": {"august-steps-2026": "admin", "weekly-cycle-sprint": "owner"},
                "daily_metrics": {
                    "2026-08-14": {"steps": 10000, "sleep_hours": 7.5, "active_hours": 1.5, "calories": 2200},
                },
            },
            "alex": {
                "id": "alex",
                "name": "Alex",
                "display_name": "Alex Rivera",
                "connected_devices": ["Apple Watch Series 9"],
                "activity_preferences": ["running", "cycling", "gym workouts"],
                "roles": {"august-steps-2026": "owner"},
            },
            "jordan": {
                "id": "jordan",
                "name": "Jordan",
                "display_name": "Jordan Lee",
                "connected_devices": ["Garmin Venu 3"],
                "activity_preferences": ["hiking", "gym workouts", "yoga"],
                "roles": {"august-steps-2026": "member"},
            },
            "taylor": {
                "id": "taylor",
                "name": "Taylor",
                "display_name": "Taylor Smith",
                "connected_devices": ["Fitbit Charge 6"],
                "activity_preferences": ["swimming", "running"],
                "roles": {"august-steps-2026": "member"},
            },
        }

        self.challenges = {
            "august-steps-2026": {
                "id": "august-steps-2026",
                "title": "August Steps Challenge",
                "description": "Monthly steps competition among friends to maintain top daily activity all August!",
                "metric": "steps",
                "goal": 300000,
                "start_date": "2026-08-01",
                "end_date": "2026-08-31",
                "is_private": False,
                "invite_url": "https://fitfriends.app/join/august-steps-2026",
                "members": {
                    "alex": {"role": "owner", "total_metric": 168000, "daily_avg": 12000},
                    "current_user": {"role": "admin", "total_metric": 140000, "daily_avg": 10000},
                    "jordan": {"role": "member", "total_metric": 126000, "daily_avg": 9000},
                    "taylor": {"role": "member", "total_metric": 112000, "daily_avg": 8000},
                },
            },
            "weekly-cycle-sprint": {
                "id": "weekly-cycle-sprint",
                "title": "Weekly Cycling Sprint",
                "description": "High-intensity cycling calorie blast challenge for the week.",
                "metric": "calories",
                "goal": 10000,
                "start_date": "2026-08-10",
                "end_date": "2026-08-17",
                "is_private": True,
                "invite_url": "https://fitfriends.app/join/weekly-cycle-sprint?code=CYCLE50",
                "members": {
                    "current_user": {"role": "owner", "total_metric": 8400, "daily_avg": 2100},
                    "alex": {"role": "member", "total_metric": 7200, "daily_avg": 1800},
                },
            },
        }

        self.badges = []

    def get_user_profile(self, user_id: str = "current_user") -> dict:
        user = self.users.get(user_id, self.users["current_user"])
        # Calculate summary metrics
        active_challenges = [
            c["title"] for c in self.challenges.values() if user["id"] in c["members"]
        ]
        return {
            "user_id": user["id"],
            "display_name": user.get("display_name", user["name"]),
            "connected_devices": user.get("connected_devices", []),
            "activity_preferences": user.get("activity_preferences", []),
            "active_challenges": active_challenges,
            "daily_metric_trends": user.get("daily_metrics", {}),
        }

    def sync_metrics(
        self,
        user_id: str = "current_user",
        steps: int = 0,
        sleep_hours: float = 0.0,
        active_hours: float = 0.0,
        calories: int = 0,
        date_str: str = None,
    ) -> dict:
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        user = self.users.get(user_id, self.users["current_user"])
        if "daily_metrics" not in user:
            user["daily_metrics"] = {}

        current_log = user["daily_metrics"].get(
            date_str, {"steps": 0, "sleep_hours": 0.0, "active_hours": 0.0, "calories": 0}
        )

        if steps > 0:
            diff = steps - current_log["steps"]
            current_log["steps"] = steps
            # Update active challenges for steps
            for ch in self.challenges.values():
                if ch["metric"] == "steps" and user["id"] in ch["members"]:
                    ch["members"][user["id"]]["total_metric"] += max(0, diff)

        if sleep_hours > 0:
            current_log["sleep_hours"] = sleep_hours

        if active_hours > 0:
            current_log["active_hours"] = active_hours

        if calories > 0:
            diff = calories - current_log["calories"]
            current_log["calories"] = calories
            for ch in self.challenges.values():
                if ch["metric"] == "calories" and user["id"] in ch["members"]:
                    ch["members"][user["id"]]["total_metric"] += max(0, diff)

        user["daily_metrics"][date_str] = current_log
        return {
            "status": "success",
            "date": date_str,
            "synced_metrics": current_log,
            "message": f"Health metrics synced for {user.get('display_name', user_id)}.",
        }

    def update_user_settings(
        self,
        user_id: str = "current_user",
        display_name: str = None,
        preferences: list[str] = None,
        connected_devices: list[str] = None,
    ) -> dict:
        user = self.users.get(user_id, self.users["current_user"])
        if display_name:
            user["display_name"] = display_name
        if preferences:
            user["activity_preferences"] = preferences
        if connected_devices:
            user["connected_devices"] = connected_devices

        return {
            "status": "success",
            "user_id": user["id"],
            "display_name": user.get("display_name"),
            "connected_devices": user.get("connected_devices"),
            "activity_preferences": user.get("activity_preferences"),
        }

    def create_challenge(
        self,
        title: str,
        metric: str,
        goal: int,
        start_date: str,
        end_date: str,
        is_private: bool = False,
        description: str = "",
        owner_id: str = "current_user",
    ) -> dict:
        ch_id = title.lower().replace(" ", "-") + "-" + datetime.now().strftime("%M%S")
        owner = self.users.get(owner_id, self.users["current_user"])
        invite_url = f"https://fitfriends.app/join/{ch_id}"

        new_ch = {
            "id": ch_id,
            "title": title,
            "description": description or f"{title} competition",
            "metric": metric.lower(),
            "goal": goal,
            "start_date": start_date,
            "end_date": end_date,
            "is_private": is_private,
            "invite_url": invite_url,
            "members": {
                owner["id"]: {"role": "owner", "total_metric": 0, "daily_avg": 0}
            },
        }

        self.challenges[ch_id] = new_ch
        owner.setdefault("roles", {})[ch_id] = "owner"

        return {
            "status": "created",
            "challenge": new_ch,
            "invite_url": invite_url,
            "message": f"Challenge '{title}' created successfully! Share this link to invite friends: {invite_url}",
        }

    def join_challenge(self, challenge_id_or_invite: str, user_id: str = "current_user") -> dict:
        # Match challenge_id
        target_ch = None
        for cid, ch in self.challenges.items():
            if cid in challenge_id_or_invite or ch["invite_url"] in challenge_id_or_invite:
                target_ch = ch
                break

        if not target_ch:
            # Try searching by title
            for ch in self.challenges.values():
                if challenge_id_or_invite.lower() in ch["title"].lower():
                    target_ch = ch
                    break

        if not target_ch:
            return {"status": "error", "message": f"Challenge '{challenge_id_or_invite}' not found."}

        user = self.users.get(user_id, self.users["current_user"])
        if user["id"] in target_ch["members"]:
            return {
                "status": "already_member",
                "challenge": target_ch,
                "message": f"You are already a member of '{target_ch['title']}'.",
            }

        target_ch["members"][user["id"]] = {"role": "member", "total_metric": 0, "daily_avg": 0}
        user.setdefault("roles", {})[target_ch["id"]] = "member"

        return {
            "status": "joined",
            "challenge_id": target_ch["id"],
            "title": target_ch["title"],
            "message": f"Successfully joined '{target_ch['title']}'! Welcome aboard.",
        }

    def get_challenge_details(self, challenge_id: str) -> dict:
        ch = self._find_challenge(challenge_id)
        if not ch:
            return {"status": "error", "message": f"Challenge '{challenge_id}' not found."}

        roster = []
        for uid, member in ch["members"].items():
            u_info = self.users.get(uid, {"display_name": uid})
            roster.append({
                "user_id": uid,
                "name": u_info.get("display_name", u_info.get("name")),
                "role": member["role"],
                "total_metric": member["total_metric"],
            })

        return {
            "id": ch["id"],
            "title": ch["title"],
            "description": ch["description"],
            "metric": ch["metric"],
            "goal": ch["goal"],
            "start_date": ch["start_date"],
            "end_date": ch["end_date"],
            "is_private": ch["is_private"],
            "invite_url": ch["invite_url"],
            "total_participants": len(ch["members"]),
            "participant_roster": roster,
        }

    def get_leaderboard(self, challenge_id: str) -> dict:
        ch = self._find_challenge(challenge_id)
        if not ch:
            return {"status": "error", "message": f"Challenge '{challenge_id}' not found."}

        # Sort members by total_metric desc
        sorted_members = sorted(
            ch["members"].items(),
            key=lambda item: item[1]["total_metric"],
            reverse=True,
        )

        leaderboard = []
        top_score = sorted_members[0][1]["total_metric"] if sorted_members else 0

        for rank, (uid, data) in enumerate(sorted_members, 1):
            u_info = self.users.get(uid, {"display_name": uid})
            total = data["total_metric"]
            gap_to_1st = top_score - total
            completion_pct = round((total / ch["goal"]) * 100, 1) if ch["goal"] > 0 else 100.0

            leaderboard.append({
                "rank": rank,
                "user_id": uid,
                "name": u_info.get("display_name", u_info.get("name")),
                "total_metric": total,
                "daily_avg": data["daily_avg"],
                "gap_to_1st": gap_to_1st,
                "completion_pct": f"{completion_pct}%",
                "role": data["role"],
            })

        return {
            "challenge_id": ch["id"],
            "title": ch["title"],
            "metric": ch["metric"],
            "goal": ch["goal"],
            "leaderboard": leaderboard,
        }

    def calculate_leaderboard_stats(
        self, challenge_id: str, user_id: str = "current_user", custom_handicap: float = 1.0
    ) -> dict:
        ch = self._find_challenge(challenge_id)
        if not ch:
            return {"status": "error", "message": f"Challenge '{challenge_id}' not found."}

        leaderboard_data = self.get_leaderboard(ch["id"])
        lb = leaderboard_data["leaderboard"]

        user_entry = None
        first_place_entry = lb[0] if lb else None

        for entry in lb:
            if entry["user_id"] == user_id or user_id.lower() in entry["name"].lower():
                user_entry = entry
                break

        if not user_entry:
            user_entry = lb[1] if len(lb) > 1 else lb[0]

        # Calculate time remaining
        try:
            today = date(2026, 8, 14)  # Fixed reference date from brief
            end = datetime.strptime(ch["end_date"], "%Y-%m-%d").date()
            start = datetime.strptime(ch["start_date"], "%Y-%m-%d").date()

            days_passed = max(1, (today - start).days + 1)
            days_remaining = max(1, (end - today).days)
            total_days = (end - start).days + 1
        except Exception:
            days_passed = 14
            days_remaining = 17
            total_days = 31

        first_total = first_place_entry["total_metric"] if first_place_entry else 0
        first_daily_pace = first_place_entry["daily_avg"] if first_place_entry else 12000

        user_total = user_entry["total_metric"]
        user_rank = user_entry["rank"]
        current_gap = max(0, first_total - user_total)

        # Projected 1st place score at end of challenge
        projected_first_final = first_total + (first_daily_pace * days_remaining)

        # Needed total steps for user to match 1st place
        needed_user_total = projected_first_final
        needed_remaining_steps = needed_user_total - user_total
        daily_steps_needed_to_win = math.ceil(needed_remaining_steps / days_remaining)

        # Handicap adjustment
        adjusted_user_total = int(user_total * custom_handicap)
        completion_pct = round((user_total / ch["goal"]) * 100, 1)

        return {
            "challenge_title": ch["title"],
            "metric": ch["metric"],
            "current_user_rank": user_rank,
            "total_participants": len(lb),
            "user_current_total": user_total,
            "first_place_user": first_place_entry["name"] if first_place_entry else "N/A",
            "first_place_total": first_total,
            "current_gap_to_1st": current_gap,
            "days_passed": days_passed,
            "days_remaining": days_remaining,
            "total_challenge_days": total_days,
            "first_place_daily_pace": first_daily_pace,
            "projected_1st_place_finish": projected_first_final,
            "daily_metric_needed_to_catch_up": daily_steps_needed_to_win,
            "handicap_multiplier": custom_handicap,
            "handicap_adjusted_score": adjusted_user_total,
            "completion_percentage": f"{completion_pct}%",
            "summary_formula": (
                f"To pass {first_place_entry['name']} (Rank 1, {first_total:,} {ch['metric']}), "
                f"who is on pace for {projected_first_final:,} total {ch['metric']}, you need {daily_steps_needed_to_win:,} "
                f"daily {ch['metric']} over the remaining {days_remaining} days."
            ),
        }

    def generate_badge(
        self, challenge_id_or_event: str, badge_type: str = "achievement", title: str = "Challenge Hero", user_id: str = "current_user"
    ) -> dict:
        badge_id = f"badge-{len(self.badges) + 1}"
        u_info = self.users.get(user_id, self.users["current_user"])
        user_name = u_info.get("display_name", u_info.get("name"))

        badge = {
            "badge_id": badge_id,
            "badge_type": badge_type,
            "title": title,
            "recipient": user_name,
            "challenge_or_event": challenge_id_or_event,
            "unlocked_date": datetime.now().strftime("%Y-%m-%d"),
            "image_url": f"https://fitfriends.app/assets/badges/{badge_id}.png",
            "description": f"Awarded to {user_name} for outstanding performance in {challenge_id_or_event}!",
        }
        self.badges.append(badge)
        return {
            "status": "generated",
            "badge": badge,
            "message": f"Personalized {badge_type} badge '{title}' generated for {user_name}!",
        }

    def _find_challenge(self, query: str) -> dict | None:
        if query in self.challenges:
            return self.challenges[query]
        for ch in self.challenges.values():
            if query.lower() in ch["id"].lower() or query.lower() in ch["title"].lower():
                return ch
        return None


# Global instance
store = FitFriendsStore()
