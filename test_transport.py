import os
import asyncio
from google.adk.context import RunContext
from travel_planner.sub_agents.transport_search.agent import transport_search_agent

async def main():
    ctx = RunContext()
    ctx.state["transport_mode"] = "avion"
    ctx.state["departure_city"] = "Montréal (YUL)"
    ctx.state["destination"] = "Paris (CDG)"
    ctx.state["travel_dates"] = "20 mai au 28 mai"
    ctx.state["budget"] = "1000 CAD"
    
    print("Execution du sous-agent Transport...")
    result = await transport_search_agent.arun("Trouve des vols", ctx)
    print("=== SORTIE BRUTE ===")
    print(ctx.state.get("transport_search_output"))
    print("====================")

if __name__ == "__main__":
    asyncio.run(main())
