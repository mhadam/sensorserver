from app.db.crud import CRUDBase
from app.models.device_block import DeviceBlock, DeviceBlockCreate, DeviceBlockUpdate


class DeviceBlockRepository(
    CRUDBase[DeviceBlock, DeviceBlockCreate, DeviceBlockUpdate]
):
    pass
