# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

python3 -m evaluation_main \
  --input_data=/home/truongnp5/Desktop/dpo/M-IFEval/data/vi_input_data_verified.jsonl \
  --input_response_data=/home/truongnp5/Desktop/dpo/M-IFEval/data/vi_input_response_data_Sen-1.7B-1.4.3-vi-en-dpo-005_v3-2025-12-19.jsonl \
  --output_dir=/home/truongnp5/Desktop/dpo/M-IFEval/evaluation

exit 0