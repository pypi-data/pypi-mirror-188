from zainpay.utils.constants import MODES
from zainpay.virtual_account.zainbox import ZainBox


class ZainPay:

    zainbox: ZainBox

    def __init__(self, pub_key: str, mode: MODES = MODES.DEVELOPMENT) -> None:
        self.zainbox = ZainBox(pub_key=pub_key, mode=mode)

    def create_zainbox(self, *args, **kwargs):
        return self.zainbox.create_zainbox(*args, **kwargs)

    def list_zainbox(self, *args, **kwargs):
        return self.zainbox.list_zainbox(*args, **kwargs)
