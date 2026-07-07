from abc import ABC, abstractmethod
from .register_file import RegisterFile
from .calling_convention import CallingConvention
from .instruction_set import InstructionSet
from .stack_model import StackModel
from .data_layout import DataLayout

class TargetBackend(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Target name (e.g., 'x86_64-linux-gnu')."""
        pass
        
    @property
    @abstractmethod
    def architecture(self) -> str:
        """e.g., 'x86_64', 'aarch64'."""
        pass
        
    @property
    @abstractmethod
    def operating_system(self) -> str:
        """e.g., 'linux', 'windows', 'macos'."""
        pass
        
    @property
    @abstractmethod
    def abi_name(self) -> str:
        """e.g., 'sysv', 'win64'."""
        pass
        
    @property
    @abstractmethod
    def pointer_size(self) -> int:
        """Pointer size in bytes."""
        pass
        
    @property
    @abstractmethod
    def endianness(self) -> str:
        """'little' or 'big'."""
        pass

    @abstractmethod
    def register_file(self) -> RegisterFile:
        pass

    @abstractmethod
    def calling_convention(self) -> CallingConvention:
        pass

    @abstractmethod
    def instruction_set(self) -> InstructionSet:
        pass

    @abstractmethod
    def stack_model(self) -> StackModel:
        pass

    @abstractmethod
    def data_layout(self) -> DataLayout:
        pass
