
def test_simple_chat():
    # basic sanity test - import the agent and ensure text response
    from backend.agent.scheduling_agent import SchedulingAgent
    a = SchedulingAgent()
    r = a.handle("I want to book an appointment", {})
    assert r['type'] == 'booking_start'
