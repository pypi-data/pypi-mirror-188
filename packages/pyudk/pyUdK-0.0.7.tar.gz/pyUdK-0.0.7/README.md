# pyUdK


This library provides Udwadia Kalaba constrained parameters and force quantities for Python 3 out of the box. The usage is mostly based on numpy and sympy library.

## Installation

Just run

    pip install pyUdK


## Usage
### Basic usage

The simplest, though not very useful usage would be

    import Udk
    Q = Udk.ideal_Constraint_force(m, q, A, b)
