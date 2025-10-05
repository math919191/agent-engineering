import asyncio

from agents import get_completion, Agent, AgentSettings

import markdowndata

from enum import Enum

class TIERS(Enum):
    BASELINE = "Baseline"
    CORE = "Core"
    STRETCH_1 = "Stretch 1"
    STRETCH_2 = "Stretch 2"

def get_report_tier(report_contents, tier_name: TIERS):
    full_report = markdowndata.loads(report_contents)
    student_data_responses = next(iter(full_report.values()))
    return student_data_responses[tier_name.value]

def get_rubric_tier(rubric_contents, tier_name: TIERS):
    data = markdowndata.loads(rubric_contents)
    return data[tier_name.value]


async def grade_tier(client, agent, tier_name: TIERS, report_contents: str, rubric_contents):
    """This function takes in the following parameters:
    - tier_name: this is the name of the tier to grade
    - report_contents: the contents of the report as a string
    Returns feedback about the requested function and its complexity
    """

    student_report_for_tier = get_report_tier(report_contents, tier_name)
    rubric_for_tier = get_rubric_tier(rubric_contents, tier_name)

    input = {"report_contents": student_report_for_tier,
             "rubric": rubric_for_tier}

    response = await get_completion(client, agent, input=input)

    return response

async def grade_all_tiers(client, agent, report_contents: str, rubric_contents):

    full_response = ""
    for tier_name in TIERS:
        response = await grade_tier(client, agent, tier_name, report_contents, rubric_contents)
        response += ("\n\n ##" + tier_name.value)
        response += full_response

    return full_response