# pyCalor

This Python module was developed in the Department of Mechanical Engineering at the University of California, Berkeley. It is used for teaching undergraduate thermodynamics (ME40).

The software package contains classes `state` and `process`. The following is the description of their use. You can also get the built-in information by typing the following statements in the Python command line:  

`from pyCalor import thermo as th`

`print(th.state.__doc__)`   

`print(th.process.__doc__)`  


## Class **state**  

A call

`from pyCalor import thermo as th`

`st = th.state(substance, property1=value1, property2=value2, name="A")`  

creates an object of class `state`. Each such object contains the following fields:  


| - | name | description |
| :-----------: | :--------------: | :-------------------------: |
| `st.p` | pressure | (in units of kPa)  |
| `st.t` | temperature | (in units of K)  |
| `st.v` | specific volume | (in units of m3/kg)  |
| `st.u` | specific energy | (in units of kJ/kg)  |
| `st.h` | specific enthalpy | (in units of kJ/kg)  |
| `st.s` | specific entropy | (in units of kJ/kg K)  |
| `st.x` | quality | (fraction)  |
| `st.molW` | molecular weight | (in units of kg/kmol)  |
| `st.R` | gas constant | (in units of kJ/kg K)  |
| `st.substance` | 'water', 'air', 'nitrogen', ... | ()  |

The property values are in the “base units”; they can be viewed by issuing a command:

`th.state.units`

Examples:

`from pyCalor import thermo as th`

`th.state.units`

`st1 = th.state('water', p=(1,'bar'), v=0.1, name="1")`

`st1.plot("pv") # supported plots are: "pv","Ts","ph"`

`st2 = th.state('R134a', x=1, t=300, name="B")`  

`st2.plot("Ts", isoProp="v")`

`fig1 = st2.plot("Ts",isoProp="v")`

`fig1.savefig("figure_1.jpg")`

`st3 = th.state('air', p=(1,'Mpa'), t=(10,'c'))` 

`st3.name = "2a"`

This information can also be viewed in the programming environment: 

`print(th.state.__doc__)`  
  

## Class process

A call

`from pyCalor import thermo as th`

`pr = th.process([(state1,state2),(state2,state3),...])`

creates an object of class process. An object of this class represent a simple process, from `st1` to `st2`,

`pr = th.process([st1,st2])`

a simple cyclic process,

`pr = th.process([(st1,st2),(st2,st3),(st3,st4),(st4,st1)])`,

which can also be created as 

`pr = th.process(st1,st2,st3,st4,st1)`,

or any complex process, but for a single working fluid.  

You can access process object properties by the following calls

|  |  description |
| :----------- | :--------------: |
| `pr.StateList` | returns a list of `state` objects| 
| `pr.isoProp(st1,st2)` | returns a dictionary of `{isoProperty: value,...}` for process `st1` &rarr; `st2` |

Once you created process object `pr`, you can display its states on a thermodynamic diagram via  

`fig2 = pr.plot('ts')`   

to display process `pr` on a *T-s* diagram; you may likewise to make such plot in other coordinates, like `'pv'`, `'ph'`, etc.  You can also save this figure via

`fig2.savefig("figure_2.pdf")`

This information can also be viewed in the programming environment:

`print(th.process.__doc__)`

Example:

`st1 = th.state('water', p=( 1,'bar'), x=0, name="A")`

`st2 = th.state('water', p=(20,'bar'), s=st1.s,name="B")`

`st3 = th.state('water', p=(20,'bar'), x=1,name="C")`

`st4 = th.state('water', p=( 1,'bar'), s=st3.s, name="D")`

`pr = th.process([(st1,st2),(st2,st3),(st3,st4),(st4,st1)])`

`fig4 = pr.plot("pv")`

`fig4.savefig("figure_4.pdf")`

## Class hf_rec

A call

`from pyCalor import thermo as th`

`rec = th.hf_rec(substance)`

returns a record for standard enthalpy of formation of substance @ T=25 C. 

`substance` is either a name or formula; e.g., 'methanol vapor' or 'ch3oh(g)'. 

`rec` is a dictionary with 'name', 'formula', 'Hf' in kJ/kmol,  and 'molw' in kg/kmol. 

Then, to get Hf, one can use any of the following commands:

`Hf = rec['Hf']`

`Hf = rec.get('Hf')`

`Hf = th.hf_rec('c2h2').get('Hf')`

To see all substance names and formulas, use 

`th.hf_keys()`

Here's a complete working example:

`from pyCalor import thermo as th`

`rec = th.hf_rec('water')`

`Hf = rec['Hf']`
