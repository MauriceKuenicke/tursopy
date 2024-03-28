from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, List, Optional, Type, TypeVar

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
    version: str
    group: str
    sleeping: bool
    hostname: str


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


@dataclass
class ConfigUpdateResponse(BaseDataClass):
    """
    Response model for database config updates.
    """

    allow_attach: Optional[bool] = None
    size_limit: Optional[str] = None


@dataclass
class Usage(BaseDataClass):
    """
    Raw usage data.
    """

    rows_read: int
    rows_written: int
    storage_byte: int


@dataclass
class SingleDBUsage(BaseDataClass):
    """
    Usage statistics for a single database.
    """

    uuid: str
    usage: Usage


@dataclass
class UsageRead(BaseDataClass):
    """
    Response model for database usage statistics.
    """

    instances: List[SingleDBUsage]
    total: Usage
    uuid: str


@dataclass
class StatQuery(BaseDataClass):
    """
    Response model for a query in the database statistics.
    """

    query: str
    rows_read: int
    rows_written: int


@dataclass
class DbInstance(BaseDataClass):
    """
    Response model for a database instance.
    """

    hostname: str
    name: str
    region: str
    type: str
    uuid: str
