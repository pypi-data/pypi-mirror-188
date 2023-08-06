import uuid
from datetime import datetime
from secrets import randbits
from time import time
from typing import Optional, cast, FrozenSet, TypedDict

from kaiju_db.services import DatabaseService, SQLService
from kaiju_tools.cache import BaseCacheService

from kaiju_auth.tables import sessions_table

__all__ = ['SessionService', 'UserSession']


class UserSession(TypedDict):
    """User session data."""

    id: str
    user_id: Optional[uuid.UUID]
    user_agent: Optional[str]
    expires: int
    permissions: FrozenSet[str]
    data: dict
    created: datetime
    _stored: bool
    _changed: bool


class SessionService(SQLService):
    """Session store base class."""

    service_name = 'sessions'
    table = sessions_table
    session_key = 'session:{session_id}'

    def __init__(
        self,
        app,
        database_service: DatabaseService = None,
        cache_service: BaseCacheService = None,
        session_idle_timeout: int = 24 * 3600,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param database_service:
        :param cache_service:
        :param session_idle_timeout: (s) Idle life timeout each session.
        :param logger:
        """
        super().__init__(app, database_service, logger=logger)
        self._cache: BaseCacheService = self.discover_service(cache_service, cls=BaseCacheService)
        self.session_idle_timeout = session_idle_timeout

    def get_new_session(self, data: dict, *, user_agent: str = None) -> UserSession:
        """Create and return a new session (not stored yet).

        :param data:
        :param user_agent: user agent or client id for security purposes
        """
        session = self._create_new_session(data, user_agent)
        self.logger.info('New session: %s', session['id'])
        return session

    async def save_session(self, session: UserSession, /) -> None:
        """Save session to the storage.

        The session will be stored only if it is marked as stored, and it has been changed.
        Token-auth sessions and initial sessions without data won't be stored.
        """
        if session['_changed'] and session['_stored']:
            self.logger.info('Saving session: %s', session['id'])
            data = session.copy()
            del data['_changed']
            del data['_stored']
            data['expires'] = int(time()) + self.session_idle_timeout
            on_conflict_values = data.copy()
            del on_conflict_values['id']
            del on_conflict_values['user_agent']
            del on_conflict_values['created']
            await self._cache.set(
                self.session_key.format(session_id=session['id']), session, ttl=session['expires'], nowait=True
            )
            await self.create(
                data,
                columns=[],
                on_conflict='do_update',
                on_conflict_keys=['id'],
                on_conflict_values=on_conflict_values,
            )

    async def delete_session(self, session_id: str, /) -> None:
        """Delete session from the storage."""
        self.logger.info('Removing session: %s', session_id)
        await self._cache.delete(self.session_key.format(session_id=session_id), nowait=True)
        await self.delete(session_id, columns=[])

    async def load_session(self, session_id: str, /, *, user_agent: Optional[str] = None) -> Optional[UserSession]:
        """Load session from the storage.

        :param session_id: unique session id
        :param user_agent: user agent or client id for security purposes
        :return: returns None when session is not available
        """
        key = self.session_key.format(session_id=session_id)
        session = cached = await self._cache.get(key)
        if not session:
            session = await self.list(conditions={'id': session_id, 'user_agent': user_agent}, limit=1)
            session = next(session['data'], None)
        if not session:
            self.logger.info('Session not found: %s', session_id)
        elif session['expires'] < time():
            self.logger.info('Expired session: %s', session_id)
            await self.delete(session_id)
        else:
            self.logger.debug('Loaded session: %s', session_id)
            if not cached:
                await self._cache.set(key, session, nowait=True)
            session = cast(UserSession, session)
            return session

    def _create_new_session(self, data, user_agent) -> UserSession:
        """Create a new session object."""
        return UserSession(
            id=uuid.UUID(int=randbits(128)).hex,
            user_id=None,
            permissions=frozenset(),
            user_agent=user_agent,
            data=data,
            expires=int(time()) + self.session_idle_timeout,
            created=datetime.now(),
            _changed=bool(data),
            _stored=True,
        )
