# Nuclear Reactor Simulator

A lightweight educational **nuclear reactor simulator** implemented in Python.
It uses a simplified point-kinetics + thermal feedback model to show how
control rod movement affects reactor power and temperatures over time.

## Features

- Reactor state tracking (power, neutron population, fuel/coolant temperatures)
- Control rod insertion control (0-100%)
- Negative temperature feedback for basic stability behavior
- Time-stepped simulation demo
- Basic tests with `pytest`

## Quickstart

### 1) Run the simulator

```bash
python3 simulator.py
```

You will get CSV-like output:

- `time(s)`
- `rods(%)`
- `power(MW)`
- `fuel(C)`
- `coolant(C)`

### 2) Run tests

```bash
pytest -q
```

## Notes

This project is intentionally simplified for learning purposes and is **not**
suitable for real-world reactor design or safety analysis.
