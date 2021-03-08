#!/bin/bash -e

usage() {
    cat <<EOM
  Some shortcuts to help you test the program. For example:
    ./test.sh keyboard anuSearch

    ./test.sh bfs anuSearch
    ./test.sh bfs aiSearch
    ./test.sh bfs mazeSearch

    ./test.sh ids anuSearch
    ./test.sh ids aiSearch
    ./test.sh ids mazeSearch

    ./test.sh astar anuSearch manhattan
    ./test.sh astar aiSearch manhattan
    ./test.sh astar mazeSearch manhattan
    ./test.sh astar mazeSearch euclidean

    ./test.sh heuristic null aiMultiSearch
    ./test.sh heuristic null anuMultiSearch
    ./test.sh heuristic null smallMultiSearch
    ./test.sh heuristic null mazeMultiSearch

    ./test.sh heuristic every_bird aiMultiSearch
    ./test.sh heuristic every_bird anuMultiSearch
    ./test.sh heuristic every_bird smallMultiSearch
    ./test.sh heuristic every_bird mazeMultiSearch

    ./test.sh minimax testAdversarial 8
EOM
    exit 0
}

[[ -z $1 ]] && { usage; }

if [[ $1 = keyboard ]]; then
    [[ -z $2 ]] && { echo "You need to specify a search layout for the keyboard agent." && usage; }
    python3 red_bird.py -l $2 -p KeyboardAgent -b GreedyBlackBirdAgent

elif [[ $1 = bfs ]]; then
    [[ -z $2 ]] && { echo "You need to specify a search layout for BFS." && usage; }
    python3 red_bird.py -l search_layouts/$2.lay -p SearchAgent -a fn=bfs

elif [[ $1 = ids ]]; then
    [[ -z $2 ]] && { echo "You need to specify a search layout for IDS." && usage; }
    python3 red_bird.py -l search_layouts/$2.lay -p SearchAgent -a fn=ids

elif [[ $1 = astar ]]; then
    [[ -z $2 ]] && { echo "You need to specify a search layout for A*." && usage; }
    [[ -z $3 ]] && { echo "You need to specify a heuristic for A*." && usage; }
    python3 red_bird.py -l search_layouts/$2.lay -p SearchAgent -a fn=astar,heuristic=$3

elif [[ $1 = heuristic && $2 = null ]]; then
    [[ -z $3 ]] && { echo "You need to specify a search layout for the null heuristic." && usage; }
    python3 red_bird.py -l search_layouts/$3.lay -p SearchAgent -a fn=astar,prob=MultiplePositionSearchProblem,heuristic=null

elif [[ $1 = heuristic && $2 = every_bird ]]; then
    [[ -z $3 ]] && { echo "You need to specify a search layout for the every_bird heuristic." && usage; }
    python3 red_bird.py -l search_layouts/$3.lay -p SearchAgent -a fn=astar,prob=MultiplePositionSearchProblem,heuristic=every_bird_heuristic

elif [[ $1 = minimax ]]; then
    [[ -z $2 ]] && { echo "You need to specify an advanced search layout for Minimax." && usage; }
    [[ -z $3 ]] && { echo "You need to specify a depth for Minimax." && usage; }
    python3 red_bird.py -p MinimaxAgent -l adv_search_layouts/$2.lay -a depth=${3} -b GreedyBlackBirdAgent --timeout 60 -c

# Print usage if the user gives an invalid argument
else
    echo "Invalid arguments."
    usage

fi
