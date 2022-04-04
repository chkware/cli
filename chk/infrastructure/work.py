"""
Worker and work related services
"""

from abc import ABC, abstractmethod


class Validatable(ABC):
    """Defines validation ability features """
    @abstractmethod
    def rules(self): pass

    @abstractmethod
    def validated(self): pass

    @abstractmethod
    def as_dict(self): pass


class WorkerContract(ABC):
    """Contacts for worker"""

    @abstractmethod
    def __before_work__(self): pass

    @abstractmethod
    def __work__(self): pass

    @abstractmethod
    def __after_work__(self): pass


def handle_worker(worker: WorkerContract) -> bool:
    """
    Run a WorkerContract's contracts

    :param worker: WorkerContract
    :return: bool
    """
    try:
        worker.__before_work__()
        worker.__work__()
        worker.__after_work__()
    except BaseException as ex:
        raise SystemExit("handle_worker: " + str(ex))

    return True


class ProcessorContract(ABC):
    """Contacts for work processing"""

    def __initialize_process__(self):
        self.request_args: dict[str, str] = {}

    @abstractmethod
    def __before_process__(self, args: dict[str, object]) -> None: pass

    @abstractmethod
    def __process__(self) -> dict: pass


def handle_processor(processor: ProcessorContract, args: dict[str, object]) -> dict:
    """
    Run a ProcessorContract's contracts

    :param processor: ProcessorContract
    :param args: dict[str, object]
    :return: dict
    """

    try:
        processor.__initialize_process__()
        processor.__before_process__(args)
        return processor.__process__()
    except BaseException as ex:
        raise SystemExit("handle_processor: " + str(ex))

