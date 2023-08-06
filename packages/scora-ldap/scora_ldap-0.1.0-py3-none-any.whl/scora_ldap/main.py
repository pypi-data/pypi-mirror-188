from boto3.session import Session
from .utils.misc import setup_logger
from .resources.ldap import Ldap
from .resources.service import Service

logger = setup_logger(__name__)


class LdapService:
    def __init__(
        self,
        tenant: str,
        ldap_username: str,
        ldap_password: str,
        dynamodb_table_name: str,
        group: str = "",
        aws_region: str = "us-east-1",
        aws_profile: str = "default",
    ) -> None:
        self.__ldap_username: str = ldap_username
        self.__ldap_password: str = ldap_password
        self.__ldap: Ldap = None
        self.tenant: str = tenant
        self.group: str = group

        boto3_session: Session = Session(
            profile_name=aws_profile, region_name=aws_region
        )
        dynamodb = boto3_session.resource("dynamodb")

        response_tenant_services: Service = Service.get_props(
            self,
            value=self.tenant,
            dynamodb_object=dynamodb,
            dynamodb_table_name=dynamodb_table_name,
        )
        if not response_tenant_services:
            logger.error(f"Service for {self.tenant} was not configured!")
            return

        ldap = Ldap(
            domain=self.tenant,
            user_name=self.__ldap_username,
            password=self.__ldap_password,
            group=self.group,
            service=response_tenant_services,
        )
        self.__ldap = ldap.auth()

    def get_ldap_users(self) -> tuple[list[str], list[str]]:
        return self.__ldap.groups, self.__ldap.users
