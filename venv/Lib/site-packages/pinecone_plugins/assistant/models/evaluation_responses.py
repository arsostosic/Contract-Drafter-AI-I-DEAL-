from dataclasses import dataclass
from typing import List
from pinecone_plugins.assistant.evaluation.core.client.model.alignment_response import AlignmentResponse as OpenAPIAlignmentResponse
from pinecone_plugins.assistant.evaluation.core.client.model.metrics import Metrics as OpenAPIMetrics
from pinecone_plugins.assistant.evaluation.core.client.model.reasoning import Reasoning as OpenAPIReasoning
from pinecone_plugins.assistant.evaluation.core.client.model.token_counts import TokenCounts as OpenAPITokenCounts
from pinecone_plugins.assistant.evaluation.core.client.model.evaluated_fact import EvaluatedFact as OpenAPIEvaluatedFact
from pinecone_plugins.assistant.evaluation.core.client.model.fact import Fact as OpenAPIFact


@dataclass
class Fact:
    content: str

    @classmethod
    def from_openapi(cls, fact: OpenAPIFact):
        return cls(content=fact.content)


@dataclass
class EvaluatedFact:
    fact: Fact
    entailment: str

    @classmethod
    def from_openapi(cls, evaluated_fact: OpenAPIEvaluatedFact):
        return cls(
            fact=Fact.from_openapi(evaluated_fact.fact),
            entailment=evaluated_fact.entailment.value
        )


@dataclass
class Reasoning:
    evaluated_facts: List[EvaluatedFact]

    @classmethod
    def from_openapi(cls, reasoning: OpenAPIReasoning):
        return cls(
            evaluated_facts=[EvaluatedFact.from_openapi(fact) for fact in reasoning.evaluated_facts]
        )


@dataclass
class Metrics:
    correctness: float
    completeness: float
    alignment: float

    @classmethod
    def from_openapi(cls, metrics: OpenAPIMetrics):
        return cls(
            correctness=metrics.correctness,
            completeness=metrics.completeness,
            alignment=metrics.alignment
        )


@dataclass
class TokenCounts:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @classmethod
    def from_openapi(cls, token_counts: OpenAPITokenCounts):
        return cls(
            prompt_tokens=token_counts.prompt_tokens,
            completion_tokens=token_counts.completion_tokens,
            total_tokens=token_counts.total_tokens
        )


@dataclass
class AlignmentResponse:
    metrics: Metrics
    reasoning: Reasoning
    usage: TokenCounts

    @classmethod
    def from_openapi(cls, alignment_response: OpenAPIAlignmentResponse):
        return cls(
            metrics=Metrics.from_openapi(alignment_response.metrics),
            reasoning=Reasoning.from_openapi(alignment_response.reasoning),
            usage=TokenCounts.from_openapi(alignment_response.usage)
        )
