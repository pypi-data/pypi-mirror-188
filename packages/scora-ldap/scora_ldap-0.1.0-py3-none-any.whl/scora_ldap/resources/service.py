import traceback

from ..database.dynamodb import get_data_by_key


class Service:
    def __init__(self) -> None:
        self.service: str = ""
        self.ldap_admin_groups: list[str] = []
        self.ldap_domain: str = ""
        self.ldap_groups: list[str] = []
        self.ldap_root_dn: str = ""
        self.ldap_root_dn_dev: str = ""
        self.ldap_server: str = ""
        self.ldap_server_alias: list[str] = []

    def get_props(
        self, value: any, dynamodb_object, dynamodb_table_name: str, field=None
    ):
        response_config: Service = None

        try:
            response_config = get_data_by_key(
                dynamodb_object, dynamodb_table_name, "service", value, field
            )
        except:
            traceback.print_exc()

        return response_config
