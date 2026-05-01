from simulator import ReactorSimulator


def test_rods_reduce_power():
    sim = ReactorSimulator()
    for _ in range(30):
        sim.step(1.0)
    baseline_power = sim.state.power_mw

    sim.set_control_rods(80.0)
    for _ in range(20):
        sim.step(1.0)

    assert sim.state.power_mw < baseline_power


def test_temperature_stays_positive():
    sim = ReactorSimulator()
    for _ in range(120):
        sim.step(0.5)
    assert sim.state.fuel_temp_c > 0
    assert sim.state.coolant_temp_c > 0
