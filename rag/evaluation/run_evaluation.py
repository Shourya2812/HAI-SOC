"""
rag/evaluation/run_evaluation.py

Runs controlled HAI-SOC RAG evaluation test cases
against the existing RAG incident analysis pipeline.

The evaluation uses mock_source_log from each test case
instead of MongoDB so that every test is deterministic.

Usage:

    python -m rag.evaluation.run_evaluation --test TEST-01

    python -m rag.evaluation.run_evaluation --test TEST-04

    python -m rag.evaluation.run_evaluation --all
"""

import argparse
import sys
import time

from rag.generator import analyze_incident
from rag.evaluation.test_cases import EVAL_TEST_CASES
from rag.evaluation.evaluator import RAGEvaluator


def get_test_case(test_id: str):
    """
    Find an evaluation test case by ID.
    """

    for test_case in EVAL_TEST_CASES:
        if test_case.id.upper() == test_id.upper():
            return test_case

    return None


def print_incident(incident: dict):
    """
    Print the controlled incident metadata.
    """

    print("\n## Incident:")
    print("-" * 80)

    for key, value in incident.items():
        print(f"{key}: {value}")


def print_source_log(source_log: dict):
    """
    Print the authoritative mock source log used for evaluation.
    """

    print("\n## Authoritative Test Source Log:")
    print("-" * 80)

    for key, value in source_log.items():
        print(f"{key}: {value}")


def run_single_test(
    test_case,
    evaluator: RAGEvaluator,
):
    """
    Execute one controlled RAG evaluation test.
    """

    print("\n" + "=" * 80)
    print("HAI-SOC RAG EVALUATION")
    print("=" * 80)

    print(f"Test ID     : {test_case.id}")
    print(f"Test Name   : {test_case.name}")
    print(f"Description : {test_case.description}")

    print_incident(test_case.incident)

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Evaluation MUST use the controlled mock source log.
    #
    # Do NOT allow generator.py to query MongoDB for test cases.
    # --------------------------------------------------------

    source_log = test_case.mock_source_log

    print_source_log(source_log)

    print("\n## Generating RAG response...")
    print("-" * 80)

    generation_start = time.perf_counter()

    try:

        report = analyze_incident(
            incident=test_case.incident,
            source_log=source_log,
        )

    except Exception as exc:

        generation_time = time.perf_counter() - generation_start

        print("\n❌ RAG GENERATION FAILED")
        print(f"Error: {exc}")
        print(f"Generation time: {generation_time:.2f} seconds")

        return None

    generation_time = time.perf_counter() - generation_start

    print(
        f"\nGeneration completed in "
        f"{generation_time:.2f} seconds."
    )

    print("\n# Generated Report:")
    print("=" * 80)
    print(report)
    print("=" * 80)

    # --------------------------------------------------------
    # Evaluate the generated report
    # --------------------------------------------------------

    print("\n## Evaluating generated report...")
    print("-" * 80)

    evaluation_start = time.perf_counter()

    result = evaluator.evaluate(
        test_case=test_case,
        report_text=report,
    )

    evaluation_time = time.perf_counter() - evaluation_start

    print(
        f"\nEvaluation completed in "
        f"{evaluation_time:.4f} seconds."
    )

    evaluator.print_result(result)

    print("\n## Timing")
    print("-" * 80)
    print(f"Generation time : {generation_time:.2f} seconds")
    print(f"Evaluation time : {evaluation_time:.4f} seconds")
    print(
        f"Total time      : "
        f"{generation_time + evaluation_time:.2f} seconds"
    )

    return result


def run_all_tests(evaluator: RAGEvaluator):
    """
    Run all controlled evaluation test cases.
    """

    print("\n" + "=" * 80)
    print("HAI-SOC RAG EVALUATION SUITE")
    print("=" * 80)

    print(
        f"Total test cases: "
        f"{len(EVAL_TEST_CASES)}"
    )

    results = []

    for index, test_case in enumerate(
        EVAL_TEST_CASES,
        start=1,
    ):

        print("\n")
        print("#" * 80)
        print(
            f"TEST {index}/"
            f"{len(EVAL_TEST_CASES)}"
        )
        print("#" * 80)

        result = run_single_test(
            test_case=test_case,
            evaluator=evaluator,
        )

        if result is not None:
            results.append(result)

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n")
    print("=" * 80)
    print("FINAL RAG EVALUATION SUMMARY")
    print("=" * 80)

    if not results:

        print("No tests completed successfully.")
        return

    passed = 0
    failed = 0

    for result in results:

        if result.passed:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1

        print(
            f"{result.test_case_id:<10}"
            f"{status:<8}"
            f"{result.overall_score * 100:>6.1f}%"
            f"   {result.test_case_name}"
        )

    print("-" * 80)

    average_score = (
        sum(
            result.overall_score
            for result in results
        )
        / len(results)
    )

    print(
        f"Passed        : "
        f"{passed}/{len(results)}"
    )

    print(
        f"Failed        : "
        f"{failed}/{len(results)}"
    )

    print(
        f"Average Score : "
        f"{average_score * 100:.1f}%"
    )

    print("=" * 80)


def main():
    """
    CLI entry point.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the HAI-SOC RAG "
            "incident analysis pipeline."
        )
    )

    group = parser.add_mutually_exclusive_group(
        required=True
    )

    group.add_argument(
        "--test",
        type=str,
        help="Run one test case, e.g. TEST-01",
    )

    group.add_argument(
        "--all",
        action="store_true",
        help="Run all evaluation test cases",
    )

    args = parser.parse_args()

    evaluator = RAGEvaluator()

    # --------------------------------------------------------
    # Single test
    # --------------------------------------------------------

    if args.test:

        test_case = get_test_case(
            args.test
        )

        if test_case is None:

            print(
                f"\n❌ Unknown test case: "
                f"{args.test}"
            )

            print(
                "\nAvailable test cases:"
            )

            for case in EVAL_TEST_CASES:

                print(
                    f"  {case.id:<10}"
                    f"{case.name}"
                )

            sys.exit(1)

        result = run_single_test(
            test_case=test_case,
            evaluator=evaluator,
        )

        if result is None:
            sys.exit(1)

        return

    # --------------------------------------------------------
    # All tests
    # --------------------------------------------------------

    if args.all:

        run_all_tests(
            evaluator=evaluator
        )


if __name__ == "__main__":
    main()