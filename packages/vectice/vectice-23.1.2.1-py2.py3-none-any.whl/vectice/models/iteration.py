from __future__ import annotations

import logging
import pickle  # nosec
from typing import TYPE_CHECKING, Any

from vectice.api.json.iteration import IterationInput, IterationStatus, IterationStepArtifactInput
from vectice.api.json.model_version import ModelVersionOutput
from vectice.models.attachment_container import AttachmentContainer
from vectice.models.datasource.datawrapper.metadata import SourceUsage
from vectice.utils.automatic_link_utils import existing_dataset_logger, existing_model_logger, link_assets_to_step
from vectice.utils.common_utils import _check_code_source, _check_for_code, _check_read_only, _inform_if_git_repo

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client
    from vectice.models import Phase, Project, Step, Workspace
    from vectice.models.datasource.datawrapper import DataWrapper
    from vectice.models.model import Model

_logger = logging.getLogger(__name__)

MISSING_DATASOURCE_ERROR_MESSAGE = "Cannot create modeling dataset. Missing %s data source."


class Iteration:
    """Represent a Vectice iteration.

    Iterations reflect the model development and test cycles completed
    by data scientists until a fully functional algorithm is ready for
    deployment.  Each iteration contains the sequence of steps defined
    at the Phase and acts as a guardrail for data scientists to
    provide their updates.
    """

    __slots__ = [
        "_id",
        "_index",
        "_phase",
        "_status",
        "_client",
        "_modeling_dataset",
        "_model",
        "_current_step",
        "_pointers",
        "_step",
    ]

    def __init__(
        self,
        id: int,
        index: int,
        phase: Phase,
        status: IterationStatus | None = IterationStatus.NotStarted,
    ):
        """Initialize an iteration.

        Parameters:
            id: The iteration identifier.
            index: The index of the iteration.
            phase: The project to which the iteration belongs.
            status: The status of the iteration.
        """
        self._id = id
        self._index = index
        self._phase = phase
        self._status = status
        self._client: Client = self._phase._client
        self._modeling_dataset: tuple[DataWrapper, DataWrapper, DataWrapper] | None = None
        self._model: Model | None = None
        self._current_step: Step | None = None

    def __repr__(self):
        steps = len(self.steps)
        return f"Iteration (index={self._index}, status={self._status}, No. of steps={steps})"

    def __eq__(self, other: object):
        if not isinstance(other, Iteration):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """The iteration's identifier.

        Returns:
            The iteration's identifier.
        """
        return self._id

    @id.setter
    def id(self, iteration_id: int):
        """Set the iteration's identifier.

        Parameters:
            iteration_id: The identifier.
        """
        _check_read_only(self)
        self._id = iteration_id

    @property
    def index(self) -> int:
        """The iteration's index.

        Returns:
            The iteration's index.
        """
        return self._index

    @property
    def properties(self) -> dict:
        """The iteration's identifier and index.

        Returns:
            A dictionary containing the `id` and `index` items.
        """
        return {"id": self.id, "index": self.index}

    @property
    def step_names(self) -> list[str]:
        """The names of the steps required in this iteration.

        Returns:
            The steps names.
        """
        return [step.name for step in self.steps]

    def step(self, step: str) -> Step:
        """Get a step by name.

        Step names are configured for a phase by the Vectice administrator.

        Parameters:
            step: The name of the step

        Returns:
            A step.
        """
        from vectice.models import Step

        steps_output = self._client.get_step_by_name(step, self.id)
        _logger.info(f"Step: {steps_output.name} successfully retrieved.")
        step_object = Step(
            steps_output.id,
            self,
            steps_output.name,
            steps_output.index,
            steps_output.description,
            steps_output.completed,
            steps_output.artifacts,
        )
        self._current_step = step_object
        return step_object

    @property
    def steps(self) -> list[Step]:
        """The steps required in this iteration.

        Returns:
            The steps required in this iteration.
        """
        from vectice.models import Step

        steps_output = self._client.list_steps(self._phase.id, self.index, self._phase.name)
        return sorted(
            [Step(item.id, self, item.name, item.index, item.description, item.completed) for item in steps_output],
            key=lambda x: x.index,
        )

    @property
    def modeling_dataset(
        self,
    ) -> tuple[DataWrapper, DataWrapper, DataWrapper] | None:
        """The iteration's modeling dataset.

        Returns:
            The training set.
            The test set.
            The validation set.
        """
        return self._modeling_dataset

    @modeling_dataset.setter
    def modeling_dataset(self, data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]):
        """Set a modeling dataset.

        Provides training, testing and validation datasources, the
        order of which does not matter (despite it being a tuple) and
        the combination of the data sources does not either. Thus, you
        could use whatever combination suites your needs.

        The DataWraper can be accessed via vectice.FileDataWrapper,
        vectice.GcsDataWrapper and vectice.S3DataWrapper.

        Or for example `from vectice import FileDataWrapper`.

        Parameters:
            data_sources: A tuple of three datasources; their metadata
                must be of three types: training, testing and validation.
        """
        # TODO: refactor to break cyclic import
        from vectice import code_capture
        from vectice.api.json.dataset_register import DatasetRegisterInput

        _check_read_only(self)
        logging.getLogger("vectice.models.iteration").propagate = True
        if code_capture:
            code_version_id = _check_for_code(self._client, self._phase._project.id, _logger)
        else:
            _inform_if_git_repo(_logger)
            code_version_id = None
        train_datasource, test_datasource, validation_datasource = self._get_datasources_in_order(data_sources)
        self._modeling_dataset = train_datasource, test_datasource, validation_datasource

        name = self._client.get_dataset_name(train_datasource)
        inputs = self._client.get_dataset_inputs(train_datasource)
        dataset_sources = self._get_metadata_from_sources((train_datasource, test_datasource, validation_datasource))
        dataset_register_input = DatasetRegisterInput(
            name=name,
            type=SourceUsage.MODELING.value,
            datasetSources=dataset_sources,
            inputs=inputs,
            codeVersionId=code_version_id,
        )
        data = self._client.register_dataset(
            dataset_register_input,
            iteration_id=self._id,
            project_id=self._phase._project._id,
            phase_id=self._phase.id,
        )
        existing_dataset_logger(data, name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self, step_artifact, name, data, _logger)

    @staticmethod
    def _get_datasources_in_order(
        data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]
    ) -> tuple[DataWrapper, DataWrapper, DataWrapper]:
        from vectice import DatasetSourceUsage

        if len(data_sources) != 3:
            raise ValueError("Exactly three datasources are needed to create a modeling dataset.")
        train_datasource, test_datasource, validation_datasource = None, None, None
        for data_source in data_sources:
            if data_source.metadata.usage == DatasetSourceUsage.TRAINING:
                train_datasource = data_source
            elif data_source.metadata.usage == DatasetSourceUsage.TESTING:
                test_datasource = data_source
            elif data_source.metadata.usage == DatasetSourceUsage.VALIDATION:
                validation_datasource = data_source
        if not train_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "training")
        if not test_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "testing")
        if not validation_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "validation")
        return train_datasource, test_datasource, validation_datasource

    @staticmethod
    def _get_metadata_from_sources(data_sources: tuple[DataWrapper, DataWrapper, DataWrapper]) -> list[dict]:
        return [data_source.metadata.asdict() for data_source in data_sources if data_source]

    @property
    def model(self) -> Model | None:
        """The iteration's model.

        Returns:
            The iteration's model.
        """
        return self._model

    @model.setter
    def model(self, model: Model):
        """Set the model for the iteration.

        The model can be created using the Model Wrapper, accessed via
        vectice.Model or `from vectice import Model`.

        Parameters:
            model: The model.
        """
        from vectice import code_capture

        _check_read_only(self)
        logging.getLogger("vectice.models.iteration").propagate = True
        if code_capture:
            code_version_id = _check_code_source(self._client, self._phase._project._id, _logger)
        else:
            _inform_if_git_repo(_logger)
            code_version_id = None
        self._model = model
        model_output = self._client.register_model(
            model, self._phase._project._id, self._phase.id, self._id, code_version_id, model.inputs
        )
        model_version = model_output.model_version
        attachments = self._set_model_attachments(model, model_version)
        _logger.info(
            f"Successfully registered Model(name='{model.name}', library='{model.library}', "
            f"technique='{model.technique}', version='{model_version.name}')."
        )
        existing_model_logger(model_output, model.name, _logger)
        step_artifact = IterationStepArtifactInput(id=model_output["modelVersion"]["id"], type="ModelVersion")
        attachments = (
            [
                IterationStepArtifactInput(id=attach["fileId"], entityFileId=attach["entityId"], type="EntityFile")
                for attach in attachments
            ]
            if attachments
            else None
        )
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self, step_artifact, model.name, model_output, _logger, attachments)

    def cancel(self) -> Iteration:
        """Cancel the iteration by abandoning all steps still open.

        Returns:
            The iteration, canceled.
        """
        iteration_input = IterationInput(status=IterationStatus.Abandoned.name)
        iteration_output = self._client.update_iteration(self.id, iteration_input)
        return Iteration(
            iteration_output.id,
            iteration_output.index,
            self._phase,
            iteration_output.status,
        )

    def _set_model_attachments(self, model: Model, model_version: ModelVersionOutput):
        logging.getLogger("vectice.models.attachment_container").propagate = True
        attachments = None
        if model.attachments:
            container = AttachmentContainer(model_version, self._client)
            attachments = container.add_attachments(model.attachments)
        if model.predictor:
            model_content = self._serialize_model(model.predictor)
            model_type_name = type(model.predictor).__name__
            container = AttachmentContainer(model_version, self._client)
            container.add_serialized_model(model_type_name, model_content)
        return attachments

    @staticmethod
    def _serialize_model(model: Any) -> bytes:
        return pickle.dumps(model)

    @property
    def connection(self) -> Connection:
        """The connection to which this iteration belongs.

        Returns:
            The connection to which this iteration belongs.
        """
        return self._phase.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this iteration belongs.

        Returns:
            The workspace to which this iteration belongs.
        """
        return self._phase.workspace

    @property
    def project(self) -> Project:
        """The project to which this iteration belongs.

        Returns:
            The project to which this iteration belongs.
        """
        return self._phase.project

    @property
    def phase(self) -> Phase:
        """The phase to which this iteration belongs.

        Returns:
            The phase to which this iteration belongs.
        """
        return self._phase
