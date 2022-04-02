"""
Worker and work related services
"""

from abc import ABC, abstractmethod


class WorkerContract(ABC):
    """Contacts for worker"""

    def __before_work__(self) -> None: pass

    @abstractmethod
    def __work__(self) -> None:
        pass

    def __after_work__(self): pass


def handle_worker(worker: WorkerContract) -> bool:
    try:
        worker.__before_work__()
        worker.__work__()
        worker.__after_work__()
    except BaseException as ex:
        raise SystemExit(str(ex))

    return True
