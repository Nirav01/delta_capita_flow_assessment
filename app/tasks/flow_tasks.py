def task1(context: dict):
    # Fetch data
    data = {"items": [1, 2, 3]}
    return {"fetched": data}


def task2(context: dict):
    # Process data using the output of task1
    t1 = context.get("task1", {})
    fetched = t1.get("data", {}).get("fetched", {})
    items = fetched.get("items", [])
    processed = [x * 10 for x in items]
    return {"processed": processed}


def task3(context: dict):
    # Store processed data
    t2 = context.get("task2", {})
    processed = t2.get("data", {}).get("processed", [])
    return {"stored_count": len(processed)}
