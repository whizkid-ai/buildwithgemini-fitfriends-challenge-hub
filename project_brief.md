# My agent: FitFriends Challenge Hub
One-liner: A conversational health and fitness agent that helps friends create, join, and compete in friendly weekly/monthly fitness challenges with live leaderboards, activity tracking, and AI coaching.

Tool coverage:
- Memory: User's connected health profiles (Garmin/Google Health metrics), activity preferences (running, hiking, swimming, cycling, gym workouts, yoga), active/past challenges, and daily metric trends (steps, sleep, activity hours, calories).
- Tools: Sync health metrics (steps, sleep, active hours, calories), create/join/manage public and private challenges, invite members via shareable URLs, update roles (owner/admin/member), and manage account settings.
- Catalog/UI: Interactive challenge cards, real-time leaderboard tables, participant rosters, and metric breakdown charts.
- Image gen: Personalized achievement badges, milestone trophy images, and weekly challenge recap banners.
- Sandbox: Calculating custom leaderboard scoring formulas, handicap adjustments, and metric completion percentages.

Core rails (everyone): memory, tools, eval, deploy, frontend
My stretch menu (pick later): A2UI card renders for leaderboards & challenge invites, AI badge image generation, sandbox scoring calculations
First eval question: "What is my current ranking in the August Steps Challenge, and how many daily steps do I need to catch up to 1st place?"
