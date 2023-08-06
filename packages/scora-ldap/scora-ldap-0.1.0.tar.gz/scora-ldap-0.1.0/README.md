# Scora Ldap

Services and functions to simplify ldap management, including extracting ldap infos with DynamoDB object config.

## Usage

```python
from scora_ldap import LdapService
ldap_service = LdapService(TENANT, LDAP_USERNAME, LDAP_PASSWORD, DYNAMODB_TABLE_NAME)
```

### DynamoDB Object Example

`service` as primary key.

```json
{
  "service": "service",
  "ldap_admin_groups": [],
  "ldap_domain": "@service.local",
  "ldap_groups": ["GS_1", "group2"],
  "ldap_root_dn": "CN=GS_1,OU=Grupos,DC=service,DC=local",
  "ldap_root_dn_dev": "dc=service,dc=local",
  "ldap_server": "ldap://localhost.389",
  "ldap_port": 636, // Default is 389
  "ldap_server_alias": ["service.com.br"]
}
```
