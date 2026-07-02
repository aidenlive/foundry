# foundation/labels

Provider-free module that turns Foundry context into a canonical name prefix
and label map. Use it at the top of every stack so all downstream resources
share consistent naming and labels.

Inputs: `org`, `project`, `environment`, `delimiter` (default `-`),
`extra_labels`.
Outputs: `name_prefix`, `labels`, `delimiter`.
