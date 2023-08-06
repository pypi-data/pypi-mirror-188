# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
from typing import TypeVar

import pydantic

from .objectmeta import ObjectMeta
from .resourcemetaclass import ResourceMetaclass


T = TypeVar("T", bound="Resource")


class Resource(pydantic.BaseModel, metaclass=ResourceMetaclass):
    __abstract__: bool = True
    api_version: str
    kind: str
    metadata: ObjectMeta

    def __init_subclass__(
        cls,
        *,
        version: str,
        group: str | None = None,
        **kwargs: Any
    ):
        super().__init_subclass__(**kwargs)

    @classmethod
    def restore(
        cls: type[T],
        uid: int | str,
        created: datetime.datetime,
        name: str | None = None,
        annotations: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        spec: dict[str, Any] | None = None
    ) -> T:
        metadata = metadata or {}
        metadata.setdefault('annotations', annotations or {})
        metadata.setdefault('labels', labels or {})
        metadata.setdefault('name', name or str(uid))
        metadata.update({
            'created': created,
            'uid': uid
        })
        return cls.parse_obj({
            'metadata': metadata,
            'spec': spec or {}
        })

    @classmethod
    def new(
        cls: type[T],
        name: str | None,
        params: dict[str, Any]
    ) -> T:
        """Create a new resource."""
        metadata: dict[str, Any] = {'name': name}
        if not metadata.get('name'):
            del metadata['name']
            metadata['generate_name'] = True
        self = cls.parse_obj({
            'metadata': {**metadata, 'uid': None},
            'spec': params
        })
        if self.metadata.generate_name and not self.metadata.name:
            self.metadata.name = self.generate_name()
        self.metadata.generate_name = not bool(self.metadata.name) or None
        return self

    def label(self, key: str, value: str) -> None:
        """Adds a label to the resources' metadata."""
        self.metadata.labels[key] = value

    def generate_name(self) -> str | None:
        """Generates a name for the resource. The default implementation
        returns ``None``, meaning that it does not know how to generate
        a name and defers the generation to other parts of the code.
        """
        return None

    def is_new(self) -> bool:
        """Return a boolean indicating if the object is new i.e. to the clients'
        knowledge, did not priorly exist.
        """
        return self.metadata.resource_version == 'pristine'