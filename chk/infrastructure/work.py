"""
Worker and work related services
"""
from abc import ABC, abstractmethod


class WorkerContract(ABC):
    """Contacts for worker"""

    @abstractmethod
    def __before_main__(self) -> None:
        pass

    @abstractmethod
    def __main__(self) -> None:
        pass

    @abstractmethod
    def __after_main__(self) -> object:
        pass

    def __work__(self) -> object:
        self.__before_main__()
        self.__main__()
        return self.__after_main__()


def handle_worker(worker: WorkerContract) -> object:
    """
    Run a WorkerContract's contracts

    :param worker: WorkerContract
    :return: bool
    """
    # try:
    return worker.__work__()


class RequestProcessorContract(ABC):
    """Contacts for work processing"""

    def __initialize_process__(self):
        self.request_args = {}

    @abstractmethod
    def __before_process__(self, args): pass

    @abstractmethod
    def __process__(self): pass


def handle_request(processor: RequestProcessorContract, args: dict):
    """
    Run a RequestProcessorContract's contracts

    :param processor: RequestProcessorContract
    :param args: dict[str, object]
    :return: dict
    """

    processor.__initialize_process__()
    processor.__before_process__(args)
    return processor.__process__()
