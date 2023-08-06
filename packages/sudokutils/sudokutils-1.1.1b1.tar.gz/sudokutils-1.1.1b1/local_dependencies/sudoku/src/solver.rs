use rand::{rngs::StdRng, seq::SliceRandom, SeedableRng};

use crate::{
    constants::{PEER_INDICES, UNIT_INDICES},
    utils::IterBits,
};

// Constant representing a cell that could be all of the possible values.
// Each bit represents a possible digit. This is equivalent to: 0b1111111110
// Where each bit corresponds to the following digits:            987654321
const ALL_POSSIBLE: usize = (2 << 9) - 2;

pub struct SudokuSolver {
    // For efficiency, this is created once so it can be reused over different solves
    eliminate_stack: Vec<(usize, usize)>,
    pub rng: StdRng,
}

impl Default for SudokuSolver {
    fn default() -> Self {
        Self::new()
    }
}

impl SudokuSolver {
    pub fn new() -> Self {
        Self {
            eliminate_stack: Vec::<(usize, usize)>::with_capacity(1000),
            rng: StdRng::from_entropy(),
        }
    }

    pub fn with_seed(seed: u64) -> Self {
        Self {
            eliminate_stack: Vec::<(usize, usize)>::with_capacity(1000),
            rng: StdRng::seed_from_u64(seed),
        }
    }

    fn possible_from_grid(&mut self, grid: &[usize]) -> Vec<usize> {
        let mut possible = vec![ALL_POSSIBLE; 81];
        for (i, &cell) in grid.iter().enumerate() {
            if cell != 0 {
                self.eliminate(&mut possible, i, 2 << (cell - 1));
            }
        }
        possible
    }

    #[allow(dead_code)]
    fn possible_from_grid_fast(&self, grid: &[usize]) -> Vec<usize> {
        let mut possible = Vec::with_capacity(81);
        for i in 0..81 {
            if grid[i] == 0 {
                // Calculate possible values with a quick search over neighbours.
                possible.push(
                    ALL_POSSIBLE
                        & !PEER_INDICES[i]
                            .iter()
                            // Filter out neighbours that aren't numbers
                            .filter(|&&idx| grid[idx] != 0)
                            // Map the values to the bitwise representation.
                            .map(|&idx| 2 << (grid[idx] - 1))
                            // Combine all values using bitwise or.
                            .fold(0, |acc, v| acc | v),
                );
            } else {
                // Push value with only the digit set
                possible.push(2 << (grid[i] - 1));
            }
        }
        possible
    }

    fn grid_from_possible(&self, possible: &[usize]) -> Option<Vec<usize>> {
        return possible
            .iter()
            .map(|&c| {
                if c.is_power_of_two() {
                    Some(c.trailing_zeros() as usize)
                } else {
                    None
                }
            })
            .collect();
    }

    fn eliminate(&mut self, possible: &mut [usize], first_pos: usize, first_val: usize) -> bool {
        self.eliminate_stack.clear();
        for power in (possible[first_pos] - first_val).iter_bits() {
            self.eliminate_stack.push((first_pos, power));
        }

        while let Some((pos, val)) = self.eliminate_stack.pop() {
            debug_assert_ne!(possible[pos] & 1, 1);

            // Assert that the value wasn't already eliminated
            if (val & possible[pos]) == 0 {
                continue;
            }

            // Eliminate the value
            possible[pos] -= val;

            if possible[pos] == 0 {
                // There are no possible values for this cell, meaning the guess was incorrect.
                return false;
            } else if possible[pos].is_power_of_two() {
                // The value has been found, eliminate all neighbour cells.
                self.eliminate_stack.extend(
                    PEER_INDICES[pos]
                        .iter()
                        .map(|peer_pos| (*peer_pos, possible[pos])),
                );
            }

            // For each shared column, row, and cell index
            for unit in UNIT_INDICES[pos] {
                // Create an iterator of neighbours that could be `val`
                let mut iterator = unit.iter().filter(|&&peer| (val & possible[peer]) != 0);

                // If there is only one, assign it. If there are none, it is an impossible
                // condition.
                if let Some(&first) = iterator.next() {
                    if iterator.next().is_none() {
                        for power in (possible[first] - val).iter_bits() {
                            self.eliminate_stack.push((first, power));
                        }
                    }
                } else {
                    return false;
                }
            }
        }
        true
    }

    pub fn solve(&mut self, grid: &[usize]) -> Option<Vec<usize>> {
        let possible = self.possible_from_grid(grid);
        let maybe_solution = self._solve(&possible);
        maybe_solution.map(|solution| self.grid_from_possible(&solution).unwrap())
    }

    fn _solve(&mut self, possible: &[usize]) -> Option<Vec<usize>> {
        // Get the cell with the lowest number of possibilites, to guess from.
        let min_pos = self.get_min_pos(possible);

        if let Some(min_pos) = min_pos {
            for power in possible[min_pos].iter_bits() {
                let mut possible_copy = possible.to_owned();
                // Remove that value, and continue to recursively solve if that works.
                if self.eliminate(&mut possible_copy, min_pos, power) {
                    if let Some(x) = self._solve(&possible_copy) {
                        // Keep passing the solution back along
                        return Some(x);
                    }
                }
            }
            // Went down a wrong track; no solutions here
            None
        } else {
            // Found a solution
            Some(possible.to_vec())
        }
    }

    pub fn solve_random(&mut self, grid: &[usize]) -> Option<Vec<usize>> {
        let possible = self.possible_from_grid(grid);
        let maybe_solution = self._solve_random(&possible);
        maybe_solution.map(|solution| self.grid_from_possible(&solution).unwrap())
    }

    fn _solve_random(&mut self, possible: &[usize]) -> Option<Vec<usize>> {
        // Get the cell with the lowest number of possibilites, to guess from.
        let min_pos = self.get_min_pos_rand(possible);

        if let Some(min_pos) = min_pos {
            let mut bits: Vec<usize> = possible[min_pos].iter_bits().collect();
            bits.shuffle(&mut self.rng);
            for power in bits {
                let mut possible_copy = possible.to_owned();
                // Remove that value, and continue to recursively solve if that works.
                if self.eliminate(&mut possible_copy, min_pos, power) {
                    if let Some(x) = self._solve_random(&possible_copy) {
                        // Keep passing the solution back along
                        return Some(x);
                    }
                }
            }
            // Went down a wrong track; no solutions here
            None
        } else {
            // Found a solution
            Some(possible.to_vec())
        }
    }

    pub fn is_valid_puzzle(&mut self, grid: &[usize]) -> bool {
        let possible = self.possible_from_grid(grid);
        self._is_valid_puzzle(&possible, 0) == 1
    }

    /// Returns 0 if there are no solutions, 1 if there a single solution,
    /// and 2 if there is more than 1 solution.
    fn _is_valid_puzzle(&mut self, possible: &[usize], mut count: usize) -> usize {
        // Get the cell with the lowest number of possibilites, to guess from.
        let min_pos = self.get_min_pos(possible);

        if let Some(min_pos) = min_pos {
            for power in possible[min_pos].iter_bits() {
                let mut possible_copy = possible.to_owned();
                // Remove that value, and continue to recursively solve if that works.
                if self.eliminate(&mut possible_copy, min_pos, power) {
                    count = self._is_valid_puzzle(&possible_copy, count);
                    if count >= 2 {
                        return count;
                    }
                }
            }
            count
        } else {
            // Found a solution
            count + 1
        }
    }

    fn get_min_pos_rand(&mut self, possible: &[usize]) -> Option<usize> {
        let mut indexes: Vec<usize> = (0..81).collect();
        indexes.shuffle(&mut self.rng);

        indexes
            .into_iter()
            .filter(|&elem| !possible[elem].is_power_of_two())
            .min_by_key(|&elem| possible[elem].count_ones())
    }

    fn get_min_pos(&self, possible: &[usize]) -> Option<usize> {
        (0..81)
            .into_iter()
            .filter(|&elem| !possible[elem].is_power_of_two())
            .min_by_key(|&elem| possible[elem].count_ones())
    }
}
