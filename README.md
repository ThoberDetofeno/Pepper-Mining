<div align="center">

<img src="docs/images/logo.png" alt="drawing" width="300"/>

## **An open-source Process Mining library in Python**
## 🌶🌶🌶 **Pepper Mining - Alpha version. 🌶🌶🌶**
## `pip install peppermining` </br>
</br>

<div align="left">

  # Welcome to Pepper Mining

Pepper Mining is a open source Process Mining platform written in Python, designed to be used in both academia and industry.
  
Pepper Mining is a framework designed firstly be the backend of an application. Such, the effort in this project is to build a framework following Design Patterns.
  
In this documentation, you can find all relevant information to set up Pepper Mining and start your Process Mining journey.

## <span>&#9888;</span> Are you discovering Process Mining?
I recommend accessing the contents of <a href="https://www.processmining.org/">processmining.org</a> and follow <b>Prof.dr.ir. Wil van der Aalst </b> on social media.

The Process Mining Handbook is amazing, you can reading in https://link.springer.com/book/10.1007/978-3-031-08848-3. Also, for a overview of process mining, we recommend looking at the [Coursera MOOC](https://www.coursera.org/learn/process-mining) on [Process Mining and the seminal book of Wil van der Aalst](https://link.springer.com/book/10.1007/978-3-662-49851-4).  
  
See also <a href="https://pm4py.fit.fraunhofer.de/">PM4PY</a>, it is another open source Process Mining platform.


Enjoy #processmining!

## 🚀 Installation

The Pepper Mining installation is very easy and used only 4 Python libraries.
For more details about the Pepper Mining requirements, see too the [setup.py](https://github.com/ThoberDetofeno/peppermining/blob/main/setup.py)
Install via PyPi
You can install Pepper Mining with Python's pip package manager:

```python
# install peppermining
pip install peppermining
```

## 🏃‍♂️ Quickstart
In this tutorial you will have a journey about the main features available in Pepper Mining.

Before you begin, please install Pepper Mining on your system, as described in the Installation section.
 
The IPython Notebook is [here](https://colab.research.google.com/drive/18y9ApU4CRzl-QR_4yWG0FPPulEXmfpBB?usp=sharing).

### Data preparation
In the remainder of this tutorial, we will use an oftenly used dummy example event log to explain the basic process mining operations. The process that we are considering is a simplified process related to customer complaint handling, i.e., taken from the book of van der Aalst. 

The process, and the event data we are going to use, looks as follows.
  
<img src="docs/images/bpmn_running_example.png" alt="drawing" width="900"/> 

  
We have prepared a small sample event log, containing behavior similar equal to the process model. The samples we are using in this example contain 8 Cases and 52 Event log.

Observe that, the arrow black in the picture below describe the Case and the arrow colorful are Event log. The Case contain two information, first a number that represent the case_id and second is a attribute with Product name. Each Event log contain the case_id, activity name, timestamp that start the activity, and resource that executed the activity.
  
<img src="docs/images/running_example.png" alt="drawing" width="1200"/> 

  
One of the characteristics of Pepper Mining is that the Event log is mandatory, but is possible to add the Cases information in separated. In this way, is possibible to add informations that represent all event logs and can be using with more performance in the filter operations or compliance analysis.
The data this tutorial is available in CSV format, on the links below:
  
Cases: https://raw.githubusercontent.com/ThoberDetofeno/peppermining/main/tests/data/case-example.csv

Event log: https://raw.githubusercontent.com/ThoberDetofeno/peppermining/main/tests/data/eventlog-example.csv

### Creating a Pepper Mining analysis
Pepper Mining analysis is the beginning of all things. When creating the PepperMining object we are creating a Pepper Mining analysis.
The first step is creating a PepperMining object, the next step is to add data from Event Logs and Cases.

After these two first steps are possible to visualize, filter and to do all operations in Pepper Mining.
```python
import peppermining as pm
# First step: Create Pepper analysis
pepper = pm.PepperMining()
# Second step: Add Event log and Case data
pepper.read_event_log_csv('https://raw.githubusercontent.com/ThoberDetofeno/peppermining/main/tests/data/eventlog-example.csv')
pepper.read_cases_csv('https://raw.githubusercontent.com/ThoberDetofeno/peppermining/main/tests/data/case-example.csv')
```
### Basic data visualizations  
In this section the basic visualizations of the data added in Pepper Mining.

The basic views are: Event log, Cases, Activities and graph of event data.
```python
# Return Event logs data
pepper.get_event_log()
# Return Cases data
pepper.get_cases()
# Return Activities data
pepper.get_activities()
```
Return the activities with interaction graph of event data. Return a graph using pydot objects. It is same the Spaghetti process. 
```python
# Return the pydot object
graph = pepper.drawing()
# Create a image 
graph.write_png('output.png')
# Render the png file.
from IPython.display import Image
Image('output.png')
```
<img src="docs/images/running_example_output.png" alt="drawing" width="500"/> 

### Filtering
Filtering is the restriction of the Pepper Mining analysis (Event log and Case) to a subset of the behavior.

After filtering the return object it have all behavior that Pepper Mining analysis. Because, de Pepper Filter is a inheritance of Pepper Mining.

It is possible to do a hierarchy of filters, because each filter is a object.
This way the user can make "n" filters and return to last step without losing the performance of the software.

  
The first filter is select all Event Logs that ended with activity 'pay compensation'. For this, let's create the CaseEndActivityFilter object.
```python
# Filter on end activities of Pepper Mining analysis
filter_1 = pm.CaseEndActivityFilter(pepper, ['pay compensation'])
filter_1.get_cases()
```

For the second filter, let's use the previous filter result. Now we want to view all events except the 7 and 8 cases. For this,  let's create the CaseFilter object with the parameter 'not contain'.
  
```python
# Case Filter of Pepper Filter (CaseEndActivityFilter)
filter_2 = pm.CaseFilter(filter_1, [3, 8], 'not contain')
filter_2.get_cases()
```
To finish this section, we show the filters used in second filter. Is possible to render the graph only of second filter.
```python
# Visualize the filter used in second filter
filter_2.get_filter()
```
### Variant Explorer
Variant Explorer is a analysis tool that helps you explore how a specific process flows through your organization, in the words, see all the different ways the process flows in your organization.

In the Pepper Mining is possible to see the variant list of a Pepper Mining analysis or Pepper Filter.

Firstly, we gonna using the Pepper Mining analysis to show the variant lists. The method get_variant return 3 main informations: a key that is an identifier for variant, a list of cases and a list of activities that represent each variant.

In this example, about customer complaint handling, we have 5 variants. The image below show the activities sequence of each variant.

<img src="docs/images/running_example_variants.png" alt="drawing" width="900"/> 

```python
# Variants of a Pepper Mining analysis
pepper.get_variants()
```
  
In the second example, we used the Pepper Filter object to view the Variant lists.

```python
# Variants of a Pepper Filter
filter_2.get_variants()
```

It is very common visualize the graph of specific variants. To show the graph of 2 variants, we gonna creating a variant filter and after view the graph.
```python
# Variant filter
variant_list = ['register request->check ticket->examine casually->decide->pay compensation',
                'register request->examine thoroughly->check ticket->decide->pay compensation']
variants = pm.VariantFilter(pepper, variant_list)
# Create a image 
variants.drawing().write_png('output.png')
# Render the png file.
from IPython.display import Image
Image('output.png')
```
<img src="docs/images/running_example_filter_variants.png" alt="drawing" width="900"/> 
  
### KPIs and Statistics
In Pepper Mining, it is possible to calculate different statistics and KPI in all modules. It can be used in the objects Pepper Mining analysis, Pepper Filter, and Conformance checking.

Is possible to user the KPIs of two way.

In the first situation you have a Pepper Analysis or Filter objects and to want adding the KPIs.
```python
# Return case datas with KPIs
pepper.get_cases(['NumberOfEvents', 'NumberOfActivities'])
# Return activities datas with KPIs
pepper.get_activities(['NumberOfCases', 'Rework'])
# Return variant datas with KPIs
pepper.get_variants(['NumberOfEvents', 'NumberOfActivities', 'NumberOfCases'])
# Return summary the events and cases.
pepper.get_summary(['NumberOfEvents', 'NumberOfActivities', 'NumberOfCases', 'AverageEventsPerCase', 'Rework'])
```
Another way is creating the Pepper KPI object and add the Pepper Analysis or Pepper Filter.
```python
kp1 = pm.NumberOfCases(filter_1)
# Summary
kp1.get_kpi()
# get_kpi_variants
kp1.get_kpi_variants()
# Return KPI value per day, it is important to line charts
kp1.get_kpi_per_day()
```
I´d like to show the KPI **Throughput time.**

Throughput time is the actual time an activity takes to be done. This includes the entire duration from start to end of the activity,
which in many cases means the time a factory needs to convert raw materials into finished goods.
Given an event log, it is possible to retrieve the list of all the durations of the cases (expressed in seconds).

```python
# Throughput time per case
pepper.get_cases(['ThroughputTime'])
# Summary with Throughput time
pepper.get_summary(['ThroughputTime'])
# Throughput time per variant
kp2 = pm.ThroughputTime(pepper)
kp2.get_kpi_variants()
```

### Conformance Checking
The conformance checker allows you to automatically compare a reference process model with the actual process flows discovered from the data. The difference between the model and actual flows is returned in the dataframe with a diagnostics column.

Then, we need a process model to compare with Pepper Mining analysis, and after this we will have the Conformance and Violations.

This section will have 3 steps: Definition of Process model, Conformance analysis and Violations.

**1. Definition of Process Model.**

Process Model represent the ideal model that used in the identification of validations and conformance.
<img src="docs/images/running_example_model.png" alt="drawing" width="900"/> 
```python
# Create the object ProcessModel
model_1 = pm.ProcessModel()
# Read the event log that represent the a ideal process.
model_1.read_process_model_csv('https://raw.githubusercontent.com/ThoberDetofeno/peppermining/main/tests/data/processmodel-example.csv')
# Return the process model data
model_1.get_process_model()
```

**2. Conformance Analysis**

The difference between the model and actual flows is returned in the dataframe with a diagnostics column.

```python
# Create the object to conformance analysis
con_analysis = pm.Conformance(pepper, model_1)
# Return all cases that are in conformance with models.
con_analysis.get_cases()
# Return Conformance overview data.
con_analysis.get_summary(['NumberOfCases', 'AverageEventsPerCase', 'ThroughputTime'])
# Return the diagnostic per case.
con_analysis.diagnostics()
```

**3. Violations**

Pepper violation has various specific methods to discovery the violation of an event log. In the Pepper Mining each violations has a class that can be analysed on demand.

In this section, we are showing three violations.
1. Undesired Activity:
```python
v1 = pm.UndesiredActivity(pepper, model_1)
v1.get_violation()
```
2. Undesired Connection:  
```python
v2 = pm.UndesiredConnection(pepper, model_1)
v2.get_violation()
```
3. Activities executed by the same user:
```python
v3 = pm.RunBySameUser(pepper, ['register request', 'check ticket', 'pay compensation'])
v3.get_violation()
```
## <span>&#10070;</span> API Modules
<img src="docs/images/api_module.png" alt="drawing" width="1200"/>

More information HERE (https://thoberdetofeno.github.io/peppermining/)!
  
## 📝 License
Pepper Mining is completely free and open-source and licensed under the [MIT](https://github.com/ThoberDetofeno/peppermining/blob/main/LICENSE.txt) license.
