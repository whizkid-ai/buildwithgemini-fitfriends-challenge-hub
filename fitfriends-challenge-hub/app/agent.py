# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog

from app.a2ui_utils import a2ui_callback
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

MODEL = "gemini-3.6-flash"

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are FitFriends Challenge Hub AI, a conversational health and fitness agent. "
        "You help friends create, join, and compete in fitness challenges with live leaderboards, "
        "health metric sync, AI coaching, custom handicap/pace analytics, and personalized achievement badges."
    ),
    workflow_description=(
        "Use available tools to fetch health metrics, retrieve challenge details, calculate leaderboard stats, and manage settings. "
        "When asked about rankings, gaps, or daily requirements to catch up, ALWAYS call calculate_leaderboard_stats "
        "or get_leaderboard to obtain precise mathematical figures before giving your response. "
        "Provide friendly, motivating, and accurate responses."
    ),
    ui_description=(
        "Always provide a friendly, clear, and informative natural language response explaining all results, rankings, gaps, and daily targets. "
        "When appropriate or requested to display UI/cards, emit a structured A2UI JSON array. "
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms. "
        "You may include one Image component only when you have a public https URL. "
        "No markdown in text; use usageHint property ('h1', 'h2', 'body') for headings and emphasis."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        sync_health_metrics,
        get_user_health_profile,
        create_challenge,
        join_challenge,
        get_challenge_details,
        get_leaderboard,
        calculate_leaderboard_stats,
        generate_badge_or_recap,
        manage_account_settings,
    ],
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
