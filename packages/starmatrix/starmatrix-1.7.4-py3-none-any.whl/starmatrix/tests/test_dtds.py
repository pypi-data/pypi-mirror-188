import pytest
import numpy as np
import starmatrix.settings as settings
import starmatrix.functions as functions
import starmatrix.constants as constants
from starmatrix.dtds import select_dtd
from starmatrix.dtds import dtd_capped_at_max_mass
from starmatrix.dtds import dtd_correction
from starmatrix.dtds import dtd_ruiz_lapuente
from starmatrix.dtds import dtd_maoz_graur
from starmatrix.dtds import dtd_castrillo
from starmatrix.dtds import dtd_greggio
from starmatrix.dtds import dtd_close_dd_04
from starmatrix.dtds import dtd_close_dd_1
from starmatrix.dtds import dtd_wide_dd_04
from starmatrix.dtds import dtd_wide_dd_1
from starmatrix.dtds import dtd_sd_chandra
from starmatrix.dtds import dtd_sd_subchandra
from starmatrix.dtds import dtd_chen
from starmatrix.dtds import dtds_strolger


@pytest.fixture
def available_dtds():
    """
    Fixture returning the names of all available DTDs defined in settings
    """
    return settings.valid_values["dtd_sn"]


def test_dtds_presence(available_dtds):
    for dtd in available_dtds:
        assert select_dtd(dtd) is not None


def test_select_dtd(available_dtds):
    dtds = [dtd_ruiz_lapuente, dtd_maoz_graur, dtd_castrillo, dtd_greggio, dtd_chen,
            dtd_close_dd_04, dtd_close_dd_1, dtd_wide_dd_04, dtd_wide_dd_1, dtd_sd_chandra, dtd_sd_subchandra,
            dtds_strolger["fit_1"], dtds_strolger["fit_2"], dtds_strolger["fit_3"], dtds_strolger["fit_4"],
            dtds_strolger["fit_5"], dtds_strolger["optimized"]]

    assert len(available_dtds) == len(dtds)

    for i in range(len(available_dtds)):
        times = [0, 0.001, 0.04, 0.1, 0.4, 1, 2, 9.] + list(np.random.rand(5)) + list(np.random.rand(5) * 9)
        for time in times:
            assert select_dtd(available_dtds[i])(time) == dtds[i](time)


def test_no_negative_time_values():
    t = -1
    assert dtd_ruiz_lapuente(t) == 0.0
    assert dtd_maoz_graur(t) == 0.0
    assert dtd_close_dd_04(t) == 0.0
    assert dtd_close_dd_1(t) == 0.0
    assert dtd_wide_dd_04(t) == 0.0
    assert dtd_wide_dd_1(t) == 0.0
    assert dtd_sd_chandra(t) == 0.0
    assert dtd_sd_subchandra(t) == 0.0


def test_dtd_correction_factor():
    assert dtd_correction({}) == 1.0
    assert dtd_correction({'dtd_correction_factor': 3.0}) == 3.0


def test_dtd_capped_at_max_mass(available_dtds):
    min_age = functions.stellar_lifetime(7, 0.02)
    min_age_default_m_max = functions.stellar_lifetime(constants.B_MAX, 0.02)
    lower_mass_age = functions.stellar_lifetime(constants.B_MIN, 0.02)

    for dtd_name in available_dtds:
        dtd = select_dtd(dtd_name)
        dtd_capped = dtd_capped_at_max_mass(dtd, 0.02, 7)
        assert dtd_capped(min_age - 0.001) == 0.0
        assert dtd_capped(min_age) == dtd(min_age)
        assert dtd_capped(lower_mass_age) == dtd(lower_mass_age)
        dtd_capped_default_m_max = dtd_capped_at_max_mass(dtd, 0.02)
        assert dtd_capped_default_m_max(min_age_default_m_max - 0.001) == 0.0
        assert dtd_capped_default_m_max(min_age_default_m_max) == dtd(min_age_default_m_max)
        assert dtd_capped_default_m_max(lower_mass_age) == dtd(lower_mass_age)
