"""
Worker and work related services
"""

from abc import ABC, abstractmethod


class WorkerContract(ABC):
    """Contacts for worker"""

    @abstractmethod
    def __before_work__(self): pass

    @abstractmethod
    def __work__(self): pass

    @abstractmethod
    def __after_work__(self): pass


def handle_worker(worker: WorkerContract):
    """
    Run a WorkerContract's contracts

    :param worker: WorkerContract
    :return: bool
    """
    # try:
    worker.__before_work__()
    worker.__work__()
    worker.__after_work__()

    return True


class ProcessorContract(ABC):
    """Contacts for work processing"""

    def __initialize_process__(self):
        self.request_args = {}

    @abstractmethod
    def __before_process__(self, args): pass

    @abstractmethod
    def __process__(self): pass


def handle_processor(processor: ProcessorContract, args: dict):
    """
    Run a ProcessorContract's contracts

    :param processor: ProcessorContract
    :param args: dict[str, object]
    :return: dict
    """

    processor.__initialize_process__()
    processor.__before_process__(args)
    return processor.__process__()
