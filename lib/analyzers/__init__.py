from typing import Type

from .base_analyzer import BaseAnalyzer
from .quality_analyzer import QualityAnalyzer
from .text_analyzer import TextAnalyzer
from .transcript_analyzer import TranscriptAnalyzer
from .video_analyzer import VideoAnalyzer

AllAnalyzers: list[Type[BaseAnalyzer]] = [
    TextAnalyzer,
    VideoAnalyzer,
    TranscriptAnalyzer,
    QualityAnalyzer,
]
