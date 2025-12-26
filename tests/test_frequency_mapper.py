import pytest
from terra_gaia.translator.frequency import FrequencyMapper

def test_frequency_mapping():
    mapper = FrequencyMapper()
    assert mapper.get_mapping(396)['chakra'] == 'root'
    assert mapper.get_mapping(417)['chakra'] == 'sacral'
    assert mapper.get_mapping(528)['chakra'] == 'solar_plexus'

def test_breath_patterns():
    mapper = FrequencyMapper()
    assert mapper.calculate_breath_pattern(396)['inhale'] == 6

def test_unsupported_frequency():
    mapper = FrequencyMapper()
    with pytest.raises(ValueError):
        mapper.get_mapping(9999)  # Unsupported frequency