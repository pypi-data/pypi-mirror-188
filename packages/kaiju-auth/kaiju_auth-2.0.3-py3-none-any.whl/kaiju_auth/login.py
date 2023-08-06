import uuid
from base64 import b64decode
from binascii import Error as B64Error
from enum import Enum
from typing import TypedDict, Tuple, final, cast

from kaiju_tools.exceptions import NotAuthorized, MethodNotAllowed
from kaiju_tools.services import Service
from kaiju_tools.rpc import AbstractRPCCompatible

from kaiju_auth.tokens import JWTService
from kaiju_auth.users import UserService
from kaiju_auth.sessions import UserSession, SessionService

__all__ = ['AuthType', 'AuthService']


class TokenInfo(TypedDict):
    """JWT methods output."""

    access: str
    refresh: str


class UserType(TypedDict):
    """User data."""

    id: uuid.UUID
    permissions: frozenset


@final
class AuthType(Enum):
    """Client authentication types."""

    PASSWORD = 'PASSWORD'  #: login-password auth
    TOKEN = 'TOKEN'  #: token based auth
    BASIC = 'BASIC'  #: basic auth


class AuthService(Service, AbstractRPCCompatible):
    """Authentication services."""

    service_name = 'auth'

    def __init__(
        self,
        app,
        *,
        user_service: UserService = None,
        token_service: JWTService = None,
        session_service: SessionService = None,
        enable_basic_auth: bool = False,
        enable_token_auth: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param enable_basic_auth:
        :param enable_token_auth:
        :param logger:
        """
        super().__init__(app, logger=logger)
        self.enable_basic_auth = enable_basic_auth
        self.enable_token_auth = enable_token_auth
        self._users: UserService = self.discover_service(user_service, cls=UserService)
        self._tokens: JWTService = self.discover_service(token_service, cls=JWTService, required=False)
        self._sessions: SessionService = self.discover_service(session_service, cls=SessionService)

    @property
    def routes(self) -> dict:
        return {
            'login': self.password_auth,
            'jwt.get': self.get_token,
            'jwt.refresh': self.refresh_token,
            'logout': self.logout,
        }

    @property
    def permissions(self) -> dict:
        return {
            'login': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'logout': self.PermissionKeys.GLOBAL_USER_PERMISSION,
            'get_token': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
        }

    async def basic_auth(self, auth_string: str) -> UserSession:
        """Try basic auth.

        Supports both plain '<user>:<password>' strings and b64 encoded (preferred).

        :raises AuthenticationFailed:
        """
        username, password = self._parse_auth_str(auth_string)
        user = await self._users.auth(username=username, password=password)
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.BASIC)
        self.logger.info('Login completed: %s / user_id=%s', AuthType.BASIC.value, user['id'])
        return session

    @staticmethod
    def _parse_auth_str(auth_str: str) -> Tuple[str, str]:
        """Parse basic auth string (both b64 and not b64 encoded)."""
        if ':' not in auth_str:
            try:
                auth_str = b64decode(auth_str).decode('utf-8')
            except (B64Error, UnicodeDecodeError):
                raise NotAuthorized
            if ':' not in auth_str:
                raise NotAuthorized
        login, password = auth_str.split(':')
        return login, password

    async def password_auth(self, username: str, password: str) -> UserSession:
        """Authenticate a user by directly providing a login / password.

        :raises AuthenticationFailed:
        """
        session = self.app.get_session()
        if session != self.ServerSessionFlag and session['user_id']:
            await self.logout()
        user = await self._users.auth(username=username, password=password)
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.PASSWORD)
        self.logger.info('Login completed: %s / user_id=%s', AuthType.PASSWORD.value, user['id'])
        return session

    async def get_token(self, username: str, password: str) -> TokenInfo:
        """Authenticate and get a new token pair."""
        if not self._tokens or not self.enable_token_auth:
            raise MethodNotAllowed('Token auth is disabled.')
        user = await self._users.auth(username=username, password=password)
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.TOKEN)
        access, refresh = await self._tokens.generate_token_pair(
            data={'permissions': session['permissions'], 'id': session['user_id']}
        )
        return TokenInfo(access=access, refresh=refresh)

    async def refresh_token(self, access: str, refresh: str) -> TokenInfo:
        """Refresh token pair."""
        if not self._tokens or not self.enable_token_auth:
            raise MethodNotAllowed('Token auth is disabled.')
        access, refresh = await self._tokens.refresh_token(refresh)
        return TokenInfo(access=access, refresh=refresh)

    async def logout(self) -> None:
        session = self.app.get_session()
        session = cast(UserSession, session)
        if session == self.ServerSessionFlag or not session['user_id']:
            return
        await self._sessions.delete_session(session['id'])
        self.logger.info('Logged out: user_id=%s', session['user_id'])
        session['user_id'] = None
        session['permissions'] = frozenset()
        session['_stored'] = False

    async def token_auth(self, token: str) -> UserSession:
        """Try token auth (JWT or similar).

        :raises AuthenticationFailed:
        """
        token = await self._tokens.verify_token(token)
        user: UserType = token.claims_data['data']
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.TOKEN)
        self.logger.info('Login completed: %s / user_id=%s', AuthType.TOKEN.value, user['id'])
        session['_stored'] = False
        return session

    @staticmethod
    def _update_session(session: UserSession, user: UserType, auth_type: AuthType) -> None:
        """Store user data in a provided session."""
        if session and user:
            session['user_id'] = user['id']
            session['permissions'] = user['permissions']
            session['_changed'] = True
            session['_stored'] = auth_type == AuthType.PASSWORD
