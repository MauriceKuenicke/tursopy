from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, List, Type, TypeVar

T = TypeVar("T")


@dataclass
class BaseDataClass:
    """
    Base dataclass implementing useful utility functionality.
    """

    def to_dict(self) -> dict[str, Any]:
        """
        Return dictionary representation.
        :return:
        """
        return asdict(self)

    @classmethod
    def load(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Load data from a dictionary into the type-hinted dataclass. Fields not in the dataclass will be ignored.
        :param data: Dictionary containing data for the dataclass.
        :return: Dataclass instance.
        """
        field_names = {f.name for f in fields(cls)}  # type:ignore [arg-type]
        reduced_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**reduced_data)


#############################################################
#                   PLATFORM API TOKENS                     #
#############################################################
@dataclass
class PlatformTokenRead(BaseDataClass):
    """
    Platform token read response model.
    """

    id: str
    name: str


@dataclass
class PlatformTokenCreated(BaseDataClass):
    """
    Platform token created response model.
    """

    id: str
    name: str
    token: str


#############################################################
#                        DATABASES                          #
#############################################################
@dataclass
class DatabaseRead(BaseDataClass):
    """
    Database read response model.
    """

    Name: str
    DbId: str
    Hostname: str
    is_schema: bool
    schema: str
    block_reads: bool
    block_writes: bool
    allow_attach: bool
    regions: List[str]
    primaryRegion: str
    type: str
    hostname: str
    version: str
    group: str
    sleeping: bool


@dataclass
class DatabaseCreated(BaseDataClass):
    """
    Database created response model.
    """

    DbId: str
    Hostname: str
    Name: str
    IssuedCertCount: int
    IssuedCertLimit: int
