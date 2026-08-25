from hottop.integrations.agent_reach import AgentReachAdapter


def test_agent_reach_builds_safe_doctor_and_install_check_commands():
    adapter = AgentReachAdapter(executable="agent-reach")
    assert adapter.doctor_command() == ["agent-reach", "doctor"]
    assert adapter.install_check_command() == ["agent-reach", "install", "--env=auto"]


def test_agent_reach_system_install_is_explicit():
    adapter = AgentReachAdapter(executable="agent-reach")
    assert adapter.install_system_command(channels=["bilibili", "twitter"]) == [
        "agent-reach",
        "install",
        "--env=auto",
        "--system",
        "--channels=bilibili,twitter",
    ]
