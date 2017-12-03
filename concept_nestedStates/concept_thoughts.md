## Thoughts on concept for being able to handle super-/substates by using group-nodes in yEd ##

There are, as at the moment I can only think of, four fundamental types of transitions need to be taken care of:
- a) superstate to superstate
- b) substate to superstate
- c) substate to substate
- d) superstate to substate

One idea I got to handle them all is to add two informations to each state, regardless if super- or substate:
- A flag **is_superstate** (costs memory, but saves a lot of iteration runtime, see explanation below)
- The **state's_superstate**, if any (NULL-Ptr or pointer to superstate)

Another idea is to do the checks which exit/entry instructions will be need to run within the code generator for performance purposes of the generated code on the microcontroller.
This would cost more memory by saving a list of to-run entry/exit instructings in the appropriate order for each transition.  
So again, this is a decision over memory use Vs. runtime.

General approach is, that the saved currentActiveState is at the lowest hierarchy (doesn't have any substates).

However, the following thoughts of algorithms are needed for both approaches.

Into detail:

### Exit instructions ###

Let's say SUB_A is currentActiveState, check for exiting transitions
* ->  yes: Set **exitState** to currentActiveState
* ->  no: Check **state's_superstate** (if any) for exiting transitions  
* * -> no: Repeat checking **state's_superstate**, until no superstate found (found topmost-state)
and no valid exit transition was found
* * -> yes, found a valid exit transition:   
+ + + Remember the superstate, which's exit transition evaluated to true (**exitState**)

Is **exitState** a superstate? (Check **is_superstate**)
* -> yes:  
* * -> **Run_exit_of_exited_substates()**
* -> no:
* * -> **Run_exit_of_exited_superstates(exitState)**

with:  

**Run_exit_of_exited_substates(exitState)** =  
- Create and set a statePtr = currentActiveState
- **do** run statePtr->exit() ; set statePtr = statePtr.**state's_superstate**
- **while**(statePtr.**state's_superstate** != exitState)



**Run_exit_of_exited_superstates(exitState)** =  
- Create and set a statePtr = **exitState**
- Get triggered transition final target targetState by calling  
 **getTransitionTargetFinalState(transition, &targetState, FALSE)**
- **do** run statePtr->exit() ; set statePtr = statePtr.**state's_superstate**  
- **while**(statePtr.**state's_superstate** != transitionTargetState.**state's_superstate**):  
- run statePtr->exit() ; set statePtr = statePtr.**state's_superstate**

This should ensure the hierarchical calling of the exit functions, form the innerst sub-state to the topmost superstate.

Note: transitionTargetState needs to be the final activated substate (no superstate!).  
For this, the following idea should work:  
- A function **evaluateTransitionTargetFinalState(transition, targetState*, flag_runEntryInstructions)**.  
This function will need to iterate a superstate down to the final transition target substate (unfortunately, two times).  
**evaluateTransitionTargetFinalState** will be called a second time:

### Entry instructions ###
Here, simply again our recently mentioned function will be used again, this time, it will also run the entry() - instructions (the targetState won't be needed):  
**evaluateTransitionTargetFinalState(transition, targetState*, TRUE)**.

About the function **evaluateTransitionTargetFinalState** :  
TODO!  
EBENFALLS MUSS NOCH GEPRÜFT WERDEN ANHAND EINIGER BEISPIELE, OB DER ANSATZ OBEN SO FUNKTIONIEREN KANN

### Changes on Init/First run ###
TBD
