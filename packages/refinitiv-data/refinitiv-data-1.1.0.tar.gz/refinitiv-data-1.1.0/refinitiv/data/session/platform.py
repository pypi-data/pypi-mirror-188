__all__ = ("Definition", "GrantPassword")

from .._core.session.grant_password import GrantPassword


class Definition(object):
    """
    Platform session.
    Can be defined indirectly using the name of a session defined
    in the configuration file or directly by specifying the other Definition parameters.

    Parameters
    ----------
    name: str, default "default"
        Session name
    app_key: str, optional
        Application key
    grant: GrantPassword object, optional
        Grants objects containing the credentials used to authenticate the user
        (or the machine) when connecting to the data platform.
        Several kind of grant objects can be used GrantPassword is the most common one.
    signon_control: bool, default True
        Controls the exclusive sign-on behavior when the user account
        (or computer account) for this session is concurrently used by another
        application. When this parameter is set to True, opening this session
        automatically disconnects the other application. When this parameter is set to
        False, the opening of this session fails preserving the other application.
    deployed_platform_host: str, optional
        Host name (or IP) and port to be used to connect to Real-Time Distribution
        System.
    deployed_platform_username: str, optional
        DACS user name identifying the user when to connecting
        to a Real-Time Distribution System
    dacs_position: str, optional
        DACS position identifying the terminal when connecting to a Real-Time
        Distribution System.
    dacs_application_id: str, optional
        Must contain the user's Data Access Control System application ID.
        For more information, refer to the DACS documentation on my.refinitiv.com

    Raises
    ----------
    Exception
        If app-key is not found in the config file and in arguments.

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> definition = rd.session.platform.Definition(name="custom-session-name")
    >>> platform_session = definition.get_session()
    """

    def __init__(
        self,
        name: str = "default",
        app_key: str = None,
        grant=None,
        signon_control: bool = True,
        deployed_platform_host: str = None,
        deployed_platform_username: str = None,
        dacs_position: str = None,
        dacs_application_id: str = None,
    ) -> None:
        from .._core.session._session_provider import (
            _make_platform_session_provider_by_arguments,
        )

        if not isinstance(name, str):
            raise ValueError("Invalid session name type, please provide string.")

        self._create_session = _make_platform_session_provider_by_arguments(
            session_name=name,
            app_key=app_key,
            signon_control=signon_control,
            deployed_platform_host=deployed_platform_host,
            deployed_platform_username=deployed_platform_username,
            dacs_position=dacs_position,
            dacs_application_id=dacs_application_id,
            grant=grant,
        )

    def get_session(self):
        """
        Creates and returns the session.

        Returns
        -------
        The platform session instance.
        """
        session = self._create_session()
        return session
