# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
""" test_multitype """
import numpy as np

from mindspore.common.api import ms_function
from mindspore.ops import Primitive
from mindspore.ops import composite as C
from mindspore.ops import operations as P
from mindspore import Tensor
from ...ut_filter import non_graph_engine


tensor_add = P.TensorAdd()
scala_add = Primitive('scalar_add')
add = C.MultitypeFuncGraph('add')


@add.register("Number", "Number")
def add_scala(x, y):
    return scala_add(x, y)


@add.register("Tensor", "Tensor")
def add_tensor(x, y):
    return tensor_add(x, y)


@ms_function
def mainf(x, y):
    return add(x, y)


@non_graph_engine
def test_multitype_tensor():
    tensor1 = Tensor(np.array([[1.2, 2.1], [2.2, 3.2]]).astype('float32'))
    tensor2 = Tensor(np.array([[1.2, 2.1], [2.2, 3.2]]).astype('float32'))
    mainf(tensor1, tensor2)


def test_multitype_scalar():
    mainf(1, 2)