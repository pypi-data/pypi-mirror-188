# Introduction

Evaluate pipe capacity per industry codes.

# Summary

# Usage

A quick way to running code is:
    - Create a virtual environment:
        - Use [conda yaml file](https://raw.githubusercontent.com/vamseeachanta/pipecapacity/master/dev_tools/environment.yml) to create a new environment
        - (or) by installing [pipecapacity]((https://github.com/vamseeachanta/pipecapacity)) package in an environment
- Run the following batch files
    - Download this [pipecapacity repository](https://github.com/vamseeachanta/pipecapacity)
    - activate environment
    - Change command line to "pipecapacity" (outside not in src) folder
        - Run the following python files in tests:
            - python src\digitalmodel\tests\ {change_to_relevant}.py
            - i.e. for catenary riser, python src\digitalmodel\tests\test_catenary_riser.py

**Units**

    verticalDistance: m
    declinationAngle: deg with vertical
    Temperature: deg F
    Pressure: psi
    EffectiveTension: kN
    BendingMoment: kNm
    YieldStrength: psi
    E: psi
    NominalID: inch
    NominalOD: inch
    NominalWT: inch
    Rho: kg/m3
    MassPerUnitLength: kg/m
    WeightPerUnitLength: N/m
    SoilStiffness: kN/m/m
    BuoyancyCoverage: Percentage
    ThermalExpansionCoefficient: in/in/deg F

