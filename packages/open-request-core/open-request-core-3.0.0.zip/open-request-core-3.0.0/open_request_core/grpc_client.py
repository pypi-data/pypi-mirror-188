#!/usr/bin/env python
# coding=utf-8
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, TypeVar
from grpclib.client import Channel

from .exception import ServerException

if TYPE_CHECKING:
    from .grpc_request import Request, Response, TResponse

logger = logging.getLogger("open-request-core")


class Client(Channel):

    async def do_action(self, request: Request[TResponse]) -> TResponse:
        async with self.request(request.name, request.cardinality, type(request), request.resp_cls) as stream:
            await stream.send_message(request, end=True)
            resp = await stream.recv_message()
        return resp
