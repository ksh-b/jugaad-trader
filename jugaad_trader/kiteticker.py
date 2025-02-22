import logging

from kiteconnect import KiteTicker

log = logging.getLogger(__name__)


class ZerodhaKiteTicker(KiteTicker):

    def __init__(self, api_key, access_token, debug=False, root=None, reconnect=True):
        super().__init__(api_key, access_token, debug, root, reconnect)

        self.root = root or self.ROOT_URI

        # Set max reconnect tries
        if super().RECONNECT_MAX_TRIES > self._maximum_reconnect_max_tries:
            log.warning(
                "`reconnect_max_tries` can not be more than {val}. Setting to highest possible value - {val}.".format(
                    val=self._maximum_reconnect_max_tries))
            self.reconnect_max_tries = self._maximum_reconnect_max_tries
        else:
            self.reconnect_max_tries = super().RECONNECT_MAX_TRIES

        # Set max reconnect delay
        if super().RECONNECT_MAX_DELAY < self._minimum_reconnect_max_delay:
            log.warning(
                "`reconnect_max_delay` can not be less than {val}. Setting to lowest possible value - {val}.".format(
                    val=self._minimum_reconnect_max_delay))
            self.reconnect_max_delay = self._minimum_reconnect_max_delay
        else:
            self.reconnect_max_delay = super().RECONNECT_MAX_DELAY

        self.connect_timeout = super().CONNECT_TIMEOUT

        self.socket_url = "{root}?api_key={api_key}" \
                          "&enctoken={access_token}".format(
            root=self.root,
            api_key=api_key,
            access_token=access_token
        )

        # Debug enables logs
        self.debug = debug

        # Placeholders for callbacks.
        self.on_ticks = None
        self.on_open = None
        self.on_close = None
        self.on_error = None
        self.on_connect = None
        self.on_message = None
        self.on_reconnect = None
        self.on_noreconnect = None

        # Text message updates
        self.on_order_update = None

        # List of current subscribed tokens
        self.subscribed_tokens = {}
