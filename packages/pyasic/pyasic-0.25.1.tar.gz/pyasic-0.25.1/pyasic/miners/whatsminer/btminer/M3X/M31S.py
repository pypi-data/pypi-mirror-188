#  Copyright 2022 Upstream Data Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pyasic.miners._backends import BTMiner  # noqa - Ignore access to _module
from pyasic.miners._types import (
    M31S,
    M31SV10,
    M31SV20,
    M31SV60,
    M31SV70,
)  # noqa - Ignore access to _module


class BTMinerM31S(BTMiner, M31S):
    pass


class BTMinerM31SV20(BTMiner, M31SV20):
    pass


class BTMinerM31SV10(BTMiner, M31SV10):
    pass


class BTMinerM31SV60(BTMiner, M31SV60):
    pass


class BTMinerM31SV70(BTMiner, M31SV70):
    pass
