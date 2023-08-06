import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATASET_SLUGNAME
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.asyncio.processor.standard.sample import (
    fast_gather,
)
from sarus_data_spec.manager.ops.asyncio.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetOp,
)
from sarus_data_spec.marginals import marginals as marginals_builder
from sarus_data_spec.path import straight_path
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.manager.ops.asyncio.processor.standard.sampling.differentiated_sampling_sizes import (  # noqa: E501
        differentiated_sampling_sizes,
    )
    from sarus_data_spec.manager.ops.asyncio.processor.standard.sampling.sql import (  # noqa: E501
        sql_differentiated_sample_to_arrow,
    )
except ModuleNotFoundError as exception:
    # for the public repo
    if (
        exception.name
        == 'sarus_data_spec.manager.ops.asyncio.processor.standard.sampling'  # noqa: E501
    ):
        pass
    else:
        raise exception

try:
    from sarus_statistics.tasks.size.sample_visitor import (
        differentiated_sampled_size,
    )
except ModuleNotFoundError as exception:
    # for the public repo
    if 'sarus_statistics' in str(exception.name):
        pass
    else:
        raise exception


class DifferentiatedSample(StandardDatasetOp):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a differentiated transform
    """

    async def size(self) -> st.Size:
        parent_size = await self.parent_size()
        size_dict = await differentiated_sampling_sizes(self.dataset)
        return size_builder(
            self.dataset,
            differentiated_sampled_size(parent_size.statistics(), size_dict),
        )

    async def bounds(self) -> st.Bounds:
        parent_bounds = await self.parent_bounds()
        size_dict = await differentiated_sampling_sizes(self.dataset)
        return bounds_builder(
            self.dataset,
            differentiated_sampled_size(parent_bounds.statistics(), size_dict),
        )

    async def marginals(self) -> st.Marginals:
        parent_marginals = await self.parent_marginals()
        size_dict = await differentiated_sampling_sizes(self.dataset)
        return marginals_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_marginals.statistics(), size_dict
            ),
        )

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            protected_paths=parent_schema.protobuf().protected,
            properties=parent_schema.properties(),
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = t.cast(Dataset, self.parent())
        if parent.manager().is_big_data(parent):
            return await sql_differentiated_sample_to_arrow(
                self.dataset, batch_size
            )
        return await self._arrow_to_arrow(batch_size)

    async def _arrow_to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        seed = Scalar(
            self.dataset.transform().protobuf().spec.differentiated_sample.seed
        ).value()
        generator = np.random.default_rng(seed)
        parent_batches = [
            batch async for batch in await self.parent_to_arrow()
        ]
        previous_ds = t.cast(Dataset, self.parent())
        previous_schema = await self.parent_schema()
        previous_size = await previous_ds.manager().async_size(previous_ds)
        assert previous_size
        size_dict = await differentiated_sampling_sizes(self.dataset)
        path_to_tables = previous_schema.tables()[0].to_strings_list()[0][:-1]
        table = pa.Table.from_batches(parent_batches).combine_chunks()
        field_names = [field.name for field in table.field('data').flatten()]
        probas = np.array(
            [
                size_dict[straight_path(path_to_tables + [field])]
                / previous_size.statistics().children()[field].size()
                for field in table['data']
                .flatten()[field_names.index('data.field_selected')]
                .to_pylist()
            ]
        )

        probas = probas / probas.sum()
        if (
            self.dataset.transform()
            .protobuf()
            .spec.differentiated_sample.HasField('fraction')
        ):
            indices = generator.choice(
                table.num_rows,
                replace=False,
                size=int(
                    self.dataset.transform()
                    .protobuf()
                    .spec.differentiated_sample.fraction
                    * table.num_rows
                ),
                p=probas,
            )

        else:
            effective_size = min(
                self.dataset.transform()
                .protobuf()
                .spec.differentiated_sample.size,
                table.num_rows,
            )
            indices = generator.choice(
                table.num_rows,
                replace=False,
                size=effective_size,
                p=probas,
            )

        return fast_gather(
            indices=indices,
            batches=table.to_batches(max_chunksize=1000),
            batch_size=batch_size,
        )
