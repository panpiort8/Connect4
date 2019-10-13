# Connect4

Implementation of two bots playing Connect 4: Monte Carlo Search Tree and Alpha-Beta Cut.


## Usage

One can watch algorithms competing by running: 
```bash
python3 ./simulate_game.py -w alphabeta -b mctree
```
or play with bot:
```bash 
python3 ./simulate_game.py -w player -b mctree
```

## Results

Algorithms were compared by running compare_algos.py script. Alpha-Beta Cut turned out to be pretty better even after tuning MCTS parameters. MCTS was at its best with &gamma;=1 and *rollouts*=1 (number of averaged simulations per rollout) and won 38%, lost 58% and drew 4% of 100 games (regardless of the reaction time, which was set to 0.1s, 0.2s or 0.5s).