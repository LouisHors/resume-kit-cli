import unittest

from resume_kit.profiles import get_profile, list_profiles


class ProfileTests(unittest.TestCase):
    def test_profiles_exist(self):
        names = [profile.name for profile in list_profiles()]
        self.assertEqual(names, ["ai-agent", "solution-expert", "ios"])

    def test_ai_agent_prioritizes_agent_materials(self):
        profile = get_profile("ai-agent")
        self.assertIn("agent-workflow", profile.priority_skill_tags)
        self.assertIn("Horspowers", profile.preferred_projects)
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", profile.preferred_projects)
