# Implementation details: The Fundamentals

This part of the handout explains some basic facts and concepts you need to be
familiar with in order to complete the tasks in the assignment. Skip it at your
own risk!

## The search infrastructure for the single-agent collecting birds problem

Your search algorithms needs to return a list of actions that reaches
the goal from the start state in the given problem. The elements of this list
need to be one or more references to the attributes `NORTH`, `SOUTH`, `EAST`
and `WEST` of the class [`Directions`](../game_engine/actions.py).

Your search algorithms will be passed as an argument an instance of either the
class [SearchProblem](../search_problems.py) or one of its subclasses. The
arguments will be instances of `PositionSearchProblem` (collecting a single
bird) or `MultiplePositionSearchProblem` (collecting all the birds).

It would be good that you get familiar with the classes in the
[module](../search_problems.py), but all of the methods you will need to use
are listed later in this section.

States are described in the [previous section](1_getting_started.md). Here we
give more details on how these are implemented:

- For `PositionSearchProblem`, states are **pairs of integers**

  ```c
  (int, int)
  ```

  representing the coordinates of the red agent.

- For `MultiplePositionSearchProblem`, states are **nested** tuples
  ```c
  ((int, int), ((int, int), ...))
  ```
  where the first sub-tuple represents the coordinates of the red agent, the
  second sub-tuple is the set of coordinates of the remaining (yet to be
  collected) yellow birds.

What is important is that in either case the states are **hashable**

> An object is hashable if it has a hash value which never changes during its
> lifetime (it needs a `__hash__()` method), and can be compared to other
> objects (it needs an `__eq__()` method). When comparing, objects which are
> equal must have the same hash value.
>
> Hashability makes an object usable as a dictionary key and a set member,
> because these data structures use the hash value internally.
>
> All of Python's immutable built-in objects are hashable, while no mutable
> container (such as lists or dictionaries) is. Objects that are instances of
> user-defined classes are hashable by default; they all compare unequal
> (except with themselves), and their hash value is derived from their id().

so they can be put into a
[set](https://docs.python.org/3/tutorial/datastructures.html#sets) or used as
a key in a
[dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
if your algorithms require it.

The typical interactions with instances of `SearchProblem` or its
sub-classes will probably be:

- Obtaining the _initial state_ via

  ```python
  s0 = problem.get_initial_state()
  ```

  or similar, so the variable `s0` contains a reference to the initial state.

- Test if a given state _s_ is a _goal_ state or not, as in

  ```python
  if problem.goal_test(s):
      print("YAY!")
  else:
      print(":'(")
  ```

- Obtain the set of successors of a given state _s_ as in

  ```python
      for successor, action, cost in problem.get_successors(s) :
          ...
  ```

  where `get_successors()` allows you to iterate over a list of tuples with elements:

  - *successor* is a successor to the current state,
  - *action* is the action required to get there from state _s_,
  - and *cost* is the cost of doing the action on state _s_.

Efficient search techniques revolve around the idea of exploring the state
space in an intelligent manner, avoiding the need of revisiting the same state
multiple times. Each state is encapsulated in a node containing the basic
information to reconstruct the path that starting from the initial state lead
to that state. In particular we suggest you to use the _SearchNode_ class
[here](../search_strategies.py), which contains the following attributes:

- The _state_ visited at that step,
- a reference to the _parent_ node,
- the _action_ done on the state in the parent node leading to the current
  state,
- other data, depending on the algorithm. This data usually includes:
  - the accumulated cost _g(n)_, that is the sum of the costs of the actions
    done to reach _state_,
  - the value of one or more heuristics _h(n)_, providing estimates on the
    cost to get to a _goal_ state,
  - the evaluation function _f(n)_ combining actual and estimated costs _f(n)
    = g(n) + h(n)_.

As you have seen in the lecture, a search algorithm makes use of a data
structure representing the frontier of your search problem. Depending on how
you explore this frontier, i.e., the order in which you pick the next element
to be explored, you have a different search strategy. For this reason, we
provide you with different kinds of [frontiers](../frontiers.py). Here's an
example on how to use a queue:

```python
from frontiers import Queue
q = Queue()  # We can now use Queue
```

Some algorithms require you to keep track of the parts already explored, that
aren't to be considered for exploration. This is usually called the **closed
list**; in order to have reasonable efficiency, it is implemented as a hash
table.

In order to help you, and also to help with grading, we provide you with a
readily available implementation of this data structure via the class
`SearchNode` in [search_strategies.py](../search_strategies.py).

### Finding Nodes on the Frontier

One thing that might surprise you when using the frontier data structures is
that in Python, a function can be the parameter of another function! For
example, this is how `find` is implemented in a queue:

```python
def find(self, f: Callable[[T], bool]) -> Optional[T]:
    """ Return some item n from the queue such that f(n) is True.
        Return None if there is no such item. Note that the parameter `f`
        is a function. This method can be slow since in the worst case, we
        need to scan through the entire queue.
    """
    for elem in self.contents:
        if f(elem):
            return elem
    return None
```

Here the parameter `f` is a function that takes an item and return either True
or False. As an example, suppose we have a bunch of fruits and vegetables in
our frontier, and we want to find the first item that contains "bananas". Here's
one way to do it:

```python
from frontiers import Stack
my_frontier = Stack()

# Push three items to the frontier. Each item is a list of words
my_frontier.push(["apples", "are", "delicious", "but", "bruise", "easily"])
my_frontier.push(["bananas", "taste", "awful", "and", "are", "bent"])
my_frontier.push(["carrots", "are", "orange", "and", "are", "not", "fruit"])

# Get the item that contains the word "bananas"
def get_bananana(fruit_info):
    return fruit_info[0] == "bananas"

item = my_frontier.find(get_bananana)
# item should now be: ["bananas", "taste", "awful", "and", "are", "bent"]

# What if I want to find "pears"?
def get_pears(fruit_info):
    return fruit_info[0] == "pears"

item = my_frontier.find(get_pears)
# item should be None
```

Finally we can save two lines of code by using lambda expressions to define
`get_bananana`. The following code is equivalent:

```python
item = my_frontier.find(lambda fruit_info: fruit_info[0] == "bananas")
```

## Adversarial Search Problems

Like all other agents, `MinimaxAgent` has a `get_action` method. This method
creates an instance of an `AdversarialSearchProblem`. Feel free to look at this
class in [search_problems.py](../search_problems.py), but we have
described all of the information which you need below.

In this problem, states are represented as the following tuple:

```python
(player, red_pos, black_pos, yellow_birds, score, yb_value)
```

where:

- `player` is an integer indicating the index of the current player. This is
  the player whose turn it is to play in this state (_0_ for red, _1_ for
  black),
- `red_pos` is a pair _(x,y)_ of integers specifying the red bird's position,
- `black_pos` is a pair _(x,y)_ of integers specifying the black bird's
  position,
- `yellow_birds` is a tuple of pairs specifying the positions of the remaining
  yellow birds,
- `score` is the current score reported by the UI, that is, the sum of the
  values of the yellow birds collected by red minus the values of those
  collected by black,
- `yb_value` is the value of each yellow bird, which decreases at a constant
  rate after each player takes their turn.

The interface of the class `AdversarialSearchProblem` provides you with methods
to access potentially useful information:

- To obtain the index of the _maximizing_ player you can do

  ```python
  max_player_id = problem.get_maximizing_player()
  ```

- If you need to know the index of the opponent player in the given state _s_

  ```Python
  opp_player_id = problem.opponent(s)
  ```

- To obtain the utility (score) of a given state _s_

  ```python
  value = problem.utility(s)
  ```

- To check if the given state _s_ is _terminal_

  ```python
  if problem.terminal_test(s) :
      print("GAME OVER")
  ```

- To iterate over the successors of a given state _s_ you can use the following

  ```python
  for next_state, action, _ in problem.get_successors(s) :
      # do something interesting with next_state
  ```

  note that agents can move onto the other agent position (triggering a
  capture and the end of the game). They cannot stay still (the action _STOP_
  is a special value only usable at the terminal).

- The width and height of the maze can be obtained via

  ```python
  w = problem.get_width()
  h = problem.get_height()
  ```

- The walls in the maze are stored as a matrix of Boolean values which you can access in
  a variety of ways, for instance

  ```python
  for i in range(h) :
      for j in range(w) :
          if problem.get_walls()[i][j] :
              print("CLONK!")
  ```

- If you need to obtain the **exact** distance between any two cells _p1_ and
  _p2_ you can get them through the method `maze_distance`

  ```python
  d_to_opponent =  problem.maze_distance(red_pos, black_pos)
  ```

That's all, you can now move to the [next section](3_breadth_first_search.md)
or go back to the [index](README.md).
