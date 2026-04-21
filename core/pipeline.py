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

            print(f"[CTX] sql={getattr(ctx, 'sql', None)} | rows={len(ctx.result) if getattr(ctx, 'result', None) is not None else None}")
        
        return ctx