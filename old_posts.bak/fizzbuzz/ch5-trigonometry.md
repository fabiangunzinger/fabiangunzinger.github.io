---
title: Chapter 5 - Trigonometry
---

## Circle geometry basics

(Mostly from [Wikipedia](https://en.wikipedia.org/wiki/Sine_and_cosine))

-   A chord is a stright line that runs between two points on a circle.

-   *Sine* is a mistranslation (via Arabic) of the Sanskrit word for "half-chord".

-   Cosine is a contraction of the latin "complementi sinus" -- it's the complement of the sine.

-   *$\pi$* is defined as the ratio of the circumverence and the diameter of a circle: $\pi = C / d = C / 2r$.

-   The *circumverence* of a circle is thus given by $C = 2r\pi$.

-   *Arc length* is the distance between two points along a curve. It follows from the above that it is given by: $\text{Arc length} = 2r\pi\left(\frac{\theta}{360}\right)$, where $\theta$ is the angle, in degrees, that the arc subtends at the center of the circle, and $\left(\frac{\theta}{360}\right)$ can be thought of the number of *rotations* around the circle.

-   *Radians* are a commonly used unit of angles (an alternative to degrees). One radian is defined as the angle at the center of the circle that subtends an arc of length equal to the radius of the circle.

-   Hence, in general, the magnitude of an angle expressed in radians is given by $\theta_{rad} = \frac{\text{Arch length}}{r}$, and, directly expressed as a function of degrees and rotations: $\theta_{rad} = 2\pi\left(\frac{\theta}{360}\right) = 2\pi\times\text{rotations}$.

-   It follows that a right angle is equal to $\frac{2r\pi\left(\frac{90}{360}\right)}{r} = \frac{\pi}{2}$ radians, half a rotation is $\frac{2r\pi\left(\frac{180}{360}\right)}{r} = \pi$, and a complete 360 degree rotation is equal to $\frac{2r\pi\left(\frac{360}{360}\right)}{r} = 2\pi$ radians.

-   Notice above that $\pi$, the commonly used circle constant, is equal to half a rotation. The [Tau Manifesto](https://tauday.com) argues that true circle constant is $\tau = 2\pi$. This will simplify our life a bit, so we'll use $\tau$.

``` python
import math
import checks
```

``` python
def degrees_to_radians(degrees: float) -> float:
    rotations = degrees / 360
    return rotations * 2 * math.pi

assert 3.1415 < degrees_to_radians(180) < 3.1516
```

``` python
def radians_to_degrees(radians: float) -> float:
    rotations = radians / math.pi / 2
    return 360 * rotations

assert radians_to_degrees(math.pi) == 180
```

``` python
def int_cos(theta: float) -> float:
    rotations = theta / math.tau
    
    if rotations % 1 == 0:
        # Some number of full rotations
        return 1
    elif rotations % 1 = 0.5:
        # Half a rotation
        return -1
    else:
        return 0
        
```

    3.141592653589793

``` python
def fizzbuzz(n: int) -> str:
    
    fizz = "fizz" * int(math.cos(n / 3 * math.tau))
    buzz = "buzz" * int(math.cos(n / 5 * math.tau))
    
    return (fizz + buzz) or str(n)


checks.check_function(fizzbuzz)
```
