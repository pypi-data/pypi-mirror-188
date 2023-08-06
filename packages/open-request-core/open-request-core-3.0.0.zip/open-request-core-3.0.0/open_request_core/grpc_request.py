#!/usr/bin/env python
# -*- coding=utf-8 -*-
from typing import Generic, TypeVar, Type

from grpclib._typing import IProtoMessage
from grpclib.const import Cardinality

__all__ = ["Request", "Response"]


class Response(IProtoMessage):
    pass


TResponse = TypeVar("TResponse", bound=Response)


class Request(IProtoMessage, Generic[TResponse]):
    def __init__(self, name: str, cardinality: Cardinality):
        self.__name = name
        self.__cardinality = cardinality

    @property
    def name(self):
        return self.__name

    @property
    def cardinality(self):
        return self.__cardinality

    @property
    def resp_cls(self) -> Type[TResponse]:
        return IProtoMessage
