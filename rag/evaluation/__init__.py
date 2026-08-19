"""
rag/evaluation/__init__.py

RAG Evaluation Framework for HAI-SOC.
"""

from rag.evaluation.evaluator import RAGEvaluator, RAGEvalResult
from rag.evaluation.test_cases import EVAL_TEST_CASES, RAGEvalTestCase, RAGEvalExpected

__all__ = [
    "RAGEvaluator",
    "RAGEvalResult",
    "EVAL_TEST_CASES",
    "RAGEvalTestCase",
    "RAGEvalExpected",
]
