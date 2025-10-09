# CalorAI
Language Model Being Developed for Teaching ME40, Thermodynamics, at UC Berkeley. 

Instructors: Prof. Hail and Prof. Schutzius. 

The data here is used for fine-tuning and retrieval augmented generation (RAG) of the small language or large language model. We are currently training a small language model Phi-3. Information on how to setup and do simple fine-tuning and RAG for Phi-3 can be found on [OskiBot](https://github.com/ucb-me-40/OskiBot).

## Housekeeping
The primary purpose of this SLM is to aid students in studying thermodynamics. Based on student feedback, we believe that most of the prompts will be copying and pasting the homework question and then searching for course resources to help them study and enable them to solve the problems on their own. An additional use is if a student gets the answer correct, they can check to see if their logic was correct or if there are alternative solutions. The resources created by the instructional staff are organized as follows:

```
CalorAI
+--data
|	`-- fine_tune_conversations.jsonl
|	`-- rag_corpus.txt
|	+-- book
|	|	`-- cengel_9th_toc.json
|	|	`-- cengel_10th_toc.json
|	+-- courseInstances
|	|	+-- Fa23
|	|	|-- Fa24
|	|	|-- Sp25
|	|	|-- Fa25
|	|	|	`-- syllabus.json
|	|	|	+--lecture-01a
|	|	|	|	`-- 1_mtmivyvl.srt
|	|	|	|	`-- 555352862 - 1_mtmivyvl - PID 2640881.json
|	|	|	|	`-- 555352862 - 1_mtmivyvl - PID 2640881.txt
|	|	|	|	`-- outline.json
|	|	|	+-- ...
|	+-- examples
|	|	+-- _archive
|	|	+-- jupyterNotebooks
|	|	|	`-- nitrogenHeatingWorkTransfer.ipynb
|	|	|	`-- ...
|	+-- homework
|	|	+-- _archive
|	|	+-- jupyterNotebooks
|	|	|	`-- notebook.ipynb
|	|	|	`-- ...
+--scripts
|	`-- _convert_notebooks_to_rag.py
|	`-- _convert_outlines_to_rag.py
|	`-- _convert_toc_to_rag.py
|	`-- _generate_base_corpus.py
|	`-- 1_create_rag_index.py
|	`-- 2_fine_tune_phi3.py
|	`-- 3_run_chatbot.py
```

### cengel_*_toc.json
The `cengel_*_toc.json` file should contain the table of contents for that specific edition.  

### syllabus.json
The `syllabus.json` file should contain the syllabus for the current semester formatted as a JSON file. This will need to be converted into corpus chunks and added to `rag_corpus.txt`. 

### courseInstances 
This folder contains data from each semester that the course is taught. This includes the syllabus and the captions from the recorded lectures (`.srt`, `.json`, `.txt` files). We create an outline.json file and define subtopics within the lecture. Those subtopics have a time_range, which is easy to define if you watch the recordings. There is a feature on bCourses, which allows you to create bookmarks. We used that to generate the `time_range` field entries. You should also tag those bookmarks, e.g., `Fa25-L1a-1.0`. This will also help students to navigate to the correct part of the video as they only have to enter that tag into the search and they will find the correct part of the video. This part is a non-trivial amount of work, but we believe it is essential for student learning. We don't recommend just uploading the closed caption data and asking it to create  an `outline.json` file. If an example is solved during lecture, We recommend having the solution in a Jupyter notebook and placed in the `examples/jupyterNotebooks` folder. 

The `"subtopics"` `"tags"` `"alpha"` means that the `"subtopics"` is ready for review by the GSI or Reader. The `"tags"` `"beta"` means that the `"subtopics"` is ready for review by the Instructor. LaTeX equations will be formatted differently in a `.json` file. Each `\` requires another `\`, i.e., `\\`. The script `_convert_outlines_to_rag.py` is able to convert from JSON to LaTeX formatted equations and add them to the `rag_corpus.txt`.

Original LaTeX entry in the Jupyter notebook: `$\mathbf{h_{\text{in}} = h_{\text{out}}}$` 

Needs to be written as in the `outline.json` file: `$\\mathbf{h_{\\text{in}} = h_{\\text{out}}}$`

Here is an example of an input outline.json file, which doesn't include `"detailed_summary"`:

```json
{
  "lectureId": "1_97hqf37r",
  "instructor": "tschutzius",
  "year": "Fa25",
  "courseCaptureId": "rtl_course_capture_2258_29147",
  "lecture": "05c",
  "title": "Mass and Energy Analysis of Control Volumes",
  "videoTitle": "ME40 - 22 Sept 2025 - Lecture 5c (edited)",
  "module": "module-one",
  "topic": "Control Volumes",
  "subtopics": [
    {
      "key": "Fa25-L5c-1.0",
      "title": "Throttling and Expansion Valves",
      "summary": "In this problem, Prof. Schutzius analyzes a throttling process. This is an important component of a refrigeration system.",
      "time_range": "00:28 - 19:45",
      "topics": ["Control Volumes","Refrigeration"],
      "detailed_summary": "",
      "examples": ["throttlingPyCalor"],
      "tags":["tschutzius","beta"]
    },
    {
      "key": "Fa25-L5c-2.0",
      "title": "Heat Exchanger",
      "summary": "Example: Energy analysis of a steady flow system: Heat exchanger: R134a refrigerant. It enters a heat exchanger as a vapor with a mass flow rate of 6 kg/min and leaves as a subcooled liquid. Neglect pressure drops. Determine the mass flow rate of the cooling water and the heat transfer rate from the refrigerant to the water.",
      "time_range": "19:46 - 41:14",
      "topics": ["Control Volumes"],
      "detailed_summary": "",
      "examples": ["heatExchangerPyCalor"],
      "tags":["tschutzius","beta"]
    },
    {
      "key": "Fa25-L5c-3.0",
      "title": "Energy analysis of unsteady flow processes",
      "summary": "Prof. Schutzius explains how one can analyze an unsteady flow process.",
      "time_range": "41:15 - 50:26",
      "topics": ["Control Volumes"],
      "detailed_summary": "",
      "examples": ["co2ReliefModeling"],
      "tags":["tschutzius","beta"]
    }
  ]
}
```

I then use Gemini or a large language model (LLM) to create a detailed summary for those subtopics:

```
I am teaching undergraduate thermodynamics to mechanical engineers. I am recording my lectures, which also includes closed captions. I've attached the closed caption files, formatted in .srt, .txt, and .json. I have also included an outline file, outline.json, which includes 3 subtopics from the lecture. Each subtopic has a key, title, summary, time_range, topics, detailed_summary, examples, and tags. I would like you to write a detailed summary for each subtopic during the "time_range" and place it in the corresponding "detailed_summary" field. If the "summary" field is blank, please also write a short summer. Please do not change any of the other fields in the outline.json file. Thank you.
```

Here is an example of the output:

```json
{
  "lectureId": "1_97hqf37r",
  "instructor": "tschutzius",
  "year": "Fa25",
  "courseCaptureId": "rtl_course_capture_2258_29147",
  "lecture": "05c",
  "title": "Mass and Energy Analysis of Control Volumes",
  "videoTitle": "ME40 - 22 Sept 2025 - Lecture 5c (edited)",
  "module": "module-one",
  "topic": "Control Volumes",
  "subtopics": [
    {
      "key": "Fa25-L5c-1.0",
      "title": "Throttling and Expansion Valves",
      "summary": "In this problem, Prof. Schutzius analyzes a throttling process. This is an important component of a refrigeration system.",
      "time_range": "00:28 - 19:45",
      "topics": ["Control Volumes","Refrigeration"],
      "detailed_summary": "The segment focuses on **throttling valves/expansion valves** within a refrigeration cycle, emphasizing that it is an **isenthalpic process** ($\\mathbf{h_{\\text{in}} = h_{\\text{out}}}$). This condition is met by assuming **no work** and **no heat transfer** (adiabatic/insulated, which is valid for a small orifice or porous plug). This expansion causes a temperature decrease, known as the **Joule-Thompson effect**. The process is visualized on a **pressure-enthalpy (p-h) diagram**, where a saturated liquid at high pressure ($x=0$) expands along a constant enthalpy line into a two-phase liquid-vapor mixture at lower pressure.",
      "examples": ["throttlingPyCalor"],
      "tags":["tschutzius","beta"]
    },
    {
      "key": "Fa25-L5c-2.0",
      "title": "Heat Exchanger",
      "summary": "Example: Energy analysis of a steady flow system: Heat exchanger: R134a refrigerant. It enters a heat exchanger as a vapor with a mass flow rate of 6 kg/min and leaves as a subcooled liquid. Neglect pressure drops. Determine the mass flow rate of the cooling water and the heat transfer rate from the refrigerant to the water.",
      "time_range": "19:46 - 41:14",
      "topics": ["Control Volumes"],
      "detailed_summary": "The segment analyzes a **heat exchanger** under **Steady-Flow Energy Analysis (SFEA)**. The overall energy balance for the adiabatic heat exchanger simplifies to $\\mathbf{\\sum \\dot{m}_{\\text{in}} h_{\\text{in}} = \\sum \\dot{m}_{\\text{out}} h_{\\text{out}}}$. Applying this to the two streams (refrigerant, $R$, and water, $w$): $\\mathbf{\\dot{m}_R (h_1 - h_2) = \\dot{m}_w (h_4 - h_3)}$. The problem involves determining the mass flow rate of the cooling water ($\\dot{m}_w$) and the heat transfer rate from the refrigerant to the water ($\\mathbf{\\dot{Q}_{\\text{out}} = \\dot{m}_R (h_1 - h_2)}$), which is also equal to the heat gained by the water ($\\mathbf{\\dot{Q}_{\\text{in}} = \\dot{m}_w (h_4 - h_3)}$).",
      "examples": ["heatExchangerPyCalor"],
      "tags":["tschutzius","beta"]
    },
    {
      "key": "Fa25-L5c-3.0",
      "title": "Energy analysis of unsteady flow processes",
      "summary": "Prof. Schutzius explains how one can analyze an unsteady flow process.",
      "time_range": "41:15 - 50:26",
      "topics": ["Control Volumes"],
      "detailed_summary": "The segment introduces **unsteady-flow analysis**, where **mass and energy within the Control Volume (CV) change over time** (e.g., tank charging/discharging). The governing equations are the **General Mass Balance** ($\\mathbf{\\dot{m}_{\\text{in}} - \\dot{m}_{\\text{out}} = \\frac{dm_{\\text{CV}}}{dt}}$) and the **General Energy Balance**.",
      "examples": ["co2ReliefModeling"],
      "tags":["tschutzius","beta"]
    }
  ]
}
```

The `"examples"` field are existing files located in the `examples` folder and are formatted as `.json` files. 


| JSON Field    | Output Format in `rag_corpus.txt` | 
| -------- 		| ------- 					|
| `lecture` (e.g., "01a"), `title`  | `### LECTURE 01A: Class plan and rules; Challenges in Decarbonizing our Energy`   |
| `subtopics[].title` | `**Concept:** Course learning objectives`     |
| `subtopics[].summary`    | `**Summary:** The course objectives focus on understanding and applying the First and Second Laws of Thermodynamics, moving from foundational concepts and simple problems to analyzing bigger systems and thermodynamic data using Python.`    |
| `subtopics[].detailed_summary` | `**Detailed Explanation:** The main learning objectives are centered on mastering the First and Second Laws of Thermodynamics to the point of being able to articulate them clearly...`     |
| `subtopics[].time_range` | `**Time Range:** 02:19 - 03:43`     |

An example of the output block for Lecture 01a, Subtopic 3.0:
```
### LECTURE 01A: Class plan and rules; Challenges in Decarbonizing our Energy
**Concept:** Course learning objectives
**Summary:** The course objectives focus on understanding and applying the First and Second Laws of Thermodynamics, moving from foundational concepts and simple problems to analyzing bigger systems and thermodynamic data using Python.
**Detailed Explanation:** The main learning objectives are centered on mastering the **First and Second Laws of Thermodynamics** to the point of being able to articulate them clearly. Students will first solve simple, single-answer problems involving both laws. The course then transitions to applying these laws to much bigger systems, including the study of **perpetual motion cycles** (cycles that violate the First and Second Laws). A key modern component is the shift from using old-school appendix tables to utilizing **Python modules** for handling and determining thermodynamic data, which is presented as a crucial skill for the course.
**Time Range:** 02:19 - 03:43
---
```

### examples
This folder should contain all of the problems solved in lecture. The file should originally be written in a Jupyter notebook, and then converted to a `.json` file. In the future it may be worthwhile to consider going directly from Jupyter notebooks to `rag_corpus.txt`. From there we will add it to `rag_corpus.txt`. 

What is important here is the `"workflow_tags"`. If a problem has not been reviewed, you should write
```json
"workflow_tags": ["draft"]
```

If the problem has been reviewed, you should write `"reviewed"` and say who checked it:
```json
"workflow_tags": ["reviewed", "tschutzius"],
```

Example of the original Jupyter notebook:
```
## Problem Metadata 
DO NOT DELETE. This is a JSON Block. The metadata and course context MUST be in the first cell. 
```

```json
{
    "problem_title": "Isentropic nitrogen compressor",
    "author": "tschutzius",
    "year": "Fa25",
    "difficulty_tags": ["easy"],
	"workflow_tags": ["draft"],
    "topic": "Entropy",
    "lecture_reference": {
        "lecture_id": "",
        "subtopics": [
            {
                "key": "Fa25-L7c-5.0",
                "title": "Air property tables: Compressor example",
            }
        ]
    },
    "book_reference": {
        "chapter_number": 7,
        "title": "Entropy",
        "sections": [
            "Isentropic Processes"
        ]
    },
    "notes": "."
}
```

```
## 1. Problem Statement
Nitrogen enters an adiabatic compressor at $p_1 =$ 110 kPa and $T_1 =$ 30 $^\circ$ C and exits at $p_2 =$ 682 kPa. The process is reversible. 

**Goal:** Determine the work input per unit mass, $\frac{\dot{W}_\text{in}}{\dot{m}}$.

## 2. Schematic 

Draw a schematic that shows a compressor. Draw the control volume around the compressor. There is a single inlet and oulet for mass to flow in and out. Indicate that it is adiabatic and that work is being transferred in. 

## 3. Assumptions and Approximations
* **Control Volume** (mass crosses the boundary).
* Nitrogen can be treated as an ideal gas. So we can use $T dS$ relations assuming constant specific heats. We can also use pyCalor to determine properties. We will do both and compare our answers.
* Neglect kinetic and potential energy ($\Delta KE \approx 0$, $\Delta PE \approx 0$).
* **Reversible process**.
* **Adiabatic process**.
* **Steady-flow process** ($\Delta m_\text{CV}= 0$, $\Delta E_\text{CV}= 0$, $\Delta S_\text{CV}= 0$).
* We have a single inlet and outlet ($\dot{m}_\text{in}$ and $\dot{m}_\text{out}$).

## 4. Physical Laws
1.  **First Law of Thermodynamics (Energy Balance for Control Volume):**
    $$\frac{dE_\text{CV}}{dt} = \dot{E}_\text{in} - \dot{E}_\text{out}$$

2.  **Conservation of Mass (Mass Balance for a Control Volume):**
    $$\frac{dm_\text{CV}}{dt} = \dot{m}_\text{in} - \dot{m}_\text{out}$$

Since this is a steady flow process, we can write:
$$\dot{E}_\text{in} = \dot{E}_\text{out}$$

$$\dot{m}_\text{in} = \dot{m}_\text{out} = \dot{m}$$

We can write our conservation of energy equation as:
$$\dot{W}_\text{in} + \dot{Q}_\text{in} + \dot{m} \left(h_1 + \frac{w_1^2}{2} + g z_1 \right) = \dot{W}_\text{out} + \dot{Q}_\text{out} + \dot{m} \left(h_2 + \frac{w_1^2}{2} + g z_2 \right)$$

Neglecting kinetic and potential energy effects we can write:
$$\dot{W}_\text{in} + \dot{Q}_\text{in} + \dot{m} \left(h_1 \right) = \dot{W}_\text{out} + \dot{Q}_\text{out} + \dot{m} \left(h_2 \right)$$

Applying the adiabatic assumption:
$$\dot{W}_\text{in} + \dot{m} \left(h_1 \right) = \dot{W}_\text{out} + \dot{m} \left(h_2 \right)$$

Rearranging:
$$ \frac{\dot{W}_\text{out} - \dot{W}_\text{in}}{\dot{m}} = h_1 - h_2$$

We expect that work is only transferred out, so $\dot{W}_\text{out} = 0$. We can then write:

$$\frac{\dot{W}_\text{in}}{\dot{m}} = h_2 - h_1$$

We know $h_1$ because we have the properties at state 1. We need additional information in order to determine state 2. Since the compressor is reversible and adiabatic (no heat transfer in), then the process is isentropic. Therefore:

$$s_2 = s_1$$

We can use this information to determine the enthalpy at state 2. 

### Alternative solution

We can determine the temperature at state 2 by using the $TdS$ relations. For an ideal gas undergoing an isentropic (reversible and adiabatic) process, we can write:

$$\left( \frac{T_2}{T_1} \right)_{s = const} = \left(\frac{p_2}{p_1} \right)^{(k-1)/k} $$

Recall that $k = c_p/c_v$, so to do this calculation we have to select the $k$ at some temperature. We can choose the temperature at the inlet state. By knowing $T_1$, $p_1$, and $p_2$, we can determine $T_2$. 

For an ideal gas, changes in enthalpy can be expressed as:

$$h_2 - h_1 = c_p \left(T_2 - T_1 \right) $$

Again, we have to select a specific heat at some temperature. We can take the inlet temperature. 
```

```python
## 5. Properties (Code Cell)
try:
    __import__('pyCalor')
    print(f"Package '{'pyCalor'}' is already installed.")
except ImportError:
    print(f"Package '{'pyCalor'}' not found. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "!pip", "install", pyCalor])
        print(f"Package '{'pyCalor'}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing '{'pyCalor'}': {e}")
        sys.exit(1) # Exit if installation fails

from pyCalor import thermo as th

# Constants and Initial State
p1_kPa = 110 # kPa
T1_C = 30 # C
T1_K = T1_C + 273.15

p2_kPa = 682 # MPa

substance = 'nitrogen'

# Determine state 1
st1 = th.state(substance,T=(T1_C,'C'),p=(p1_kPa,'kPa'),name='1')
s1_kJperKgPerK = st1.s
h1_kJperKg = st1.h
cp_kJperKgPerK = st1.cp
cv_kJperKgPerK = st1.cv
k = cp_kJperKgPerK/cv_kJperKgPerK

# Determine state 2
s2_kJperKgPerK = s1_kJperKgPerK
st2 = th.state(substance,s=(s2_kJperKgPerK,'kJ/kg K'),p=(p2_kPa,'kPa'),name='2')
h2_kJperKg = st2.h

## Alternative solution
T2_K_alt = T1_K*(p2_kPa/p1_kPa)**((k-1)/k)

# 6 Calculations (Code Cell)
wIn_kJperKg = h2_kJperKg - h1_kJperKg

print(f"Work input per unit mass: {wIn_kJperKg:.2f} kJ/kg")

wIn_kJperKg_alt = cp_kJperKgPerK*(T2_K_alt - T1_K)

print(f"Work input per unit mass assuming ideal gas and using TdS relations: {wIn_kJperKg_alt:.2f} kJ/kg")
```

```
## 7. 💡 Summary and Reasoning

By separating flow work from total work to form the property enthalpy, the work term we calculate is then useful shaft work. The work out per unit mass is a simple formula: 

$$\frac{\dot{W}_\text{in}}{\dot{m}} = h_2 - h_1$$

* **Key Insight:** For a steady flow system undergoing an **adiabatic** and **reversible** process, this can be considered as an isentropic process. That is useful because it allows us to determine the exit state of the turbine since we also know the exit pressure. 

* **Alternative Solution** If we assume ideal gas behavior, and if the process is isentropic (reversible and adiabatic) then we can write:

$$\frac{\dot{W}_\text{in}}{\dot{m}} = c_p \left( T_2 - T_1 \right)$$

For that we have to select specific heats at a certain temperature. We chose the inlet temperature. That turned out to be a good assumption. This approach is simpler and is a good way to first solve the problem. One can check if it is a good assumption by determining actual property values using `pyCalor`.
```

We can then run `_convert_notebooks_to_rag.py` to conver the Jupyter notebook into corpus chunks that are appended to the `rag_corpus.txt` file. 

```
---
### PROBLEM: nitrogenHeatingWorkTransfer
**Source:** Jupyter Notebook (nitrogenHeatingWorkTransfer.ipynb)
**Topic:** Closed Systems
**Lecture References:** Lecture ID: 1_3375c5yj, Key: Fa25-L4c-2.0 (Electrical heating and cooling of a cylinder containing nitrogen at constant pressure)
**Book Reference:** Book Ch. 4: Energy Analysis of Closed Systems

#### Discussion / Problem Statement:
## 7. Summary and Reasoning

We see that the values for $T_2$ are the same for two different approaches. The assumption of constant specific heat values appears to be a good one.

#### Solution Code:
```
```python
# 5. Properties (Code Cell)
!pip install pyCalor
from pyCalor import thermo as th

R_JperKgPerK = 296.8
V1_m3 = 0.5
p1_Pa = 400e3
T1_K = 27+273.15
substance = 'nitrogen'

# determine state 1 using pyCalor
st1 = th.state(substance,T=(T1_K,'K'),p=(400,'kpa'),name='1')
h1_JperKg = st1.h*1e3

# determine the mass in the piston using the ideal gas law
m_kg = (p1_Pa*V1_m3)/(R_JperKgPerK*T1_K); print(m_kg)

Qout_J = 2800
Volt_V = 120
I_A = 2
t_s = 5*60
```

```python
# 6 Calculations (Code Cell)

Win_J = Volt_V*I_A*t_s; print(Win_J)

h2_JperKg = h1_JperKg + ((Win_J - Qout_J)/m_kg)
h2_kJperKg = h2_JperKg/1e3

# by knowing h2, we can determine state 2 using pyCalor
st2 = th.state(substance,p=(p1_Pa/1e3,'kpa'),h=h2_kJperKg,name='2')

# final answer, T2
T2_C = st2.T-273.15
print(T2_C)

# alternative solution
cp_N2_JperKgPerK = 1.039*1e3

T2_K_ = T1_K + ((Win_J - Qout_J)/(cp_N2_JperKgPerK*m_kg))
print(T2_K_-273.15)

error = (T2_K_ - st2.T)/st2.T; 
print(error*100)
```

#### Final Summary / Reasoning:
## 7. Summary and Reasoning

We see that the values for $T_2$ are the same for two different approaches. The assumption of constant specific heat values appears to be a good one.

```

Alternatively, you can ask Gemini to convert this into a complete corpus chunk. For `nitrogenHeatingWorkTransfer`, this then looks like:

```
### WORKED EXAMPLE: nitrogenHeatingWorkTransfer (Closed Systems)
**Reference:** Lecture: Electrical heating and cooling of a cylinder containing nitrogen at constant pressure (Fa25-L4c-2.0). Textbook: Chapter 4: Energy Analysis of Closed Systems.

## Problem Statement
Nitrogen ($N_2$) is contained in a piston-cylinder device. An electrical resistor heats the gas while a fan stirs it. During this process, $2.8 \text{ kJ}$ of heat is removed from the system ($Q_{\text{out}}$). Assume the gas is ideal with constant specific heat and is undergoing a constant-pressure process ($P_1 = P_2$).

**Given Data:**
* Substance: Nitrogen ($N_2$)
* Mass: $m = 1 \text{ kg}$
* Initial Pressure: $P_1 = 100 \text{ kPa}$
* Initial Temperature: $T_1 = 20^\circ \text{C}$
* Electrical Work Input: $W_{\text{elect}, \text{in}} = 2.4 \text{ kJ}$
* Heat Outflow: $Q_{\text{out}} = 2.8 \text{ kJ}$

**Goal:** Determine the final temperature of the nitrogen, $T_2$ in Celsius.

## Physical Basis & Governing Laws
This is a **closed system** (fixed mass) undergoing a **constant pressure process** ($P_1 = P_2$). The primary governing principle is the **First Law of Thermodynamics (Energy Balance)** for a closed system:

$$\Delta E = Q_{\text{net}} - W_{\text{net}}$$

Since the process is constant pressure, the **Boundary Work** ($W_b = P \Delta V$) can be absorbed into the internal energy term, simplifying the expression to a **change in Enthalpy ($\Delta H$)** in terms of **net heat and other forms of work:**

$$m(h_2 - h_1) = Q_{\text{net}} - W_{\text{net, other}}$$

Where:
* $Q_{\text{net}} = Q_{\text{in}} - Q_{\text{out}} = -2.8 \text{ kJ}$
* $W_{\text{net, other}} = W_{\text{elect}, \text{in}} = 2.4 \text{ kJ}$

The final enthalpy $h_2$ is the solution to the energy balance, which can then be used with the final pressure $P_2$ to find the final temperature $T_2$ using fluid property tables (or `pyCalor`).

## Solution Code and Calculations (pyCalor)
The following Python code uses the `pycalor` library to solve the problem using the energy balance approach.
```

```python
import pycalor as th

# --- 1. Inputs and State 1 Initialization ---
substance = 'nitrogen'
m_kg = 1.0
p1_Pa = 100*1e3 # Pa
T1_C = 20
Qout_kJ = 2.8
Win_kJ = 2.4
T1_K = T1_C + 273.15

# Determine State 1 properties (using p and T)
st1 = th.state(substance, p=(p1_Pa/1e3,'kpa'), T=T1_K, name='1')
h1_JperKg = st1.h*1e3 # Enthalpy at state 1 in J/kg
print('h1: {0:1.2f} J/kg'.format(h1_JperKg))

# --- 2. Energy Balance Calculation ---
# Convert energy transfers to Joules
Win_J = Win_kJ*1e3
Qout_J = Qout_kJ*1e3

# Apply Energy Balance (solving for h2): 
# m*h2 = (W_other - Q_out) + m*h1
h2_JperKg = ( (Win_J - Qout_J) + m_kg*h1_JperKg ) / m_kg
h2_kJperKg = h2_JperKg / 1e3

# --- 3. Determine Final State 2 ---
# Find final temperature (T2) using p2 and h2
st2 = th.state(substance, p=(p1_Pa/1e3,'kpa'), h=h2_kJperKg, name='2')

# Final Answer: T2 in deg C
T2_C = st2.T - 273.15
print('Final Temperature T2: {0:1.2f} deg C'.format(T2_C))

# --- 4. Alternative Solution (using constant specific heat) for error check ---
cp_N2_JperKgPerK = 1.039*1e3 # Specific heat for Nitrogen

# T2 = T1 + (Q_net - W_other) / (m * c_p)
T2_K_cp_approx = T1_K + ((Win_J - Qout_J) / (cp_N2_JperKgPerK * m_kg))

# print(T2_K_cp_approx - 273.15) # Should be very close to T2_C

# --- 5. Summary and Conclusion---

Result: The final temperature of the nitrogen, $T_2$, is determined by the net change in enthalpy caused by the electrical work input and the heat loss.
Key Insight: The use of the enthalpy balance $m(h_2 - h_1 )=Q_{net} - W_{net,other}$ is the most efficient way to analyze a closed system at constant pressure, as it implicitly accounts for the boundary work term. The electrical work, $W_{elect,in}$, is treated as a positive work input to the system.

```

Instead of converting the Jupyter notebooks to corpus chunks, we could instead convert them to JSON files. Here is the prompt I then gave Gemini:
```
I am attaching here a Jupyter notebook which I would like to use for retrieval-augmented generation (RAG) or fine-tuning the a small language model. The notebook has been broken down into chunks according to:

1. Problem Statement
2. Schematic
3. Assumptions and approximations
4. Physical Laws
5. Properties
6. Calculations
7. Summary and Reasoning

Appropriate metadata has been included in Problem Metadata formatted as a JSON Block. I would now like you to convert this Jupyter notebook to a JSON file using the following steps:

1. Please first extract the metadata. Parse the first Markdown cell to retrieve the initial JSON block. Use these values to populate the top-level keys and the course_reference object.

2. Concatenate Code: Combine the content of all subsequent Code Cells into the solution_code array, using the suggested step_name labels for clarity.

3. Preserve LaTeX: Ensure that any LATE​X math notation (text enclosed in $ or $$ delimiters) is preserved exactly as it appears in the Markdown source cells, particularly in the physical_laws_and_assumptions and pedagogical_summary fields.

4. Clean Prose: Remove all Markdown formatting (e.g., #, **, ---, *) from the extracted non-code/non-JSON text fields (problem_statement_raw, physical_laws_and_assumptions, pedagogical_summary).
```

Example of the converted `.json` file:
```json
{
  "uuid": "8a7c2b0d-4f1e-45a9-9c3f-7e0d3f2c1b42",
  "problem_title": "Isentropic nitrogen compressor",
  "topic": "Entropy",
  "tags": [
    "easy"
  ],
  "workflow_tags": ["draft"],
  "course_reference": {
    "book_reference": {
      "chapter_number": 7,
      "title": "Entropy",
      "sections": [
        "Isentropic Processes"
      ]
    },
    "lecture_reference": {
      "lecture_id": "",
      "subtopics": [
        {
          "key": "Fa25-L7c-5.0",
          "title": "Air property tables: Compressor example"
        }
      ]
    }
  },
  "problem_statement_raw": "Nitrogen enters an adiabatic compressor at $p_1 =$ 110 kPa and $T_1 =$ 30 $^\\circ$ C and exits at $p_2 =$ 682 kPa. The process is reversible. Goal: Determine the work input per unit mass, $\\frac{\\dot{W}_\\text{in}}{\\dot{m}}$. Draw a schematic that shows a compressor. Draw the control volume around the compressor. There is a single inlet and oulet for mass to flow in and out. Indicate that it is adiabatic and that work is being transferred in.",
  "physical_laws_and_assumptions": "Control Volume (mass crosses the boundary). Nitrogen can be treated as an ideal gas. So we can use $T dS$ relations assuming constant specific heats. We can also use pyCalor to determine properties. We will do both and compare our answers. Neglect kinetic and potential energy ($\\Delta KE \\approx 0$, $\\Delta PE \\approx 0$). Reversible process. Adiabatic process. Steady-flow process ($\\Delta m_\\text{CV}= 0$, $\\Delta E_\\text{CV}= 0$, $\\Delta S_\\text{CV}= 0$). We have a single inlet and outlet ($\\dot{m}_\\text{in}$ and $\\dot{m}_\\text{out}$). 1. First Law of Thermodynamics (Energy Balance for Control Volume): $$\\frac{dE_\\text{CV}}{dt} = \\dot{E}_\\text{in} - \\dot{E}_\\text{out}$$ 2. Conservation of Mass (Mass Balance for a Control Volume): $$\\frac{dm_\\text{CV}}{dt} = \\dot{m}_\\text{in} - \\dot{m}_\\text{out}$$ Since this is a steady flow process, we can write: $$\\dot{E}_\\text{in} = \\dot{E}_\\text{out}$$ $$\\dot{m}_\\text{in} = \\dot{m}_\\text{out} = \\dot{m}$$ We can write our conservation of energy equation as: $$\\dot{W}_\\text{in} + \\dot{Q}_\\text{in} + \\dot{m} \\left(h_1 + \\frac{w_1^2}{2} + g z_1 \\right) = \\dot{W}_\\text{out} + \\dot{Q}_\\text{out} + \\dot{m} \\left(h_2 + \\frac{w_1^2}{2} + g z_2 \\right)$$ Neglecting kinetic and potential energy effects we can write: $$\\dot{W}_\\text{in} + \\dot{Q}_\\text{in} + \\dot{m} \\left(h_1 \\right) = \\dot{W}_\\text{out} + \\dot{Q}_\\text{out} + \\dot{m} \\left(h_2 \\right)$$ Applying the adiabatic assumption: $$\\dot{W}_\\text{in} + \\dot{m} \\left(h_1 \\right) = \\dot{W}_\\text{out} + \\dot{m} \\left(h_2 \\right)$$ Rearranging: $$ \\frac{\\dot{W}_\\text{out} - \\dot{W}_\\text{in}}{\\dot{m}} = h_1 - h_2$$ We expect that work is only transferred out, so $\\dot{W}_\\text{out} = 0$. We can then write: $$\\frac{\\dot{W}_\\text{in}}{\\dot{m}} = h_2 - h_1$$ We know $h_1$ because we have the properties at state 1. We need additional information in order to determine state 2. Since the compressor is reversible and adiabatic (no heat transfer in), then the process is isentropic. Therefore: $$s_2 = s_1$$ We can use this information to determine the enthalpy at state 2. Alternative solution We can determine the temperature at state 2 by using the $TdS$ relations. For an ideal gas undergoing an isentropic (reversible and adiabatic) process, we can write: $$\\left( \\frac{T_2}{T_1} \\right)_{s = const} = \\left(\\frac{p_2}{p_1} \\right)^{(k-1)/k} $$ Recall that $k = c_p/c_v$, so to do this calculation we have to select the $k$ at some temperature. We can choose the temperature at the inlet state. By knowing $T_1$, $p_1$, and $p_2$, we can determine $T_2$. For an ideal gas, changes in enthalpy can be expressed as: $$h_2 - h_1 = c_p \\left(T_2 - T_1 \\right) $$ Again, we have to select a specific heat at some temperature. We can take the inlet temperature.",
  "solution_code": [
    {
      "step_name": "initial_setup_and_properties",
      "code_block": "## 5. Properties (Code Cell)\n!pip install pyCalor\nfrom pyCalor import thermo as th\n\n# Constants and Initial State\np1_kPa = 110 # kPa\nT1_C = 30 # C\nT1_K = T1_C + 273.15\n\np2_kPa = 682 # MPa\n\nsubstance = 'nitrogen'\n\n# Determine state 1\nst1 = th.state(substance,T=(T1_C,'C'),p=(p1_kPa,'kPa'),name='1')\ns1_kJperKgPerK = st1.s\nh1_kJperKg = st1.h\ncp_kJperKgPerK = st1.cp\ncv_kJperKgPerK = st1.cv\nk = cp_kJperKgPerK/cv_kJperKgPerK\n\n# Determine state 2\ns2_kJperKgPerK = s1_kJperKgPerK\nst2 = th.state(substance,s=(s2_kJperKgPerK,'kJ/kg K'),p=(p2_kPa,'kPa'),name='2')\nh2_kJperKg = st2.h\n\n## Alternative solution\nT2_K_alt = T1_K*(p2_kPa/p1_kPa)**((k-1)/k)"
    },
    {
      "step_name": "final_calculation_logic",
      "code_block": "# 6 Calculations (Code Cell)\nwIn_kJperKg = h2_kJperKg - h1_kJperKg\n\nprint(f\"Work input per unit mass: {wIn_kJperKg:.2f} kJ/kg\")\n\nwIn_kJperKg_alt = cp_kJperKgPerK*(T2_K_alt - T1_K)\n\nprint(f\"Work input per unit mass assuming ideal gas and using TdS relations: {wIn_kJperKg_alt:.2f} kJ/kg\")"
    }
  ],
  "pedagogical_summary": "By separating flow work from total work to form the property enthalpy, the work term we calculate is then useful shaft work. The work out per unit mass is a simple formula: $$\\frac{\\dot{W}_\\text{in}}{\\dot{m}} = h_2 - h_1$$ Key Insight: For a steady flow system undergoing an adiabatic and reversible process, this can be considered as an isentropic process. That is useful because it allows us to determine the exit state of the turbine since we also know the exit pressure. Alternative Solution If we assume ideal gas behavior, and if the process is isentropic (reversible and adiabatic) then we can write: $$\\frac{\\dot{W}_\\text{in}}{\\dot{m}} = c_p \\left( T_2 - T_1 \\right)$$ For that we have to select specific heats at a certain temperature. We chose the inlet temperature. That turned out to be a good assumption. This approach is simpler and is a good way to first solve the problem. One can check if it is a good assumption by determining actual property values using `pyCalor`."
}

```
This then needs to be converted into a "Prompt/Completion" pair. For that I gave Gemini the following prompt and uploaded the files I listed:

```
I am interested in using a small language model to improve student learning in the thermodynamics course I am teaching. The goal of the model would be to help students study more efficiently. It is common in thermodynamics for students to not even know where to start with solving a problem. Therefore, if a student has a homework problem they are stuck on, they can ask the model (prompt), and then the model can suggest (reply) what material to read, what exercise problems to review, what lecture videos to watch, etc., so that the students can best prepare in order to be able to solve the problem. 

I am providing here: 
- book chapter and section titles (tableOfContents.json)
- captions from my previous lecture videos. I have taken these files and created outline.json files from them. I’ve attached an example for the first module of the course (outline-module-one.json).
- JSON files based on Jupyter notebooks from problems I have solved in class. I’ve attached an example (nitrogenHeatingWorkTransfer.json).
- pyCalor REDME.md file (thermodynamic property module)
- course syllabus (syllabus.json)

I would like to follow a scaffolding approach for the prompts and completions which relies on three different training functions:
- level_1: --- Level 1: Conceptual Strategy / Study Guide ---
- level_2: --- Level 2: Specific Hint / Next Step ---
- level_3: --- Level 3: Full Solved Example ---

Can you create a JSONL file with such prompts and completions for the nitrogenHeatingWorkTransfer.json example?

I would like to use this JSONL file to fine-tune an open source model (Phi-3). I have already set up the Phi-3 model to tune. I have a HP Z4 workstation with an NVIDIA GPU which I can use to do the training. It has Ubuntu installed.
```

Here is the reply:

```
{"prompt": "--- Level 1: Conceptual Strategy / Study Guide ---\n\nA piston cylinder contains nitrogen initially at 400 kPa, 27\u00b0C, and 0.5 m\u00b3. The piston contains a resistor. The pressure in the piston is kept constant while 120 V is applied to the resistor resulting in 2 A flowing through it for 5 min. The piston is also cooled, transferring 2800 J out. Goal: Determine the final temperature, T\u2082.", "completion": "The key to this problem is to apply the **First Law of Thermodynamics (Energy Balance)** to the system.\n\n### \u26a1\ufe0f Conceptual Strategy\n1.  **Identify the System and Process:** The system is a **Closed System** (piston-cylinder, no mass transfer). The process is **constant pressure**.\n2.  **Apply the First Law:** Since pressure is constant, the boundary work ($W_{boundary}$) is related to $\\Delta (PV)$. This allows the energy balance to be written in terms of the change in **Enthalpy ($\u0394H$):** $\u0394H = Q_{net} - W_{net, other}$.\n3.  **Calculate Initial Properties:** Use the Ideal Gas Law to find the mass ($m$) of nitrogen at State 1.\n4.  **Calculate Energy Transfers:** Calculate the electrical work input ($W_{electrical}$).\n\n### \u2705 Study Guide\n\n| Material | Reference | Topic | \n| :--- | :--- | :--- |\n| **Book Chapter** | Chapter 4: **Energy Analysis of Closed Systems** | Provides the core theory for this problem type. |\n| **Book Section** | Section 4-1: **Moving Boundary Work** | To understand the $P dV$ work that simplifies the energy equation. |\n| **Book Section** | Section 4-4: **Internal Energy, Enthalpy, and Specific Heats of Ideal Gases** | Required for the assumption $\u0394H = m c_p \\u0394T$ (Ideal Gas). |\n| **Lecture Video** | **Electrical heating and cooling of a cylinder containing nitrogen at constant pressure** (Fa25-L4c-2.0, cited in problem) | A direct example of this problem type. |\n| **Lecture Video** | **Introduction to the first law of thermodynamics** (L1a, 19:13 - 40:13) | Review of the foundational conservation of energy principle. |\n| **Software** | **pyCalor (README.md)** | Review the `state` class documentation to find the Gas Constant ($R$) or Specific Heat ($c_p$) for nitrogen, as properties are needed for the calculation. |"}
{"prompt": "--- Level 2: Specific Hint / Next Step ---\n\nA piston cylinder contains nitrogen initially at 400 kPa, 27\u00b0C, and 0.5 m\u00b3. The piston contains a resistor. The pressure in the piston is kept constant while 120 V is applied to the resistor resulting in 2 A flowing through it for 5 min. The piston is also cooled, transferring 2800 J out. Goal: Determine the final temperature, T\u2082. \n\nWhat is the very first key calculation I need to perform, and what is the simplified energy balance equation for this process?", "completion": "The very first key calculation is to determine the **mass ($m$)** of the nitrogen.\n\n### \u2192 Step 1: Calculate Mass ($m$)\n\nSince nitrogen is treated as an ideal gas, use the Ideal Gas Law:\n\n$$\\text{Mass}: m = \\frac{P_1 V_1}{R_{\\text{Nitrogen}} T_1}$$\n\n**(Hint:** Remember to convert the initial temperature $T_1 = 27^\circ \\text{C}$ to Kelvin, and use $R_{\\text{Nitrogen}} \u2248 296.8 \\text{ J/kg}\u00b7\\text{K}$).\n\n### \u2192 Step 2: Simplified Energy Balance\n\nFor a closed system undergoing a constant pressure process ($\u0394P = 0$), the First Law of Thermodynamics, $\u0394E = Q_{net} - W_{net}$, simplifies by combining $\u0394U$ and $W_{boundary}$ into the change in Enthalpy ($\u0394H$):\n\n$$\\text{Core Equation: } m(h_2 - h_1) = W_{in, electrical} - Q_{out}$$\n\nIf you assume constant specific heats (Ideal Gas approximation), this simplifies further to solve for $\u0394T$:\n\n$$\\text{Working Equation: } m c_p (T_2 - T_1) = V I t - Q_{out}$$"}
{"prompt": "--- Level 3: Full Solved Example ---\n\nA piston cylinder contains nitrogen initially at 400 kPa, 27\u00b0C, and 0.5 m\u00b3. The piston contains a resistor. The pressure in the piston is kept constant while 120 V is applied to the resistor resulting in 2 A flowing through it for 5 min. The piston is also cooled, transferring 2800 J out. Goal: Determine the final temperature, T\u2082. \n\nShow me the full, step-by-step solution, including the calculations.", "completion": "This problem requires applying the First Law of Thermodynamics for a closed system, making use of the enthalpy formulation due to the constant pressure process.\n\n### \u2795 Step 1: State Variables and Mass Calculation\n\n**Given:**\n* $P_1 = 400 \\text{ kPa} = 400 \\times 10^3 \\text{ Pa}$\n* $T_1 = 27^\circ \\text{C} = 300.15 \\text{ K}$\n* $V_1 = 0.5 \\text{ m}^3$\n* $V_{resistor} = 120 \\text{ V}$\n* $I = 2 \\text{ A}$\n* $t = 5 \\text{ min} = 300 \\text{ s}$\n* $Q_{out} = 2800 \\text{ J}$\n* Gas Constant for Nitrogen: $R_{\\text{Nitrogen}} \u2248 296.8 \\text{ J/kg}\u00b7\\text{K}$ (from properties table or pyCalor)\n\n**Mass ($m$):** Using the Ideal Gas Law $m = \\frac{P_1 V_1}{R T_1}$:\n\n$$m = \\frac{(400 \\times 10^3 \\text{ Pa})(0.5 \\text{ m}^3)}{(296.8 \\text{ J/kg}\u00b7\\text{K})(300.15 \\text{ K})} \u2248 2.247 \\text{ kg}$$\n\n### \u2795 Step 2: Calculate Work and Heat Transfers\n\n**Electrical Work Input ($W_{\\text{in}}$):**\n\n$$W_{\\text{in}} = W_{\\text{electrical}} = V I t = (120 \\text{ V})(2 \\text{ A})(300 \\text{ s}) = 72000 \\text{ J}$$\n\n**Net Energy Transfer:**\n\n$$\\text{Net Energy} = W_{\\text{in}} - Q_{\\text{out}} = 72000 \\text{ J} - 2800 \\text{ J} = 69200 \\text{ J}$$\n\n### \u2795 Step 3: Apply Energy Balance to Solve for $T_2$\n\nThe energy balance for a constant pressure process ($\u0394P = 0$) in a closed system simplifies to the enthalpy change, $\u0394H = Q_{net} - W_{net, other}$. Treating Nitrogen as an Ideal Gas with constant specific heat $c_p \u2248 1040 \\text{ J/kg}\u00b7\\text{K}$:\n\n$$m c_p (T_2 - T_1) = W_{\\text{in}} - Q_{\\text{out}}$$\n\nSolving for $T_2$:\n\n$$T_2 = T_1 + \\frac{W_{\\text{in}} - Q_{\\text{out}}}{m c_p}$$\n\n$$T_2 = 300.15 \\text{ K} + \\frac{69200 \\text{ J}}{(2.247 \\text{ kg})(1040 \\text{ J/kg}\u00b7\\text{K})} \\approx 300.15 \\text{ K} + 29.62 \\text{ K}$$\n\n$$\\text{Final Temperature, } T_2 \u2248 329.77 \\text{ K} \\u2248 56.62^\circ \\text{C}$$"}
``` 

For now we are only using the `examples` for corpus chunks to be added to `rag_corpus.txt`. 

### Homework
Building on the workflow mentioned above, where we go from Jupyter notebook to JSON to JSONL, I will first generate a JSON file from the PrairieLearn problems. I created a single file that contains all of the examples done in class, `examples.json`. I also converted the syllabus to a JSON file, `syllabus.json` as well as the table of contents for the book, `tableOfContents.json`. I also have the `pyCalor` README file. Finally, I have the entire outline of my lecture audio recordings, organized by subtopics, in a single file `outline-module-one.json`. Upload those files and the PrairieLearn files (`question.html`, `server.py`, and `info.json`) to Gemini, and enter this prompt as well as the PrairieLearn files:

```
I am teaching undergraduate thermodynamics to mechanical engineers. I teach the course in three modules. The students do their homework on PrairieLearn. I would like to use my homework problems programmed on PrairieLearn for use in fine-tuning and retrieval augmented generation in the small language model. I have uploaded here the following files for the problem nozzleConvergingDiverging-noID:
- question.html: This is where the problem question is located. 
- server.py: The numerical solution is typically in this file.
- info.json: The problem "title", "topic", "tags" (e.g., easy, medium, hard) and other problem metadata is located in this file.
- README: `pyCalor` is a python module that allows students to determine thermodynamic properties. 
- outline-module-one.json: The course outline for Module 1, including "topics" and "subtopics" is located in this file. If possible, references should be made to those "subtopics". Also mentioned in the subtopics are the "examples" that have been solved. See the file "examples.json" for the example "problem_title".
- syllabus.json: The course syllabus for Fall 2025.
- tableOfContents.json: The table of contents of the book used in the course.
- examples.json. Contains the problems and solutions for all exercises done in Module 1 of the course.

Is it possible for you to create a single .json file formatted in a way that is ideal for fine-tuning and RAG? 

If possible, references should be made to relevant book chapter(s) and section(s), exercises, and lecture subtopics

Please cleanup the formatting:
The numerical values that are displayed in the question.html file are formatted as: {{params.p1_MPa}}. It would be best if we could convert those to their variables, e.g., {{params.p2_MPa}} to $p_1$; {{params.T1_C}} to $T_1$; {{params.mdot12_kgPerS}} to $\dot{m}_{12}$; etc. 

The students should use `pyCalor` to determine thermodynamic properties and not IAPWS or CoolProp. I'm attaching the README for `pyCalor`.
```

Here is the reply from Gemini (be sure to check the "key" and "title" for the lecture reference; for me it was the right "key" but it hallucinated a "title"):
``` json
{
  "problem_id": "nozzleConvergingDiverging-noID",
  "metadata": {
    "title": "Nozzle (Steady-Flow Device)",
    "topic": "Control Volumes",
    "difficulty_tags": ["medium", "Fa25"]
  },
  "problem_statement": {
    "question_summary": "Determine the exit area of a converging-diverging nozzle.",
    "raw_problem": "Steam enters a converging-diverging nozzle operating at steady state with an inlet pressure $p_1$, an inlet temperature $T_1$, and an inlet velocity $w_1$. The steam flows through the nozzle with **negligible heat transfer** ($\dot{Q} \\approx 0$) and **no significant change in potential energy** ($\\Delta PE \\approx 0$). At the exit, the pressure is $p_2$ and the velocity is $w_2$. The mass flow rate is $\\dot{m}$.",
    "given_variables_mapping": [
      {"variable": "$p_1$", "placeholder": "{{params.p1}}", "units": "kPa"},
      {"variable": "$T_1$", "placeholder": "{{params.T1}}", "units": "$^\\circ$C"},
      {"variable": "$w_1$", "placeholder": "{{params.vel1}}", "units": "m/s"},
      {"variable": "$p_2$", "placeholder": "{{params.p2}}", "units": "kPa"},
      {"variable": "$w_2$", "placeholder": "{{params.vel2}}", "units": "m/s"},
      {"variable": "$\\dot{m}$", "placeholder": "{{params.mdot}}", "units": "kg/s"}
    ],
    "goal": "Determine the exit area of the nozzle, $A_2$ (in m$^2$).",
    "system_assumptions": [
      "**Steady-Flow System** (Mass and Energy within the CV are constant over time)",
      "Single-Inlet, Single-Outlet",
      "No Work Transfer ($\dot{W}=0$)",
      "Adiabatic ($\dot{Q} \\approx 0$)",
      "Negligible Potential Energy Change ($\\Delta PE \\approx 0$)"
    ]
  },
  "solution_guide": {
    "governing_laws": [
      "Conservation of Mass (Continuity Equation)",
      "First Law of Thermodynamics (Energy Balance for a Steady-Flow Control Volume)"
    ],
    "energy_balance_equation": "The First Law for a steady-flow, adiabatic, no-work, negligible $\\Delta PE$ process simplifies to:\n$$\\dot{m} \\left(h_1 + \\frac{w_1^2}{2} \\right) = \\dot{m} \\left(h_2 + \\frac{w_2^2}{2} \\right)$$\n$$h_1 + \\frac{w_1^2}{2} = h_2 + \\frac{w_2^2}{2}$$",
    "mass_balance_equation": "The continuity equation is used to relate the flow rate to the area:\n$$\\dot{m} = \\frac{1}{v} A w \quad \\implies \quad A_2 = \\frac{\\dot{m} v_2}{w_2}$$",
    "solution_steps": [
      "**Step 1: Calculate Exit Enthalpy ($h_2$)**\nSolve the energy equation for $h_2$: $h_2 = h_1 + \\frac{w_1^2 - w_2^2}{2}$.\n*Use $h_1$ and $p_1$ with `pyCalor` to find the inlet specific enthalpy $h_1$.*",
      "**Step 2: Determine Exit Specific Volume ($v_2$)**\nUse the calculated exit enthalpy ($h_2$) and the known exit pressure ($p_2$) to determine the specific volume ($v_2$) at the exit state, using the **`pyCalor`** module for Steam (Water).",
      "**Step 3: Calculate Exit Area ($A_2$)**\nUse the specific volume, mass flow rate, and exit velocity: $A_2 = \\frac{\\dot{m} v_2}{w_2}$."
    ]
  },
  "property_module": {
    "name": "**pyCalor**",
    "usage_note": "Thermodynamic properties **must** be determined using the **`pyCalor`** Python module (not IAPWS or CoolProp). The required fields are $h$ (specific enthalpy in kJ/kg), $p$ (pressure in kPa), and $v$ (specific volume in m$^3$/kg).\n\nProperties are retrieved using the `state` class: `st = th.state(substance, property1=value1, property2=value2, name=\"A\")`."
  },
  "references": {
    "course_outline_module_1": {
      "key": "Fa25-L5c-1.0",
      "title": "Throttling and Expansion Valves",
      "lecture_topic": "Control Volumes",
      "context": "This subtopic covers the analysis of several **steady-flow devices**, including **nozzles and diffusers**."
    },
    "textbook_reference": {
      "book_title": "Thermodynamics: An Engineering Approach (Ninth Edition)",
      "chapter_number": 5,
      "chapter_title": "Mass and Energy Analysis of Control Volumes",
      "sections": [
        "Steady-Flow Processes",
        "Some Steady-Flow Engineering Devices"
      ]
    },
    "related_course_example": {
      "example_title": "heatExchangerPyCalor",
      "lecture_subtopic_key": "Fa25-L5c-2.0",
      "description": "Another Module 1 problem applying the First Law to a steady-flow device (Heat Exchanger)."
    }
  }
}

```

After you've run the prompt once, if you stay in the same chat you can write:
```
I have uploaded the following files for the problem turbineAdiabaticFeedwaterHeating-C9-5-57:
- question.html: This is where the problem question is located. 
- server.py: The numerical solution is typically in this file.
- info.json: The problem "title", "topic", "tags" (e.g., easy, medium, hard) and other problem metadata is located in this file.

I already uploaded the following files:
- README: `pyCalor` is a python module that allows students to determine thermodynamic properties. 
- outline-module-one.json: The course outline for Module 1, including "topics" and "subtopics" is located in this file. If possible, references should be made to those "subtopics". Also mentioned in the subtopics are the "examples" that have been solved. See the file "examples.json" for the example "problem_title".
- syllabus.json: The course syllabus for Fall 2025.
- tableOfContents.json: The table of contents of the book used in the course.
- examples.json. Contains the problems and solutions for all exercises done in Module 1 of the course.

Is it possible for you to create a single .json file formatted in a way that is ideal for fine-tuning and RAG? 

If possible, references should be made to relevant book chapter(s) and section(s), exercises, and lecture subtopics

Please cleanup the formatting:
The numerical values that are displayed in the question.html file are formatted as: {{params.p1_MPa}}. It would be best if we could convert those to their variables, e.g., {{params.p2_MPa}} to $p_1$; {{params.T1_C}} to $T_1$; {{params.mdot12_kgPerS}} to $\dot{m}_{12}$; etc. 

The students should use `pyCalor` to determine thermodynamic properties and not IAPWS or CoolProp. I'm attaching the README for `pyCalor`.
```

The response:

```
{
  "problem_id": "turbineAdiabaticFeedwaterHeating-C9-5-57",
  "metadata": {
    "title": "Turbine with Feedwater Heating (Multi-Stream CV)",
    "topic": "Control Volumes",
    "difficulty_tags": ["medium", "Fa25"],
    "course_module": "Module 1 (First Law)"
  },
  "problem_statement": {
    "question_summary": "Determine the work output of an adiabatic steam turbine that bleeds a portion of its steam for feedwater heating.",
    "raw_problem": "An **adiabatic steam turbine** ($\dot{Q} \\approx 0$) operates with steam entering at state 1, splitting at state 2, and the remaining stream exiting at state 4. Assume **negligible kinetic and potential energy changes** ($\\Delta KE \\approx 0$, $\\Delta PE \\approx 0$).\n\n**Given conditions:**\n* Inlet (State 1): $p_1$ and $T_1$ with mass flow rate $\\dot{m}_{12}$.\n* Bleed (State 2): $p_2$ and $T_2$ with mass flow rate $\\dot{m}_{\\text{bleed}}$.\n* Exit (State 4): $p_4$ and $T_4$.",
    "given_variables_mapping": [
      {"variable": "$p_1$", "placeholder": "{{params.p1_MPa}}", "units": "MPa"},
      {"variable": "$T_1$", "placeholder": "{{params.T1_C}}", "units": "$^\\circ$C"},
      {"variable": "$\\dot{m}_{12}$", "placeholder": "{{params.mdot12_kgPerS}}", "units": "kg/s"},
      {"variable": "$p_2$", "placeholder": "{{params.p2_MPa}}", "units": "MPa"},
      {"variable": "$T_2$", "placeholder": "{{params.T2_C}}", "units": "$^\\circ$C"},
      {"variable": "$\\dot{m}_{\\text{bleed}}$", "placeholder": "{{params.mdotbleed_kgPerS}}", "units": "kg/s"},
      {"variable": "$p_4$", "placeholder": "{{params.p4_MPa}}", "units": "MPa"},
      {"variable": "$T_4$", "placeholder": "{{params.T4_C}}", "units": "$^\\circ$C"}
    ],
    "goal": "Determine the work output of the turbine, $\\dot{W}_{\\text{out}}$ (in MW).",
    "system_assumptions": [
      "**Steady-Flow System** (Mass and Energy within the CV are constant over time)",
      "One Inlet (1) and Two Outlets (2, 4)",
      "Adiabatic ($\dot{Q} \\approx 0$)",
      "Negligible Kinetic and Potential Energy Changes ($\Delta KE \\approx 0, \Delta PE \\approx 0$)"
    ]
  },
  "solution_guide": {
    "governing_laws": [
      "Conservation of Mass (Continuity Equation)",
      "First Law of Thermodynamics (Energy Balance for a Steady-Flow Control Volume)"
    ],
    "mass_balance_equation": "The total mass flow rate in must equal the total mass flow rate out, where $\\dot{m}_{34}$ is the mass flow rate leaving at state 4:\n$$\\dot{m}_{12} = \\dot{m}_{\\text{bleed}} + \\dot{m}_{34}$$",
    "energy_balance_equation": "The First Law for this multi-stream, adiabatic, steady-flow device simplifies to:\n$$\\sum_{\\text{in}} \\dot{m} h = \\dot{W}_{\\text{out}} + \\sum_{\\text{out}} \\dot{m} h$$ \n$$\\dot{m}_{12} h_1 = \\dot{W}_{\\text{out}} + \\dot{m}_{\\text{bleed}} h_2 + \\dot{m}_{34} h_4$$",
    "solution_steps": [
      "**Step 1: Determine Enthalpies**\nUse the given $p$ and $T$ conditions for states 1, 2, and 4 to find the specific enthalpies $h_1$, $h_2$, and $h_4$ (in kJ/kg) using **`pyCalor`**.",
      "**Step 2: Calculate Mass Flow Rate $\\dot{m}_{34}$**\nApply the mass balance: $\\dot{m}_{34} = \\dot{m}_{12} - \\dot{m}_{\\text{bleed}}$ (in kg/s).",
      "**Step 3: Calculate Work Output $\\dot{W}_{\\text{out}}$**\nSolve the energy balance equation for the work output (power):\n$$\\dot{W}_{\\text{out}} = \\dot{m}_{12} h_1 - \\dot{m}_{\\text{bleed}} h_2 - \\dot{m}_{34} h_4$$\n*The result must be converted from $\\text{kJ/s}$ (kW) to $\\text{MW}$ for the final answer.*"
    ]
  },
  "property_module": {
    "name": "**pyCalor**",
    "usage_note": "Thermodynamic properties **must** be determined using the **`pyCalor`** Python module. The required fields for calculation are specific enthalpy ($h$ in kJ/kg), pressure ($p$), and temperature ($T$ in $^\\circ$C or K).\n\nProperties are retrieved using the `state` class, e.g., `st1 = th.state('water', p=(p1,'MPa'), T=(T1,'C'), name='1')`."
  },
  "references": {
    "course_outline_module_1": {
      "key": "Fa25-L5b-2.0",
      "title": "**Energy Analysis of a Steady-flow System**",
      "lecture_topic": "Control Volumes",
      "context": "This subtopic provides the framework for applying the First Law to all steady-flow devices, including the turbine examined in this problem."
    },
    "textbook_reference": {
      "book_title": "Thermodynamics: An Engineering Approach (Ninth Edition)",
      "chapter_number": 5,
      "chapter_title": "Mass and Energy Analysis of Control Volumes",
      "sections": [
        "Steady-Flow Processes",
        "Some Steady-Flow Engineering Devices"
      ]
    },
    "related_course_example": {
      "example_title": "heatExchangerPyCalor",
      "lecture_subtopic_key": "Fa25-L5c-2.0",
      "description": "This is a relevant example of analyzing a **multi-stream control volume** (Heat Exchanger) which utilizes the same mass and energy balance principles and the **`pyCalor`** property module."
    }
  }
}
```

It seems that it likes to select the same example and reading for all steady flow devices. I had to update it, for example, to direct it to a compressor example I did in class instead of a heat exchanger. 

If you want this JSON file to have a similar format to others, you can also upload an example. I've done that in this prompt:
```
I am teaching undergraduate thermodynamics to mechanical engineers. I teach the course in three modules. The students do their homework on PrairieLearn. I would like to use my homework problems programmed on PrairieLearn for use in fine-tuning and retrieval augmented generation in the small language model. I have uploaded here the following files for the problem propertyTablesCalculation-noID:
- question.html: This is where the problem question is located. 
- server.py: The numerical solution is typically in this file.
- info.json: The problem "title", "topic", "tags" (e.g., easy, medium, hard) and other problem metadata is located in this file.
- README: `pyCalor` is a python module that allows students to determine thermodynamic properties. 
- outline-module-one.json: The course outline for Module 1, including "topics" and "subtopics" is located in this file. If possible, references should be made to those "subtopics". Also mentioned in the subtopics are the "examples" that have been solved. See the file "examples.json" for the example "problem_title".
- syllabus.json: The course syllabus for Fall 2025.
- tableOfContents.json: The table of contents of the book used in the course.
- examples.json. Contains the problems and solutions for all exercises done in Module 1 of the course.

Is it possible for you to create a single .json file formatted in a way that is ideal for fine-tuning and RAG? I attached a version of this from a previous problem, which may be helpful for formatting this file. 

If possible, references should be made to relevant book chapter(s) and section(s), exercises, and lecture subtopics.

Please cleanup the formatting:
The numerical values that are displayed in the question.html file are formatted as: {{params.p1_MPa}}. It would be best if we could convert those to their variables, e.g., {{params.p2_MPa}} to $p_1$; {{params.T1_C}} to $T_1$; {{params.mdot12_kgPerS}} to $\dot{m}_{12}$; etc. 

Please also make sure that the LaTeX formulas are properly formatted for a JSON file. 

The students should use `pyCalor` to determine thermodynamic properties and not IAPWS or CoolProp. I'm attaching the README for `pyCalor`.

```

The reply:

```
{
  "problem_id": "propertyTablesCalculation-noID",
  "metadata": {
    "title": "Property Tables: Calculating State Properties",
    "topic": "Properties",
    "difficulty_tags": [
      "medium",
      "Fa23",
      "release"
    ],
    "course_module": "Module 1 (First Law)"
  },
  "problem_statement": {
    "question_summary": "Determine the thermodynamic properties (Temperature $T$, Pressure $p$, Enthalpy $h$, Specific Volume $v$, and Quality $x$) for four independent states of water (a pure substance), representing key points in a Rankine power cycle (boiler exit, turbine exit, condenser exit, pump exit).",
    "raw_problem": "The problem requires calculating various properties of water—the working fluid—at specific states using two known independent properties. These states correspond to key points in an idealized power plant (Rankine cycle): \n\n1. **Saturated Liquid-Vapor Mixture (State A)**: Given pressure $p_A$ and quality $x_A$. Calculate $T$, $h$, and $v$.\n2. **Superheated Vapor (State B)**: Given pressure $p_B$ and specific enthalpy $h_B$. Calculate $T$ and $v$.\n3. **Saturated Liquid (State C)**: Given pressure $p_C$ and is implied to be saturated liquid ($x_C = 0$). Calculate $T$, $h$, and $v$.\n4. **Compressed Liquid (State D)**: Given temperature $T_D$ and pressure $p_D$. Calculate $h$ and $v$.\n\nThe student must use the `pyCalor` module to determine all properties.",
    "given_variables": [
      {
        "variable": "$p_A$",
        "placeholder": "{{params.p1MPa}}",
        "state": "Saturated L-V",
        "units": "\\text{MPa}"
      },
      {
        "variable": "$x_A$",
        "placeholder": "{{params.x}}",
        "state": "Saturated L-V",
        "units": "-"
      },
      {
        "variable": "$p_B$",
        "placeholder": "{{params.p2MPa}}",
        "state": "Superheated Vapor",
        "units": "\\text{MPa}"
      },
      {
        "variable": "$h_B$",
        "placeholder": "{{params.h2}}",
        "state": "Superheated Vapor",
        "units": "\\text{kJ/kg}"
      },
      {
        "variable": "$p_C$",
        "placeholder": "{{params.p3MPa}}",
        "state": "Saturated Liquid",
        "units": "\\text{MPa}"
      },
      {
        "variable": "$p_D$",
        "placeholder": "{{params.p4MPa}}",
        "state": "Compressed Liquid",
        "units": "\\text{MPa}"
      },
      {
        "variable": "$T_D$",
        "placeholder": "{{params.T4C}}",
        "state": "Compressed Liquid",
        "units": "^{\\circ}\\text{C}"
      }
    ]
  },
  "solution_steps": {
    "summary": "The solution requires using the `pyCalor.thermo.state` class to look up unknown properties based on the two given independent properties for each of the four states. For water, the two independent properties are sufficient to fully define the state.",
    "conceptual_steps": [
      "**Step 1: Setup and Property Module Import**\\nImport the necessary module: `from pyCalor import thermo as th`.",
      "**Step 2: State A (Saturated Liquid-Vapor)**\\nUse the given pressure ($p_A$) and quality ($x_A$). The quality $x$ specifies the state as a saturated mixture. Use the `th.state` class with the pressure in 'Mpa' and the quality as a fraction to find the remaining properties ($T, h, v$):\\n`st_A = th.state('water', p=(P_A,'Mpa'), x=x_A)`",
      "**Step 3: State B (Superheated Vapor)**\\nUse the given pressure ($p_B$) and specific enthalpy ($h_B$). Use the `th.state` class with the pressure in 'Mpa' and enthalpy in 'kJ/kg' to find the remaining properties ($T, v$):\\n`st_B = th.state('water', p=(P_B,'Mpa'), h=(h_B,'kJ/kg'))`",
      "**Step 4: State C (Saturated Liquid)**\\nUse the given pressure ($p_C$) and the fact that it is a saturated liquid, which means quality ($x_C$) is 0. Use the `th.state` class with the pressure in 'Mpa' and $x=0$ to find the remaining properties ($T, h, v$):\\n`st_C = th.state('water', p=(P_C,'Mpa'), x=0)`",
      "**Step 5: State D (Compressed Liquid)**\\nUse the given temperature ($T_D$) and pressure ($p_D$). The problem requires using the pressure and temperature to define the compressed liquid state. Note: For a compressed liquid, properties like $v$ and $h$ are often approximated using the saturated liquid values at the given temperature ($T_D$), but `pyCalor` finds the exact value. Convert $T_D$ to Kelvin first.\\n`st_D = th.state('water', p=(P_D,'Mpa'), T=(T_D + 273.15,'K'))`"
    ]
  },
  "property_module": {
    "name": "pyCalor",
    "usage_note": "Students are required to use the custom **`pyCalor`** Python module to determine thermodynamic properties, not IAPWS or CoolProp.\n\nThe software package contains classes `state` and `process`. Thermodynamic properties are found using the `state` class, which requires the substance and two independent properties:\n\n`from pyCalor import thermo as th`\n`st = th.state(substance, property1=value1, property2=value2, name=\"State Label\")`\n\nFields available include $p$ (pressure in \\text{kPa}), $T$ (temperature in \\text{K}), $v$ (specific volume in \\text{m}^3/\text{kg}), and $h$ (specific enthalpy in \\text{kJ/kg})."
  },
  "references": {
    "course_outline_module_1": {
      "key": "Fa25-L1a-3.0",
      "title": "Course learning objectives",
      "lecture_topic": "Introduction",
      "notes": "The course specifically emphasizes moving from old-school appendix tables to utilizing Python modules like `pyCalor` for handling and determining thermodynamic data."
    },
    "textbook_reference": {
      "book_title": "Thermodynamics: An Engineering Approach (Ninth Edition)",
      "chapter_number": 3,
      "chapter_title": "Properties of Pure Substances",
      "sections": [
        "Phase-Change Processes of Pure Substances",
        "Property Diagrams for Phase-Change Processes",
        "Property Tables"
      ]
    },
    "related_examples": [
      {
        "problem_title": "heatExchangerPyCalor",
        "notes": "This example problem demonstrates the application of the `pyCalor` module to find properties (enthalpies of water and R-134a) for a steady-flow device analysis, directly illustrating the use case of the property determination methods learned in this problem."
      }
    ]
  }
}
```

Converting from JSON to JSONL

Here is my prompt:

```
I am interested in using a small language model to improve student learning in the thermodynamics course I am teaching. The goal of the model would be to help students study more efficiently. It is common in thermodynamics for students to not even know where to start with solving a problem. Therefore, if a student has a homework problem they are stuck on, they can ask the model (prompt), and then the model can suggest (reply) what material to read, what exercise problems to review, what lecture videos to watch, etc., so that the students can best prepare in order to be able to solve the problem. 

I am providing here: 
- book chapter and section titles (tableOfContents.json)
- captions from my previous lecture videos. I have taken these files and created outline.json files from them. I’ve attached an example for the first module of the course (outline-module-one.json).
- JSON files based on Jupyter notebooks from problems I have solved in class. I’ve attached an example (turbineAdiabaticFeedwaterHeating-C9-5-57.json).
- pyCalor REDME.md file (thermodynamic property module)
- course syllabus (syllabus.json)
- examples that I have worked out in lecture (examples.json) and are sometimes linked with outline-module-one.json

I would like to follow a scaffolding approach for the prompts and completions which relies on three different training functions:
- level_1: --- Level 1: Conceptual Strategy / Study Guide ---
- level_2: --- Level 2: Specific Hint / Next Step ---
- level_3: --- Level 3: Full Solved Example ---

Can you create a JSONL file with such prompts and completions for the turbineAdiabaticFeedwaterHeating-C9-5-57.json example?

I would like to use this JSONL file to fine-tune an open source model (Phi-3). I have already set up the Phi-3 model to tune. I have a HP Z4 workstation with an NVIDIA GPU which I can use to do the training. It has Ubuntu installed.
```

And the reply from Geimini:

```
{"prompt": "I am trying to solve the thermodynamics problem about the adiabatic steam turbine with feedwater heating (C9-5-57), but I don't know where to start. What should I do?", "completion": "--- Level 1: Conceptual Strategy / Study Guide ---\n\nThis problem involves a **steady-flow, multi-stream control volume (CV)**, which requires careful application of the fundamental balance equations.\n\n**Conceptual Strategy:**\n1.  **Define the CV:** Treat the entire turbine as a single control volume.\n2.  **Apply Conservation Laws:** Write the simplified **Mass Balance** and **Energy Balance (First Law)** for this steady-flow device, considering the assumptions (adiabatic, negligible $\\Delta KE$, $\\Delta PE$).\n3.  **Property Determination:** Use the given state information to find the specific enthalpy ($h$) at all three ports (inlet 1, bleed 2, exit 4). The problem requires the use of the **`pyCalor`** module for this step.\n4.  **Solve for Work:** Rearrange the Energy Balance equation to isolate and solve for the work output ($\\\\dot{W}_{\\\\text{out}}$).\n\n**Study Guide:**\n* **Read:** Review **Chapter 5, Sections: 'Steady-Flow Processes' and 'Some Steady-Flow Engineering Devices'** in the textbook to reinforce the First Law application to devices like turbines.\n* **Watch:** The lecture subtopic **\"Energy Analysis of a Steady-flow System\"** (`Fa25-L5b-2.0`) provides the general framework.\n* **Review Example:** The **`heatExchangerPyCalor`** example is helpful as it also deals with mass splits, multiple streams, and the First Law for Control Volumes, and it uses the **`pyCalor`** module."}
{"prompt": "I've reviewed the material, but I'm still not sure how to set up the equations for the turbine problem (C9-5-57). Can you give me a specific hint for the next step?", "completion": "--- Level 2: Specific Hint / Next Step ---\n\nThe key to solving this multi-stream problem is correctly setting up the **Mass and Energy Balances** for the Control Volume (the entire turbine) and identifying the missing mass flow rates and properties.\n\n**Next Steps:**\n\n1.  **Calculate Specific Enthalpies ($h$):** Before using the balances, you must determine the specific enthalpy for each state ($h_1, h_2, h_4$) using the given pressure and temperature/quality data. Use the mandated **`pyCalor`** state class.\n    * For state 1: $h_1 = h(p_1, T_1)$\n    * For state 2: $h_2 = h(p_2, T_2)$\n    * For state 4: $h_4 = h(p_4, T_4)$\n\n2.  **Mass Balance:** The total mass flow rate in equals the total mass flow rate out:\n    $$\\dot{m}_1 = \\dot{m}_2 + \\dot{m}_4$$\n    Since the mass split fraction $y = \\dot{m}_2 / \\dot{m}_1$ is given, you can express all mass flow rates in terms of $\\dot{m}_1$ and $y$:\n    * $\\dot{m}_2 = y \\dot{m}_1$\n    * $\\dot{m}_4 = (1 - y) \\dot{m}_1$\n\n3.  **Energy Balance (First Law):** With the assumptions ($\\\\dot{Q} = 0$, $\\\\Delta KE = 0$, $\\\\Delta PE = 0$), the steady-flow energy equation simplifies to:\n    $$\\dot{E}_{\\text{in}} = \\dot{E}_{\\text{out}} + \\dot{W}_{\\text{out}}$$\n    $$\\dot{m}_1 h_1 = (\\dot{m}_2 h_2 + \\dot{m}_4 h_4) + \\dot{W}_{\\text{out}}$$\n\n**Your immediate next step is to use the `pyCalor` module to find the three required enthalpies ($h_1, h_2, h_4$) and then calculate the mass flow rates $\\dot{m}_2$ and $\\dot{m}_4$ using the mass split fraction $y$.**"}
{"prompt": "I've tried using the energy balance, but I'm running into calculation errors for the adiabatic steam turbine problem (C9-5-57). Can you provide the full solved example with the final equation and structure?", "completion": "--- Level 3: Full Solved Example ---\n\nThis is the complete, structured solution for the work output of the turbine ($\\\\dot{W}_{\\\\text{out}}$), including the governing equations, property calls using `pyCalor`, and the final calculation steps.\n\n**1. Governing Equations (First Law & Mass Balance)**\n\nAssuming the turbine is adiabatic ($\\\\dot{Q} \\\\approx 0$), is a steady-flow device ($\\\\frac{dE_{\\\\text{CV}}}{dt} = 0$), and has negligible kinetic and potential energy changes ($\\\\Delta KE \\\\approx 0$, $\\\\Delta PE \\\\approx 0$), the Energy Balance simplifies to:\n$$\\dot{W}_{\\text{out}} = \\dot{m}_1 h_1 - (\\dot{m}_2 h_2 + \\dot{m}_4 h_4)$$\n\nThe Mass Balance (steady flow) gives the relationship between the mass flow rates:\n$$\\dot{m}_1 = \\dot{m}_2 + \\dot{m}_4$$\nUsing the mass split fraction, $y = \\frac{\\dot{m}_2}{\\dot{m}_1} = \\text{\\{\\{params.y\\}\\}} = \\text{\\{\\{params.mass_split_percent\\}\\}}/100$, the specific work output (work per unit total inlet mass flow rate) is:\n$$\\frac{\\dot{W}_{\\text{out}}}{\\dot{m}_1} = h_1 - (y h_2 + (1 - y) h_4)$$\n\n**2. Property Determination (Using pyCalor)**\n\nThe following code steps show how the specific enthalpies are found using the `pyCalor` module, which is necessary before calculation.\n\n```python\nfrom pyCalor import thermo as th\n\n# --- State 1: Turbine Inlet ---\n# Given: p1 = {{params.p1_MPa}} MPa, T1 = {{params.T1_C}} deg C\nst1 = th.state('water', p=({{params.p1_MPa}}, 'MPa'), T=({{params.T1_C}}, 'C'), name='1')\nh1_kJperKg = st1.h\n\n# --- State 2: Bleed Outlet ---\n# Given: p2 = {{params.p2_MPa}} MPa, T2 = {{params.T2_C}} deg C\nst2 = th.state('water', p=({{params.p2_MPa}}, 'MPa'), T=({{params.T2_C}}, 'C'), name='2')\nh2_kJperKg = st2.h\n\n# --- State 4: Main Exit Outlet ---\n# Given: p4 = {{params.p4_kPa}} kPa, T4 = {{params.T4_C}} deg C\np4_MPa = {{params.p4_kPa}} / 1000\nst4 = th.state('water', p=(p4_MPa, 'MPa'), T=({{params.T4_C}}, 'C'), name='4')\nh4_kJperKg = st4.h\n```\n\n**3. Final Calculation (Total Work Output)**\n\nFirst, calculate the actual mass flow rates $\\dot{m}_2$ and $\\dot{m}_4$:\n\n```python\n# Given: Total Inlet Mass Flow Rate\nmdot1_kgPerS = {{params.mdot1_kgPerS}}\n\n# Given: Mass Split Fraction (y)\ny = {{params.mass_split_percent}} / 100\n\n# Calculate Outlet Mass Flow Rates\nmdot2_kgPerS = y * mdot1_kgPerS\nmdot4_kgPerS = (1 - y) * mdot1_kgPerS\n```\n\nFinally, substitute the values into the Energy Balance equation to find the total work output ($\\\\dot{W}_{\\\\text{out}}$):\n\n```python\n# Energy Balance: W_dot_out = m_dot1 * h1 - (m_dot2 * h2 + m_dot4 * h4)\nWdot_out_kJperS = (mdot1_kgPerS * h1_kJperKg) - (mdot2_kgPerS * h2_kJperKg + mdot4_kgPerS * h4_kJperKg)\n\n# Convert to MW (1 MW = 1000 kJ/s)\nWdot_out_MW = Wdot_out_kJperS / 1000\n\n# Final Answer\nprint('(a): Work Output: {0:1.2f} MW'.format(Wdot_out_MW))\n```"}
```

### Generating `rag_corpus.txt` File
From the `CalorAI` directory, please run:
``` bash
python scripts/_generate_base_corpus.py && \
python scripts/_convert_toc_to_rag.py && \
python scripts/_convert_outlines_to_rag.py && \
python scripts/_convert_notebooks_to_rag.py
```
