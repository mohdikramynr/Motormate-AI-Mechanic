
class CommunicationAgent:
    """Extracts vehicle type (bike / scooty) and returns structured problem.
    This is a simple rule-based extractor; you can replace with an LLM-powered NLU later.
    """
    def interact(self, user_message: str):
        msg = user_message.lower()
        # heuristics to detect scooty
        scooty_keywords = ['scooty', 'scooter', 'activa', 'dio', 'fascino']
        bike_keywords = ['bike', 'motorcycle', 'pulsar', 'royal enfield', 'honda cb']

        vehicle = 'bike'
        for k in scooty_keywords:
            if k in msg:
                vehicle = 'scooty'
                break
        # simple override: if user explicitly says bike
        for k in bike_keywords:
            if k in msg:
                vehicle = 'bike'
                break

        # try short normalization
        problem = user_message.strip()

        return {
            "vehicle_type": vehicle,
            "problem": problem
        }
