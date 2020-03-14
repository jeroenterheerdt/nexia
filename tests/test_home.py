"""Tests for Nexia Home."""

import json
import os
from os.path import dirname
import unittest

from nexia.home import NexiaHome


def load_fixture(filename):
    """Load a fixture."""
    test_dir = dirname(__file__)

    path = os.path.join(test_dir, "fixtures", filename)
    with open(path) as fptr:
        return fptr.read()


class TestNexiaThermostat(unittest.TestCase):
    """Tests for nexia thermostat."""

    def test_update(self):
        nexia = NexiaHome(auto_login=False)
        house_json = json.loads(load_fixture("mobile_houses_123456.json"))
        nexia.update_from_json(house_json)
        thermostat = nexia.get_thermostat_by_id(2059661)
        zone_ids = thermostat.get_zone_ids()
        self.assertEqual(zone_ids, [83261002, 83261005, 83261008, 83261011])
        nexia.update_from_json(house_json)
        zone_ids = thermostat.get_zone_ids()
        self.assertEqual(zone_ids, [83261002, 83261005, 83261008, 83261011])
        nexia.update_from_json(house_json)

    def test_idle_thermo(self):
        """Get methods for an idle thermostat."""
        nexia = NexiaHome(auto_login=False)
        house_json = json.loads(load_fixture("mobile_houses_123456.json"))
        nexia.update_from_json(house_json)

        thermostat = nexia.get_thermostat_by_id(2059661)

        self.assertEqual(thermostat.get_thermostat_model(), "XL1050")
        self.assertEqual(thermostat.get_thermostat_firmware(), "5.9.1")
        self.assertEqual(thermostat.get_thermostat_dev_build_number(), "1581321824")
        self.assertEqual(thermostat.get_thermostat_device_id(), "000000")
        self.assertEqual(thermostat.get_thermostat_type(), "XL1050")
        self.assertEqual(thermostat.get_thermostat_name(), "Downstairs East Wing")
        self.assertEqual(thermostat.get_deadband(), 3)
        self.assertEqual(thermostat.get_setpoint_limits(), (55, 99))
        self.assertEqual(thermostat.get_variable_fan_speed_limits(), (0.35, 1.0))
        self.assertEqual(thermostat.get_unit(), "F")
        self.assertEqual(thermostat.get_humidity_setpoint_limits(), (0.35, 0.65))
        self.assertEqual(thermostat.get_fan_mode(), "auto")
        self.assertEqual(thermostat.get_outdoor_temperature(), 88.0)
        self.assertEqual(thermostat.get_relative_humidity(), 0.36)
        self.assertEqual(thermostat.get_current_compressor_speed(), 0.0)
        self.assertEqual(thermostat.get_requested_compressor_speed(), 0.0)
        self.assertEqual(thermostat.get_fan_speed_setpoint(), 0.35)
        self.assertEqual(thermostat.get_dehumidify_setpoint(), 0.50)
        self.assertEqual(thermostat.has_dehumidify_support(), True)
        self.assertEqual(thermostat.has_humidify_support(), False)
        self.assertEqual(thermostat.get_system_status(), "System Idle")
        self.assertEqual(thermostat.get_air_cleaner_mode(), "auto")
        self.assertEqual(thermostat.is_blower_active(), False)

        zone_ids = thermostat.get_zone_ids()
        self.assertEqual(zone_ids, [83261002, 83261005, 83261008, 83261011])

    def test_active_thermo(self):
        """Get methods for an active thermostat."""
        nexia = NexiaHome(auto_login=False)
        house_json = json.loads(load_fixture("mobile_houses_123456.json"))
        nexia.update_from_json(house_json)

        thermostat = nexia.get_thermostat_by_id(2293892)

        self.assertEqual(thermostat.get_thermostat_model(), "XL1050")
        self.assertEqual(thermostat.get_thermostat_firmware(), "5.9.1")
        self.assertEqual(thermostat.get_thermostat_dev_build_number(), "1581321824")
        self.assertEqual(thermostat.get_thermostat_device_id(), "0281B02C")
        self.assertEqual(thermostat.get_thermostat_type(), "XL1050")
        self.assertEqual(thermostat.get_thermostat_name(), "Master Suite")
        self.assertEqual(thermostat.get_deadband(), 3)
        self.assertEqual(thermostat.get_setpoint_limits(), (55, 99))
        self.assertEqual(thermostat.get_variable_fan_speed_limits(), (0.35, 1.0))
        self.assertEqual(thermostat.get_unit(), "F")
        self.assertEqual(thermostat.get_humidity_setpoint_limits(), (0.35, 0.65))
        self.assertEqual(thermostat.get_fan_mode(), "auto")
        self.assertEqual(thermostat.get_outdoor_temperature(), 87.0)
        self.assertEqual(thermostat.get_relative_humidity(), 0.52)
        self.assertEqual(thermostat.get_current_compressor_speed(), 0.69)
        self.assertEqual(thermostat.get_requested_compressor_speed(), 0.69)
        self.assertEqual(thermostat.get_fan_speed_setpoint(), 0.35)
        self.assertEqual(thermostat.get_dehumidify_setpoint(), 0.45)
        self.assertEqual(thermostat.has_dehumidify_support(), True)
        self.assertEqual(thermostat.has_humidify_support(), False)
        self.assertEqual(thermostat.get_system_status(), "Cooling")
        self.assertEqual(thermostat.get_air_cleaner_mode(), "auto")
        self.assertEqual(thermostat.is_blower_active(), True)

        zone_ids = thermostat.get_zone_ids()
        self.assertEqual(zone_ids, [83394133, 83394130, 83394136, 83394127, 83394139])


class TestNexiaHome(unittest.TestCase):
    """Tests for nexia home."""

    def test_basic(self):
        """Basic tests for NexiaHome."""
        nexia = NexiaHome(auto_login=False)
        house_json = json.loads(load_fixture("mobile_houses_123456.json"))
        nexia.update_from_json(house_json)

        thermostat_ids = nexia.get_thermostat_ids()
        self.assertEqual(thermostat_ids, [2059661, 2059676, 2293892, 2059652])


class TestNexiaThermostatZone(unittest.TestCase):
    """Tests for nexia thermostat zone."""

    def test_zone_relieving_air(self):
        """Tests for nexia thermostat zone relieving air."""
        nexia = NexiaHome(auto_login=False)
        house_json = json.loads(load_fixture("mobile_houses_123456.json"))
        nexia.update_from_json(house_json)

        thermostat = nexia.get_thermostat_by_id(2293892)
        zone = thermostat.get_zone_by_id(83394133)

        self.assertEqual(zone.thermostat, thermostat)

        self.assertEqual(zone.get_name(), "Bath Closet")
        self.assertEqual(zone.get_cooling_setpoint(), 79)
        self.assertEqual(zone.get_heating_setpoint(), 63)
        self.assertEqual(zone.get_current_mode(), "AUTO")
        self.assertEqual(
            zone.get_requested_mode(), "AUTO",
        )
        self.assertEqual(
            zone.get_presets(), ["None", "Home", "Away", "Sleep"],
        )
        self.assertEqual(
            zone.get_preset(), "None",
        )
        self.assertEqual(
            zone.get_status(), "Relieving Air",
        )
        self.assertEqual(
            zone.get_setpoint_status(), "Permanent Hold",
        )

    def test_zone_cooling_air(self):
        """Tests for nexia thermostat zone cooling."""
        nexia = NexiaHome(auto_login=False)
        house_json = json.loads(load_fixture("mobile_houses_123456.json"))
        nexia.update_from_json(house_json)

        thermostat = nexia.get_thermostat_by_id(2293892)
        zone = thermostat.get_zone_by_id(83394130)

        self.assertEqual(zone.get_name(), "Master")
        self.assertEqual(zone.get_cooling_setpoint(), 71)
        self.assertEqual(zone.get_heating_setpoint(), 63)
        self.assertEqual(zone.get_current_mode(), "AUTO")
        self.assertEqual(
            zone.get_requested_mode(), "AUTO",
        )
        self.assertEqual(
            zone.get_presets(), ["None", "Home", "Away", "Sleep"],
        )
        self.assertEqual(
            zone.get_preset(), "None",
        )
        self.assertEqual(
            zone.get_status(), "Damper Open",
        )
        self.assertEqual(
            zone.get_setpoint_status(), "Permanent Hold",
        )