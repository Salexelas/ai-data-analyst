class Step:
    name = "base"

    def run(self, ctx):
        raise NotImplementedError


class Pipeline:

    def __init__(self, steps):
        self.steps = steps

    def run(self, ctx):
        for step in self.steps:
            print(f"[STEP] {step.name}")

            step.run(ctx)

            print(f"[CTX] sql={ctx.exec.sql} | rows={len(ctx.output.result) if ctx.output.result is not None else None}")
        
        return ctx