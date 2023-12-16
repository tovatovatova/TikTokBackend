from lib.analyzers import AllAnalyzers
from lib.section import Section
from lib.user_config import UserConfig


def get_final_results(file_path: str, user_config: UserConfig) -> list[Section]:
    final_results: list[Section] = []
    for Analyzer in AllAnalyzers:
        analyzer = Analyzer(file_path, user_config)
        final_results += analyzer.analyze()

    return final_results
