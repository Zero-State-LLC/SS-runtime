# First authoritative trace findings

Actual Simulation.step positions joined to exported source contacts. Not observed display slip. No pass/fail slip threshold.

| Case | Phase model | Travel units | Maximum contact span world | View logical px |
|---|---|---:|---:|---:|
| quarter | fixed-time | 299.967955 | 17.500534 | 8.750267 |
| quarter | distance-phase | 299.967955 | 7.000855 | 3.500427 |
| half | fixed-time | 299.967955 | 12.501068 | 6.250534 |
| half | distance-phase | 299.967955 | 6.997650 | 3.498825 |
| full | fixed-time | 299.967955 | 5.497009 | 2.748505 |
| full | distance-phase | 299.967955 | 4.997864 | 2.498932 |
| cardinal-quarter | fixed-time | 78.000000 | 19.291215 | 10.119918 |
| cardinal-quarter | distance-phase | 78.000000 | 19.982379 | 19.844996 |
| cardinal-half | fixed-time | 78.000000 | 16.972093 | 11.734274 |
| cardinal-half | distance-phase | 78.000000 | 18.839720 | 18.499561 |
| cardinal-full | fixed-time | 76.000000 | 19.982379 | 19.844996 |
| cardinal-full | distance-phase | 76.000000 | 17.848660 | 17.194292 |
| collision-stop | fixed-time | 28.000000 | 17.848660 | 17.194292 |
| collision-stop | distance-phase | 28.000000 | 17.848660 | 17.194292 |
| wall-slide | fixed-time | 223.823852 | 16.377837 | 14.629661 |
| wall-slide | distance-phase | 223.823852 | 20.153790 | 20.036959 |
| reversal | fixed-time | 299.967955 | 50.497009 | 25.248505 |
| reversal | distance-phase | 299.967955 | 46.497436 | 23.248718 |
| dodge | fixed-time | 347.962828 | 5.497009 | 2.748505 |
| dodge | distance-phase | 347.962828 | 4.997864 | 2.498932 |
| pause | fixed-time | 239.974364 | 5.497009 | 2.748505 |
| pause | distance-phase | 239.974364 | 4.997864 | 2.498932 |
| stationary | fixed-time | 0.000000 | not sampled | not sampled |
| stationary | distance-phase | 0.000000 | not sampled | not sampled |

Cardinal, slide and reversal use a deliberately held south source to expose the missing facing/contact problem, not to claim a correct facing. Idle/collision-stop and dodge do not receive fabricated walk contacts. Pause is the core no-step control only.

The source correction lowers recovery pelvis rise while retaining all foot coordinates, speed and cycle time. Therefore both source variants have identical modeled support slip. This is an honest motion-shape proposal, not a claimed slip fix. Partial-input policy remains unselected until native comparison.
