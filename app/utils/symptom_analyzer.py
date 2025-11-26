
# lightweight helper — you can expand rules or load JSON rule files for bike/scooty
def symptom_analyzer(text: str):
    text = text.lower()
    results = []
    if 'brake' in text:
        results.append(('brake_issue', 0.9, 'brake noise or reduced efficiency'))
    if 'overheat' in text or 'hot' in text or 'temperature' in text:
        results.append(('overheat', 0.8, 'engine temperature rise'))
    if not results:
        results.append(('unknown', 0.3, 'needs inspection'))
    return results
