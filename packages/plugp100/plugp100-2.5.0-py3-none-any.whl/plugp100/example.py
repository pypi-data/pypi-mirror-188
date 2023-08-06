import asyncio

from plugp100 import TapoApiClient, TapoApiClientConfig
from plugp100.domain.light_effect import LightEffectPreset


async def main():
    # create generic tapo api
    config = TapoApiClientConfig("<ip>", "<email>", "<passwd>")
    sw = TapoApiClient.from_config(config)
    await sw.login()
    await sw.off()
    state = await sw.get_state()
    print(state.firmware_version)
    print(state.is_hardware_v2)

    # color temperature and brightness
    await sw.set_color_temperature(4000)
    await sw.set_brightness(100)

    # light effect example
    await sw.set_light_effect(LightEffectPreset.rainbow().effect)
    state = await sw.get_state()
    energy_info = await sw.get_energy_usage()
    power_info = await sw.get_power_info()
    print(state.get_unmapped_state())
    print(energy_info and energy_info.get_unmapped_state())
    print(power_info and power_info.get_unmapped_state())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
