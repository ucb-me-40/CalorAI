# CalorAI
Language Model Being Developed for Teaching ME40, Thermodynamics, at UC Berkeley. 

Instructors: Prof. Hail and Prof. Schutzius. 

The data here is used for fine-tuning and retrieval augmented generation (RAG) of the small language or large language model. We are currently training a small language model Phi-3. 

## Housekeeping
The primary purpose of this SLM is to aid students in studying thermodynamics. Based on student feedback, we believe that most of the prompts will be copying and pasting the homework question and then searching for course resources to help them study and enable them to solve the problems on their own. The resources created by the instructional staff are organized as follows:

```
me40-slm
+-- book
|	`-- tableOfContents.json
+-- courseInstances
|	+-- Fa23
|	|-- Fa24
|	|-- Sp25
|	|-- Fa25
|		`-- syllabus.json
|		`--lecture-01a
|			`-- 1_mtmivyvl.srt
|			`-- 555352862 - 1_mtmivyvl - PID 2640881.json
|			`-- 555352862 - 1_mtmivyvl - PID 2640881.txt
|			`-- outline.json
|		`-- ...
+-- examples
|	+-- nitrogenHeatingWorkTransfer.json
|	|-- ...	 
+-- homework
|	+-- flowWorkCompressor-C9-5-20.json
|	|-- ...

### tableOfContents.json
The `tableOfContents.json` file should contain all of the book editions that you think students may use. Do not delete other editions.

### courseInstances 
This folder contains data from each semester that the course is taught. This includes the syllabus and the captions from the recorded lectures (`.srt`, `.json`, `.txt` files). I create an outline.json file and define subtopics within the lecture. Those subtopics have a time_range, which is easy to define if you watch the recordings. There is a feature on bCourses, which allows you to create bookmarks. I used that to generate the `time_range` field entries. You should also tag those bookmarks, e.g., `Fa25-L1a-1.0`. This will also help students to navigate to the correct part of the video as they only have to enter that tag into the search and they will find the correct part of the video. This part is a non-trivial amount of work, but I believe it is essential for student learning. I don't recommend just uploading the closed caption data and asking it to create  an `outline.json` file. If an example is solved during lecture, I recommend having the solution in a Jupyter notebook, formatted in a specific way, so that we can convert that to a `.json` file to be placed in the `examples` folder. 

The `"tags"` `"alpha"` means that the `"subtopics"` is ready for review by the GSI or Reader. The `"tags"` `"beta"` means that the `"subtopics"` is ready for review by the Instructor. LaTeX equations will be formatted differently in a `.json` file. Each `\` requires another `\`, i.e., `\\`. 

Original LaTeX entry: `$\mathbf{h_{\text{in}} = h_{\text{out}}}$` 

Needs to be written as: `$\\mathbf{h_{\\text{in}} = h_{\\text{out}}}$`

Here is an example of an input outline.json file:

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

The `"examples"` field are existing files located in the `examples` folder and are formatted as `.json` files. These individual `outline.json` files will then be combined into a single `outline.jsonl` file. 

### examples
This folder should contain all of the problems solved in lecture. The file should originally be written in a Jupyter notebook, and then converted to a `.json` file. From there we will convert it to a prompt/completion, which is formatted as `.jsonl`. This method (IPYNB to JSON to JSONL) is the better engineering approach for a large, high-stakes dataset.

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

Here is the prompt I then gave Gemini:
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
