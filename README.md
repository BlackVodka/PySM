# PySM

PySM is a **Py**thon-based **S**tate **M**achine generator, using yEd diagrams (*.graphml) as source.  
It's based on a static library core written in C and the generated state machine dependend code files.

The main features are:
- **Easy:** Creating a yEd diagram for a state machine is quite easy, so is generating the according code
- **Powerful:** The library and generated state machine code is able to
  - Support transition priorities, conditions and actions
  - Handle the generated state machine as a module with boundarys by defining in- and output signals
  - Generate own defines and includes, like e.g. for calling external functions
  - Create state machine - local variables (counters, internal flags,...)
  - Support actions when entering, executing and leaving a state by keywords

### What it can do for you...
The PySM project is based on an idea of a workmate (greeting to Florian Koerfer at this point!) and is inspired by the idea of model-driven development, being able to see and alter easily the behaviour of a program, not needing to take a single look at the generated code.  
Also, to enable companies to use this work for their projects, I decided to use the LGPLv3 license (for more details, see section **Commercial use**).

## ...and what it can't
Other commercial well known code generators have pretty good fixed point support, whereas PySM will fill given code in the diagram just as it is (beside of some basic checks), propably leading finally to compiling errors if the pasted code is wrong.  
Another point is the debug-ability, other tools provide nice shiny GUIs to debug their diagrams as "what-you-see-is-what-is-happening", whereas you'll have to debug the generated/library code by hand  
(which shouldn't be much pain due to the code's readability, though).

## How it works
Please see **Detailed documentation** section below for detailed explaination for designing state machine diagrams and using the generator.  
The generator parses a given yEd diagram (\*.graphml-file), searching for states, configuration blocks and transitions.  
Only diagram element types describing these objects are processed by the generator, other objects will be ignored (and can be used as e.g. documentation blocks).  
Afterwards, the generator will produce a \*.c and \*.h file for the generated state machine, which should compile along with the library core to a fully running state machine.

The library core itself basically does the following:
```
      +------------------+
      | RunStateMachine()|
      +--------+---------+
               |
      +--------v---------+
      | Execute entry of |
      | initial state    |
      +--------+---------+
               |
     +---------v----------+
     | RunStateMachine()  <------------------+
     +---------+----------+                  |
               |                             |
               |                             |
     +---------v----------+                  |
     | Execute during of  |                  |
     | active state       |                  |
     |                    |                  |
     +---------+----------+                  |
               |                             |
    +----------v------------+                |
    | Evaluates a transition|       no       ^
    | leaving active state  +----------------+
    | to TRUE?              |                |
    +----------+------------+                |
               |                             |
               |yes                          |
               |                             |
               |                             |
+--------------v----------------+            |
| Execute exit of active state, |            |
| if any                        |            |
+--------------+----------------+            |
               |                             |
  +------------v--------------+              |
  | Execute transition action |              |
  | instructions, if anny     |              |
  +------------+--------------+              |
               |                             |
       +-------v----------+                  |
       | Execute entry of |                  |
       | next state       |                  |
       +-------+----------+                  |
               |                             |
 +-------------v-----------------+           |
 | Set active state = next state +-----------+
 +-------------------------------+
```

## Getting everything set up
Todo: explanation of python 3.6 etc.

## Detailed documentation
A short note: The library core is documented using Doygen, see pySM_test/DOXY/html/index.html).

### About the files
The folder test_diagrams for some already preprepared example diagrams.  
In pySM_Gen, the generator's files can be found (more on launching and using it later).  
The folder pySM_test contains the library core in folder LIB, basically everything you'll need to run your own state machines.  
Along with that, there's a main.c file, calling a litte software component (swc), which will use and call the generated example state machines.  
This is the intended usage later:  
A main function, calling a module/software component, using one or more generated state machines there.  
Also, as this project was developed using Eclipse CDT and PyDev, you'll find .project, pydevproject and .cproject files in the according folders.

**Drawing yEd diagrams for state machines**  
At the moment of writing, the following mapping is set:  
- States == Flowchart Process elements
- Transitions == Edges/Splines with a defined beginning and ending (start- and stop state)
- Configuration blocks == Flowchart Predefined Process, divided into blocks defining
  - Preprocessor directives (defines, includes)
  - State machine - local variables
  - Input signals
  - Output signals
- Init state marker == Flowchart Start2

Division of the configuration block is done by a first-line keyword, as they are at the moment of writing: **PREPROCESSOR_DIRECTIVES**, **VARIABLES**, **INPUT_SIGNALS** and **OUTPUT_SIGNALS**.

All and each of the configuration blocks are optional, a diagram for code generation just must have at least one state and an init marker, or generation will fail.

### Rules for diagrams
Configuration blocks:  
**Preprocessor directives** will be completely raw inserted line-by-line into the generated code at the appropriate section  
**Variables** are checked for a valid given datatype and a given intial value, following a semicolon ( ; ) at each line end.  
A valid variable line without an intial value will generate a warning and an assumed initial value 0 (zero).  
**Input- and Output signals** also must be declared with a valid datatype, variablename and a semicolon ( ; ) at line end.  

State texts:  
A state object must contain at least one line of text.  
The state's first text line defines the **state's name**. It's highly recommended to use uppercase here for readability of the later generated code.  
In the following (optional) text lines, a state can contain instructions executed when entering, staying or leaving the state.  
Defining any of these instructions (each optional) is done by a textline,  
containing one of the codewords **entry:**, **during:** or **exit:**, followed by the instruction text, finished either by the state's text end or by another codeword.  
A instruction text for itself will be inserted raw and unprocessed (just in- and output signals will be handled) in the in the appropriate code section, so be sure to check that!

Init state:  
There must be one(!) init marker, connected by one(!) transition to a single(!) state, marking the initial state this way.

Transition texts:  
Transitions don't require to have a text and checking their transition condition will alway return true, leading to an immediately triggering transition when being handled.  
A transition text can contain one or more of the following:  
- **Priority** (highly recommended): A transition's priority can be given by the first text line, first few characters containing the priority as number (1,2,3...) in angle brackets ( < , > ). Preceding and following spaces are allowed, but be sure to avoid them in the priority instruction, as the generator searches directly for the expression `<X>` .
- **Condition**: A transition condition is defined by condition text, surrounded by square brackets ( [ , ] ).  
Transition condition text will be directly generated into the correct place in code, so be sure that the given code evaluates to only either true or false!  
Therefore, line breaks and whitespaces are allowed in condition text, as long as this text would compile as it is.
- **Action(s)**: Transition actions are defined by executable code surrounded by curly brackets ( { , } ).  
Transition action text will be directly generated into the correct place in code, so be sure that the given code is executable!  
However again, line breaks and whitespaces are allowed in action text, as long this text would compile as it is.

**Some notes about in- and output signals**  
If you use and provide signals (in- and output values) over the boundarys of the state machine itself, due to the nature of the generated code the in- and output values need to have a prefix, at the moment of writing `<sigName>_inputSignals->` or `<sigName>_outputSignals->` .
To avoid having to insert this in every occurence of an in-/output signal in the diagram, the generator will append this prefix to a defined in-/output signal variable using the according configuration block, wherever they occur (transition conditions, actions and state instructions).  
So, if you'd like to use a in- or output signal, you'll just have define them with the according configuration block and use the exact given variable name there somewhere else in your diagram.

Ignoring any of these rules will either lead to corresponding warnings and/or code generation abort with an error (good), or misbehaving/wrong generated code (bad).

### Using the generator
ToDo: Explain code generator

### Notes / Configurable things
- Due to the way the library core was coded, the maximum number of transitions leaving a state is limited.  
The setting for this is a define in pySM_test/LIB/PySm_Cfg.h , called PYSM_MAX_NO_OF_TRANSITIONS_PER_STATE and set to 10 atm., which should be sufficient, though.  
This limitation is also respected by the code generator, unfortunately set in it's own configuration file, `max_number_of_transitions_per_state` in pySM_Gen/PySM_Cfg.py.
- A list of valid datypes as defined in pySM_test/LIB/PySm_types.h is set for the generator in pySM_Gen/PySM_Cfg.py.  
Default is atm. list_of_dataTypes =   
pySm_bool,pySm_uint8,pySm_int8,pySm_uint16,pySm_int16,pySm_uint32,pySm_int32,pySm_uint64,pySm_int64
- Some generator default settings can be configured in pySM_Gen/PySM_Cfg.py, like  
  - default_code_header_file = 'defaultCodeHeader.txt'  
  - default_author_name = 'Author'  
  - default_output_path = 'OUT'  
  - logfile_name = 'PySM_Gen.log'

Besides of the mentioned entries in pySM_Gen/PySM_Cfg.py, it's not recommended to change anything else in this file, unless you really know what you are doing!

## Commercial use
One important note:  
I'm neither a lawyer nor an expert in juristic topics, the following may be incorrect or  incomplete.  
For being sure in commercial using this project, do for yourself some investigations and/or contact a lawyer!

As far as I know, the only way to have a open source (OS) project like this being able to be used in commercial ways and still have a strict OS-license, the OS-part must be compiled as a shared library (e.g. \*.so, \*.a).  
Due to the nature this project was built, this shouldn't be a problem at all, although I haven't had the time yet to set up an example for doing so.

Long story short: Link the library core as dynamic library (NOT static!) and you should be good to go!

References (German): [http://www.it-rechts-praxis.de/meldungen/Open-Source-Kommerzielle-Nutzung-von-LGPL-Libraries-12]
