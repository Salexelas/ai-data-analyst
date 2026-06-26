from pipeline.pipeline_factory import (
    PipelineFactory,
)

from pipeline.response_mapper import (
    ResponseMapper,
)


def run_pre_pipeline(
    ctx,
    llm,
):

    return (
        PipelineFactory
        .build_pre_pipeline(llm)
        .run(ctx)
    )


def run_main_pipeline(
    ctx,
    llm,
):

    ctx = (
        PipelineFactory
        .build_main_pipeline(llm)
        .run(ctx)
    )

    return (
        ResponseMapper
        .from_context(ctx)
    )