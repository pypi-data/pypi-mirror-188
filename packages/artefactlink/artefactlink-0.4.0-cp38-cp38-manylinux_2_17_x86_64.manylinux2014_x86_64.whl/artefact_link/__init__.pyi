import datetime
import pathlib
from typing import List, Dict, Union, Optional, Tuple


class PyVcsID:
    """
    Deterministic Identifier for Version Control Info - hashed from SHA, Branch, and
    Remote Resource, Owner, and Repository.

    It's really unlikely you'll use this directly - it's commonly provided as a shorthand
    to VcsInformation.
    """
    ...


class PyRemoteRepository:
    """Linked Version Control Repository"""
    def __init__(self, resource: str, repository: str, owner: str) -> None:
        ...

    @property
    def resource(self) -> str:
        """Version Control Provider, i.e. GitHub, BitBucket, GitLab """
        ...

    @property
    def repository(self) -> str:
        """Remote Repository for the saved model, e.g. 'Jackdaw'"""
        ...

    @property
    def owner(self) -> str:
        """owner of Remote Repository, e.g. 'ShareableAI'"""
        ...

class PyVcsInfo:
    """Version Control Information"""

    def __init__(self, sha: str, branch: str, remote: Optional[PyRemoteRepository]) -> None:
        ...

    @property
    def branch(self) -> str: ...

    @property
    def sha(self) -> str: ...

    @property
    def short_sha(self) -> str: ...

    @property
    def remote_repository(self) -> Optional[PyRemoteRepository]:
        """
        Remote Repository for the Model

        May not exist - Git doesn't enforce that a commit must have a remote attached.
        """
        ...

    def id(self) -> PyVcsID:
        ...


class PyRunID:
    def __init__(self, endpoint: ArtefactEndpoint) -> None:
        ...

    @staticmethod
    def from_existing(uuid_str: str) -> PyRunID:
        ...


class PyMetricFilter:
    def __init__(self, name: str, value: float, ordering: str) -> None:
        ...

    def or_(self, metric: PyMetricFilter) -> PyMetricFilter:
        ...

    def and_(self, metric: PyMetricFilter) -> PyMetricFilter:
        ...


class LocalArtefactRegistry:
    path: Optional[pathlib.Path]

    def __init__(self, path: Optional[pathlib.Path]) -> None:
        self.path = path


class LocalEndpoint:
    def __init__(self, registry_endpoint: LocalArtefactRegistry, storage_location: Optional[pathlib.Path]) -> None:
        ...


class ShareableAIEndpoint:
    def __init__(self, api_key: str) -> None:
        ...


ArtefactEndpoint = Union[LocalEndpoint, ShareableAIEndpoint]


class PyID:
    """
    Artefact or Artefact Set ID - readable in Python
    """

    def as_string(self) -> str: ...

    def as_hex_string(self) -> str: ...

    @staticmethod
    def from_string(id: str) -> PyID: ...


class PyModelRun:
    def __init__(self, endpoint: ArtefactEndpoint, run_id: PyRunID, model_uuid: str, model_name: str,
                 vcs: PyVcsInfo) -> None:
        ...

    def save_metrics(self, endpoint: ArtefactEndpoint, metrics: List[Tuple[datetime.datetime, str, float]]):
        ...


class PyModelUUID:
    """
        Identifier for a Python Model class - used to distinguish classes with the same
        name during the same run.
    """

    def __init__(self) -> None: ...

    @staticmethod
    def from_existing(uuid_str: str) -> PyModelUUID: ...


class PyShortArtefactSchemaID:
    """
    Shorthand/Nickname for a Model Artefact Schema ID.

    Artefact Schema IDs are long because they're deterministically unique. That's a great
    property to have when you hold potentially millions of models, and an awful property
    when you want to share an ID over slack.

    ShortArtefactSchemaIDs are like short SHAs on Git - they're the first 8 characters of
    a real ArtefactSchemaID, and are still pretty unlikely to collide for the models you as
    a user might create over your lifetime. That means they represent a risk - they're fine
    for using for interactive sessions, but have an improbably small chance of colliding in
    a production environment. Use them as you would short SHAs, and you'll never have an issue.
    """
    ...

    @staticmethod
    def from_str(string: str) -> PyShortArtefactSchemaID: ...


class PyModelID:
    """Model Identifier."""

    def __init__(self, name: str, vcs_hash: str, artefact_set_id: PyID, artefact_schema_id: PyID) -> None: ...

    @property
    def name(self) -> str: ...

    @property
    def vcs_id(self) -> PyVcsID: ...

    @property
    def artefact_schema_id(self) -> PyID: ...

    @property
    def short_schema_id(self) -> PyShortArtefactSchemaID:
        ...

    @property
    def model_size(self) -> int: ...

class PyArtefact:
    """
    Data Backing for a Python-Compatible Artefact
    """

    def id(self) -> PyID:
        ...

    def path(self, temp_dir: pathlib.Path) -> pathlib.Path: ...

    """
       Retrieve or create a local path containing the Model Artefact
    """


class ModelData:
    """
    Model Data Representation for Save/Load
    """

    def __init__(
            self,
            name: str,
            vcs_info: PyVcsInfo,
            local_artefacts: List[LocalArtefactPath],
            children: Dict[str, PyModelID],
    ):
        """Create a Model Data Representation
        Args:
            name: Model Name
            vcs_hash: The Version Control System hash for the file
            local_artefacts: Paths for artefacts on the local system
            remote_artefacts: Paths for artefacts on remote systems
            children: Model IDs for Model Children
        """
        ...

    def dumps(
            self, endpoint: ArtefactEndpoint, run_id: Optional[PyRunID], model_uuid: Optional[PyModelUUID]
    ) -> PyModelID:
        """
        Save Model Data to `endpoint`

        If a RunID and Model UUID is provided, the model will be associated with a given run for the purpose
        of tracking associated metrics.
        """
        ...

    @property
    def model_id(self) -> PyModelID:
        ...

    @property
    def child_ids(self) -> dict[str, PyModelID]: ...

    def artefact_slots(self) -> List[str]:
        """Provide a list of all artefacts on this object"""
        ...

    def artefact_by_slot(self, slot: str) -> PyArtefact:
        """Retrieve an Artefact by the slot name"""
        ...

    def child_id_by_slot(self, slot: str) -> PyModelID: ...


class LocalArtefactPath:
    """
    Local Artefact - referenced by absolute path
    """

    def __init__(self, slot: str, path: str) -> None: ...


class PyModelSearchResult:
    """Search Results for a given Model"""

    @property
    def model_id(self) -> PyModelID: ...

    @property
    def vcs_info(self) -> PyVcsInfo: ...

    @property
    def creation_time(self) -> int:
        """Creation Time in seconds since epoch"""
        ...


def search_by_model_id(
        endpoint: ArtefactEndpoint,
        short_sha: str,
        short_artefact_schema_id: PyShortArtefactSchemaID,
        model_name: str
) -> PyModelID:
    """
    Lookup ModelID by its shortcode
    :param endpoint: Local or Remote Model
    :param short_sha: First 7 characters of a Git Hash/Git SHA
    :param short_artefact_schema_id: Short Artefact Schema ID from Search
    :param model_name: Model Name
    :return: Model ID
    """
    ...


def load_model_data(
        model_name: str,
        vcs_id: PyVcsID,
        artefact_schema_id: PyID,
        endpoint: ArtefactEndpoint
) -> ModelData:
    """
    Load Model Data from Model Identifiers

    Requests the Model Data from the remote SQL server, and the Artefact Data from the remote Storage server.

    The model info and artefact data is copied to the local sql server and storage server respectively,
    and then artefacts are provided to the caller. The artefacts are presented with the OnDisk data backing,
    giving the most flexibility in terms of use. It is entirely possible to instead present Remote links to the
    end user, but this means consuming a stream each time the data must be checked, and assuming that the remote
    connection remains valid after the object is returned, which cannot be guaranteed.

    :param vcs_id: Version Control Information ID
    :param model_name: Name of the Model
    :param artefact_schema_id: ID representing the saved Artefacts and their layout in the model
    :param endpoint: Connection Options

    """
    ...


def search_for_models(
        endpoint: ArtefactEndpoint,
        names: List[str],
        runs: List[PyRunID],
        metric_filter: Optional[PyMetricFilter],
        vcs_id: List[PyVcsID],
        include_children: bool
) -> List[PyModelSearchResult]:
    ...


def search_for_vcs_id(
        endpoint: ArtefactEndpoint,
        repository_name: str,
        branch_name: Optional[str]
) -> List[PyVcsID]:
    ...
