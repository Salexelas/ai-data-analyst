'''from core.pipeline import Pipeline

from pipeline.steps.validation_step import ValidationStep
from pipeline.steps.language_step import LanguageStep
from pipeline.steps.intent_step import IntentStep

from pipeline.steps.schema_step import SchemaStep
from pipeline.steps.sql_generation_step import SQLGenerationStep
from pipeline.steps.execution_step import ExecutionStep
from pipeline.steps.insight_step import InsightStep

from pipeline.services.validation_service import ValidationService
#from pipeline.services.language_service import LanguageService
from pipeline.services.intent_service import IntentService

from pipeline.services.schema_service import SchemaService
from pipeline.services.sql_service import SQLService
from pipeline.services.execution_service import ExecutionService
from pipeline.services.insight_service import InsightService


class PipelineFactory:

    @staticmethod
    def build_pre_pipeline(llm):

        return Pipeline(
            [
                ValidationStep(
                    ValidationService()
                ),
                IntentStep(
                    IntentService(llm)
                ),
            ]
        )

    @staticmethod
    def build_main_pipeline(llm):

        return Pipeline(
            [
                SchemaStep(
                    SchemaService()
                ),
                SQLGenerationStep(
                    SQLService(llm)
                ),
                ExecutionStep(
                    ExecutionService()
                ),
                InsightStep(
                    InsightService(llm)
                ),
            ]
        )'''