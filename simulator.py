#!/usr/bin/env python3
"""Simple nuclear reactor core simulator.

Models neutron population, thermal power, and fuel temperature
with basic feedback and operator controls.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReactorState:
    time_s: float = 0.0
    neutron_population: float = 1.0
    power_mw: float = 100.0
    fuel_temp_c: float = 320.0
    coolant_temp_c: float = 290.0
    control_rods_pct: float = 55.0


@dataclass
class ReactorConfig:
    prompt_lifetime_s: float = 0.08
    base_reactivity: float = 0.0015
    rod_worth: float = 0.00006
    temp_feedback: float = 0.000004
    heat_capacity: float = 250.0
    heat_removal_coeff: float = 0.014
    ambient_coolant_c: float = 285.0


class ReactorSimulator:
    def __init__(self, config: ReactorConfig | None = None) -> None:
        self.config = config or ReactorConfig()
        self.state = ReactorState()

    def set_control_rods(self, insertion_pct: float) -> None:
        self.state.control_rods_pct = max(0.0, min(100.0, insertion_pct))

    def step(self, dt_s: float) -> ReactorState:
        s = self.state
        c = self.config

        # Reactivity balance: base - control rods - thermal feedback
        rod_term = c.rod_worth * s.control_rods_pct
        temp_term = c.temp_feedback * max(0.0, s.fuel_temp_c - 300.0)
        rho = c.base_reactivity - rod_term - temp_term

        # Point-kinetics-inspired power update (very simplified)
        growth = rho / c.prompt_lifetime_s
        s.neutron_population = max(0.01, s.neutron_population * (1.0 + growth * dt_s))
        s.power_mw = max(1.0, 100.0 * s.neutron_population)

        # Thermal model
        heat_in = s.power_mw
        heat_out = c.heat_removal_coeff * (s.fuel_temp_c - s.coolant_temp_c) * 100.0
        delta_temp = (heat_in - heat_out) / c.heat_capacity * dt_s
        s.fuel_temp_c += delta_temp

        coolant_rise = 0.025 * (s.fuel_temp_c - s.coolant_temp_c) * dt_s
        coolant_cooling = 0.01 * (s.coolant_temp_c - c.ambient_coolant_c) * dt_s
        s.coolant_temp_c += coolant_rise - coolant_cooling

        s.time_s += dt_s
        return ReactorState(**s.__dict__)


def run_demo(duration_s: int = 120, dt_s: float = 1.0) -> None:
    sim = ReactorSimulator()
    print("time(s),rods(%),power(MW),fuel(C),coolant(C)")

    for t in range(0, duration_s):
        if t == 20:
            sim.set_control_rods(45.0)
        if t == 60:
            sim.set_control_rods(65.0)
        st = sim.step(dt_s)
        if t % 5 == 0:
            print(
                f"{st.time_s:6.1f},{st.control_rods_pct:7.1f},"
                f"{st.power_mw:8.2f},{st.fuel_temp_c:7.2f},{st.coolant_temp_c:9.2f}"
            )


if __name__ == "__main__":
    run_demo()
