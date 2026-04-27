from core.observability import log_event
import time

class Step:
    name = "base"

    def run(self, ctx):
        raise NotImplementedError


class Pipeline:

    def __init__(self, steps):
        self.steps = steps

    def run(self, ctx):
        for step in self.steps:
            start = time.time()

            log_event(
                "step_start",
                ctx.trace_id,
                step=step.name
            )

            try:
                step.run(ctx)

                duration = time.time() - start

                log_event(
                    "step_success",
                    ctx.trace_id,
                    step=step.name,
                    duration=duration
                )

            except Exception as e:
                duration = time.time() - start

                log_event(
                    "step_error",
                    ctx.trace_id,
                    step=step.name,
                    duration=duration,
                    error=str(e)
                )

                raise

        return ctx