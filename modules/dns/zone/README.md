# dns/zone

An authoritative public DNS zone.

## Contract

| Variable | Type          | Default | Notes                    |
| -------- | ------------- | ------- | ------------------------ |
| `name`   | `string`      | —       | Zone/domain (example.com) |
| `labels` | `map(string)` | `{}`    | Where supported          |

Outputs: `zone_id`, `name_servers` — delegate the domain to these at your
registrar. Azure needs `resource_group_name`; DigitalOcean name servers are
the static ns1–ns3.digitalocean.com set.
