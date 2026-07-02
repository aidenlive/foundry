# storage/object-store

A private, versioned, encrypted object bucket.

## Contract

| Variable        | Type          | Default | Notes                                     |
| --------------- | ------------- | ------- | ----------------------------------------- |
| `name`          | `string`      | —       | Bucket name (must satisfy provider rules) |
| `labels`        | `map(string)` | `{}`    |                                            |
| `region`        | `string`      | —       |                                            |
| `versioning`    | `bool`        | `true`  |                                            |
| `force_destroy` | `bool`        | `false` | Allow destroy with objects present         |

Outputs: `bucket_id`, `bucket_name`.

## Security defaults

Buckets are private: public access blocked (S3), uniform bucket-level access
(GCS), private containers (Azure), private ACL (Spaces). Encryption at rest is
enabled everywhere. Never weaken these in the module; expose data publicly via
a CDN or signed URLs at the stack layer instead.

Azure note: storage account names must be 3–24 lowercase alphanumerics; the
module strips hyphens from `name`, so keep prefixes short. Extra input:
`resource_group_name`.
