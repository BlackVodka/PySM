# PySM

## I. Introduction
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

### ...and what it can't
Other commercial well known code generators have pretty good fixed point support, whereas PySM will fill given code in the diagram just as it is (beside of some basic checks), propably leading finally to compiling errors if the pasted code is wrong.  
Another point is the debug-ability, other tools provide nice shiny GUIs to debug their diagrams as "what-you-see-is-what-is-happening", whereas you'll have to debug the generated/library code by hand  
(which shouldn't be much pain due to the code's readability, though).

## II. How it works
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

## III. Installation / Getting everything set up
At the moment of writing, PySM uses standard python 3 built-in modules except of PyQt5 for GUI creation.
Although it has been developed in a python 3.6 environment, it should work in any 3.x env.
### Linux
On Linux, depending on your distro, you'll have to install python3 and PyQt5  
(here in my ArchLinux system called pacman packages python-pyqt5 and python3).  
Afterwards, you should be able to run the generator by executing
`python3 /path/to/PySM_Gen.py`.
### Mac OSX
As I don't own a Mac, I cannot guide you how to get this running.  
In theory, everything described for Linux should be valid for OSX, too.
Anyway, Anaconda is also available for OSX, so propably this is the better option.
### Windows
On windows platform I highly recommended using Anaconda for python installation, as it brings per default every modules you'll need.  
You just need to create a Anaconda python 3 installation (either per default or as a separate anaconda environment) and either start the generator using the anaconda command line, or create a launcher for that, using as  
**Target** either if you're using the default Anaconda environment  
`%ComSpec% /k ""C:\Users\xxx\Anaconda3\Scripts\activate.bat" && python PySM_Gen.py""`  
or if you need to use an explicit Anaconda environment  
`%ComSpec% /k ""C:\Users\xxx\Anaconda3\Scripts\activate.bat" "C:\Users\xxx\Anaconda3\envs\myEnv" && python PySM_Gen.py""`  
and setting the property  
**Start in** to the generator dir (e.g. D:\pySM\pySM_Gen) .  
Note that of course you'll have to adjust the Anaconda installation path to your system.  
Also, with the `/k` switch the terminal will stay open, showing python interpreter error output, if any. If you don't like this behaviour, you can change it to `/c`, which will terminate the terminal if the generator execution has been finished/window closed (not recommended).

Anaconda-Link:  
[https://www.anaconda.com/download]

## IV. I found a bug, what now?
Please open up an issue ticket on github about the problem.  
For better investigation / recreation of the bug, please
- Provide a debug-enabled generation logfile. Per default, the generator creates a logfile calles PySM_Gen.log in it's dir.  
Also, please make sure that debug logging is enabled (`__ENABLE_DEBUG__ = True` in PySM_Gen.py)
- If the generation aborts without an error/warning, most propably one of the python functions crashed with an unhandled exception.  
In this case, please try to reproduce this behaviour when launching the generator from terminal/cmd and provide the python error traceback in the issue ticket.
- If possible, please provide a simple example diagram, which provokes the reported problem for easier reproducability here

Also, you're very welcome if you have ideas for new features or changes.

And, if you're familar with python, I'd be very glad if you like to take part in the further development of this project :)

## V. Detailed documentation
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

## VI. Using the generator
Usage of the generator will be explained using the following screenshot of a successful generation:  
![Alt text](./generator_screenshot.png?raw=true "Title")  
- [1] Path to state machine's yEd diagram file (\*.graphml); also supports drag & drop
- [2] Path in which the state machine's source files will be generated. Already existing files will be overwritten; also supports drag & drop of the target folder.  
Default output is relative to the generator's path a dir called OUT (see also chapter VII)
- [3] Header prologue file: At the beginning of the generated source files (\*.c, \*.h), a file header will be inserted.  
Here you can provide e.g. your company's copyright information.
Default used file is defaultCodeHeader.txt (see also Chapter VII)
- [4] The author's name; will be used for doygen's `@author` - keyword
- [5] The state machine name. This will be used for almost every state-machine's internal variable naming and for the input-/output signal typedef naming, as well.  
Therefore, whitespaces are permitted here, so be sure to use a short, unique name!
- [6] Start generation
- [7] Generator's output window.  
Should contain at least a message about errors or successful code generation.
If no finishing message a la code generation finished/aborted is shown, most propably you've found a bug =/  
Please see following up chapter about that.

## VII. Notes / Configurable things
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
- Different companies have different naming conventions for their code.  
I use here my personal naming convention, which generates besides of function and file names everything lowercase.  
If you want to alter this behaviour, the corresponding point in the generator's python files should be easy to find, if you can't, feel free to open an issue ticket for me to help you ;)

## VIII. Commercial use
One important note:  
I'm neither a lawyer nor an expert in juristic topics, the following may be incorrect or  incomplete.  
For being sure in commercial using this project, do for yourself some investigations and/or contact a lawyer!

As far as I know, the only way to have a open source (OS) project like this being able to be used in commercial ways and still have a strict OS-license, the OS-part must be compiled as a shared library (e.g. \*.so, \*.a).  
Due to the nature this project was built, this shouldn't be a problem at all, although I haven't had the time yet to set up an example for doing so.

Long story short: Link the library core as dynamic library (NOT static!) and you should be good to go!

References (German): [http://www.it-rechts-praxis.de/meldungen/Open-Source-Kommerzielle-Nutzung-von-LGPL-Libraries-12]

## IX. Future plans / development progress
At the moment, I'm quite satisfied with the achieved work and will have a look at bugfixes with the highest priority.  
For the near future I'm planing to enhance the library core code for pointer/memory protection, finally enabling it to get reviewed and certified for functional safety relevant projects according to ISO 26262 in companies.

Another though I have in my mind for some days is the complete avoidance of yEd and creating a complete own GUI, which would have some benefits as e.g. having some graphical behaviour simulation abilities as known from other commercial products, which is the biggest 'would-like-to-have' feature I'm thinking of for now.
