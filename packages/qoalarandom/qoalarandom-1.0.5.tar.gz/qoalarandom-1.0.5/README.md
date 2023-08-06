![Image](https://mcusercontent.com/6310a52cdfd4835b6f5b53169/images/a1f0bb87-9152-a233-d7b5-e2e75a93dc97.png)
[![License](https://img.shields.io/github/license/Qiskit/qiskit.svg?)](https://opensource.org/licenses/Apache-2.0)
<!-- ![Test and Build Status](https://github.com/hannahyelle/qoalas/actions/workflows/main.yml/badge.svg?branch=master) -->

**QoalaRandom** is a quantum powered random number generator. 

Produced by Qoalas @ iQuHack 2023

# Installation

The best way of installing `qoalarandom` is by using `pip`

```bash
$ pip install -i https://test.pypi.org/simple/ qoalarandom
```

# Using Qoala Random 

## randint(start, stop, distribution=1)

Parameters:
- start (int)
- stop (int)
- distribution (int, default=1 (uniform distribution))

    distribution is the index of the distribution type desired. See more in distribution options. 

Returns: A random integer between start and stop 

## randrange(start, stop, step=1, distribution=1)

Parameters: 
- start (int)
- stop (int)
- step (int, default=1)
- distribution (int, default=1 (uniform distribution))

    distribution is the index of the distribution type desired. See more in distribution options.

Returns: A random integer between start and stop incrementing by step

## randfloat(start, stop, distribution=1)

Parameters: 
- start (int)
- stop (int)
- distribution (int, default=1 (uniform distribution))

    distribution is the index of the distribution type desired. See more in distribution options.

Returns: A random float between start and stop 

## randchoice(user_list, distribution=1)

Parameters:
- user_list (list)
- distribution (int, default=1 (uniform distribution))

    distribution is the index of the distribution type desired. See more in distribution options.

Returns: A random element of user_list

# Distribution Options
## 0 = normal
To extract the random numbers from a normal distribution (centred at 0, variance = 1)
## 1 = uniform 
To extract the random numbers from a uniform distribution
## 2 = porterthomas 
To extract the random numbers from a Porter-Thomas distribution
## 3 = deeprandom
To fully take advantage of the quantum circuit, creating a circuit that exploit statistical propertier of dual-unitary circuits to generate a number extracted uniformly from the Haar distribution (approximated according to the amount of resources requested to the QPU)