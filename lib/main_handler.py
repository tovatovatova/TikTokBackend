from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from lib.analyzers import AllAnalyzers
from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section, Status
from lib.user_config import UserConfig


def get_final_results(file_path: Path, user_config: UserConfig) -> list[Section]:
    final_results: list[Section] = []
    analyzers = [Analyzer(user_config) for Analyzer in AllAnalyzers]
    with ThreadPoolExecutor(max_workers=len(analyzers)) as executor:

        def analyze(analyzer: BaseAnalyzer) -> list[Section]:
            assert analyzer.SectionType is not None
            try:
                return analyzer.analyze(file_path)
            except Exception as e:
                print(e)
                return [
                    Section(
                        0,
                        0,
                        f"unknown error",
                        analyzer.SectionType,
                        status=Status.error,
                        error=e,
                    )
                ]

        final_results = [
            section
            for sections in executor.map(analyze, analyzers)
            for section in sections
        ]

    return final_results


if __name__ == "__main__":
    get_final_results(Path("./frames/test-20.mp4"), UserConfig("en", "tiktok"))
