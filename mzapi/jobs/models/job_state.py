from dataclasses import dataclass
from enum import Enum


class JobStages(Enum):
    INITIAL = 0
    DOWNLOAD = 1
    CONVERTING = 2
    FINISHED = 3


@dataclass
class JobState:
    job_id: str
    stage: int
    progress: int
