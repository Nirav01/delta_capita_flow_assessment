from app.tasks import registry


class FlowManager:
    # Runs a JSON-defined flow like the one in the task PDF.
    def __init__(self, flow_def: dict):
        f = flow_def["flow"]
        self.flow_id = f.get("id")
        self.flow_name = f.get("name")
        self.start_task = f["start_task"]
        # conditions decide where to go next after each task
        self.conditions = f.get("conditions", [])

    def _condition_for(self, task_name: str):
        for c in self.conditions:
            if c.get("source_task") == task_name:
                return c
        return None

    def run(self, context=None):
        ctx = context or {}
        current = self.start_task
        trace = []

        while current and current != "end":
            func = registry.get(current)
            if func is None:
                trace.append({
                    "task": current,
                    "status": "failure",
                    "data": None,
                    "error": f"task '{current}' not found",
                })
                break

            try:
                data = func(ctx)
                status = "success"
                error = ""
            except Exception as e:
                data = None
                status = "failure"
                error = str(e)

            trace.append({
                "task": current,
                "status": status,
                "data": data,
                "error": error,
            })
            # store result so next tasks/conditions can read it
            ctx[current] = {
                "status": status,
                "data": data,
                "error": error,
            }
            cond = self._condition_for(current)
            if not cond:
                # no condition -> end
                break

            expected = cond.get("outcome", "success")
            if status == expected:
                current = cond.get("target_task_success", "end")
            else:
                current = cond.get("target_task_failure", "end")

        final_status = trace[-1]["status"] if trace else "unknown"

        return {
            "flow_id": self.flow_id,
            "flow_name": self.flow_name,
            "trace": trace,
            "final_status": final_status,
        }
