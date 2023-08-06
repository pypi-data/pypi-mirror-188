import dataclasses
import logging
from typing import Optional, Dict, Any

import aiohttp

from plugp100.domain.energy_info import EnergyInfo
from plugp100.domain.power_info import PowerInfo
from plugp100.domain.tapo_api import TapoApi
from plugp100.domain.tapo_state import TapoDeviceState
from plugp100.tapo_protocol.methods import GetDeviceInfoMethod
from plugp100.tapo_protocol.methods.get_current_power import GetCurrentPowerMethod
from plugp100.tapo_protocol.methods.get_energy_usage import GetEnergyUsageMethod
from plugp100.tapo_protocol.params import DeviceInfoParams, SwitchParams, LightParams, LightEffectData
from plugp100.tapo_protocol.tapo_protocol_client import TapoProtocolClient

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TapoApiClientConfig:
    address: str
    username: str
    password: str
    session: Optional[aiohttp.ClientSession] = None


class TapoApiClient(TapoApi):
    TERMINAL_UUID = "88-00-DE-AD-52-E1"

    @staticmethod
    def from_config(config: TapoApiClientConfig) -> 'TapoApiClient':
        return TapoApiClient(
            TapoProtocolClient(config.address, config.username, config.password, config.session)
        )

    def __init__(self, client: TapoProtocolClient):
        self.client = client

    async def login(self) -> bool:
        await self.client.login()
        return True

    async def get_state(self, include_energy: bool = False, include_power: bool = False) -> TapoDeviceState:
        state_dict = await self.client.send_tapo_request(GetDeviceInfoMethod(None))
        energy_info = await self.__get_energy_usage() if include_energy else None
        power_info = await self.__get_current_power() if include_power else None
        return TapoDeviceState(state=state_dict, energy_info=energy_info, power_info=power_info)

    async def get_energy_usage(self) -> Optional[EnergyInfo]:
        energy_info = await self.__get_energy_usage()
        return EnergyInfo(energy_info) if energy_info is not None else None

    async def get_power_info(self) -> Optional[PowerInfo]:
        power_info = await self.__get_current_power()
        return PowerInfo(power_info) if power_info is not None else None

    async def on(self) -> bool:
        return await self.__set_device_state(SwitchParams(True))

    async def off(self) -> bool:
        return await self.__set_device_state(SwitchParams(False))

    async def set_brightness(self, brightness: int) -> bool:
        return await self.__set_device_state(LightParams(brightness=brightness))

    async def set_color_temperature(self, color_temperature: int, brightness: Optional[int] = None) -> bool:
        return await self.__set_device_state(LightParams(color_temperature=color_temperature, hue=0, saturation=0, brightness=brightness))

    async def set_hue_saturation(self, hue: int, saturation: int, brightness: Optional[int] = None) -> bool:
        return await self.__set_device_state(LightParams(hue=hue, saturation=saturation, color_temperature=0, brightness=brightness))

    async def set_light_effect(self, effect: LightEffectData) -> bool:
        try:
            return await self.client.set_lighting_effect_state(effect, self.TERMINAL_UUID)
        except Exception as e:
            logger.error("Error during set lighting state %s", str(e))
            return False

    async def __set_device_state(self, device_params: DeviceInfoParams) -> bool:
        try:
            await self.client.set_device_state(device_params, self.TERMINAL_UUID)
            return True
        except Exception as e:
            logger.error("Error during set device state %s", str(e))
            return False

    async def __get_energy_usage(self) -> Optional[Dict[str, Any]]:
        try:
            return await self.client.send_tapo_request(GetEnergyUsageMethod(None))
        except (Exception,):
            return None

    async def __get_current_power(self) -> Optional[Dict[str, Any]]:
        try:
            return await self.client.send_tapo_request(GetCurrentPowerMethod(None))
        except (Exception,):
            return None
