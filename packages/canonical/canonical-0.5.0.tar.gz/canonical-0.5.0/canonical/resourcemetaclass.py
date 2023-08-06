# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

import pydantic

from .objectmeta import ObjectMeta


class ResourceMetaclass(pydantic.main.ModelMetaclass):

    def __new__(
        cls,
        name: str,
        bases: tuple[type[Any]],
        namespace: dict[str, Any],
        **params: Any
    ) -> 'ResourceMetaclass':
        if not namespace.pop('__abstract__', False):
            annotations = namespace.setdefault('__annotations__', {})
            group = params.get('group')
            version = api_version = params.get('version')
            if group is not None:
                api_version = f'{group}/{version}'

            # Ensure that the apiVersion, kind and metadata fields are present. Defaults
            # and constraints are set during subclass initialization.
            annotations.update({
                'api_version': Literal[api_version], # type: ignore
                'kind': Literal[name], # type: ignore
                'metadata': ObjectMeta,
            })
            namespace.update({
                '__annotations__': annotations,
                'api_version': pydantic.Field(
                    alias='apiVersion',
                    default=api_version
                ),
                'kind': pydantic.Field(
                    default=name
                ),
                'metadata': pydantic.Field(
                    default=...,
                    title='Metadata',
                    description="Standard object's metadata."
                )
            })

            # Determine if there is a status model.
            ResourceStatus: Any | None = namespace.pop('Status', None)
            if ResourceStatus is not None:
                annotations.update({
                    'status': ResourceStatus.model | None
                })
                namespace.update({
                    'status': pydantic.Field(
                        default=None,
                        title='Status',
                        description=f'Most recently observed status of the `{name}`.'
                    )
                })

        new_cls = super().__new__(cls, name, bases, namespace, **params) # type: ignore
        return new_cls # type: ignore