# pubsubplus-python-client
#
# Copyright 2021-2023 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains the enum classes related to SolaceTransportState"""

import enum

from abc import ABC, abstractmethod
from typing import Union, Callable
from solace.messaging.config._solace_message_constants import CCSMP_SUB_CODE, CCSMP_INFO_SUB_CODE, \
    CCSMP_INFO_CONTENTS, CCSMP_CALLER_DESC, CCSMP_RETURN_CODE, CCSMP_SUB_CODE_OK
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError

class _SolaceTransportState(enum.Enum):
    # TODO model live state for other useful states like connecting, reconnecting, etc
    LIVE = 1
    DOWN = -1

class _SolaceTransportEvent(enum.Enum):
    """
    Enumeration of different transport events, add more when necessary.
    """

    TRANSPORT_DOWN = 0
    TRANSPORT_UP = 1
    TRANSPORT_RECONNECTING = 2
    TRANSPORT_RECONNECTED = 3

class _SolaceTransport(ABC):
    """
    Interface for internal transport used by services.
    """

    @property
    @abstractmethod
    def event_emitter(self) -> '_SolaceTransportEventEmitter':
        ...

    @abstractmethod
    def connect(self) -> (int, Union[Exception, None]):
        ...

    @abstractmethod
    def disconnect(self) -> (int, Union[Exception, None]):
        ...

class _SolaceTransportEventInfo:
    def __init__(self, host, message, event_info:dict, exception = None):
        self._host = host
        self._message = message
        self._event_info: dict = event_info
        self._exception = exception

    @property
    def host(self):
        return self._host

    @property
    def message(self):
        return self._message

    @property
    def subcode(self) -> int:
        return self._event_info[CCSMP_INFO_SUB_CODE]
    
    @property
    def subcode_str(self) -> str:
        return self._event_info[CCSMP_SUB_CODE]

    @property
    def exception(self):
        if self._exception == None:
            error = None
            if self.subcode_str != CCSMP_SUB_CODE_OK:
                # TODO handle more complex transport error type mapping based on subcode
                error = PubSubPlusClientError(message=self._event_info)
            self._exception = error
        return self._exception

    def __str__(self):
        error = self.exception
        if error:
            return f"{type(self).__name__}:[host:'{self._host}', message:'{self._message}', error_info: [{self._event_info}], exception: '{error}']"
        else:
            return f"{type(self).__name__}:[host:'{self._host}', message:'{self._message}', error_info: [{self._event_info}]]"

class _SolaceTransportEventEmitter(ABC):
    @abstractmethod
    def register_transport_event_handler(self, event: '_SolaceTransportEvent', handler: Callable[[dict], None]) -> int:
        """
        Registers transport event handlers, when used with a _SolaceTransport event should be register before calls
        to connect. Note only one handler can be registered at a time and replaces the previous handler.
        """

    @abstractmethod
    def unregister_transport_event_handler(self, handler_id: int):
        """
        Unregisters transport event handlers so that they can no longer be called. This is useful to ensure that no
        event handlers are called after the transport has disconnected.
        """

    @abstractmethod
    def _emit_transport_event(self, event: '_SolaceTransportEvent', event_info: '_SolaceTransportEventInfo'):
        """
        Emits a transport event along with the variable arguments needed for the event handler.
        """
