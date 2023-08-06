use std::iter::zip;

use rand::seq::SliceRandom;

use crate::solver::SudokuSolver;

pub struct SudokuGenerator {
    solver: SudokuSolver,
}

impl Default for SudokuGenerator {
    fn default() -> Self {
        Self::new()
    }
}

impl SudokuGenerator {
    pub fn new() -> Self {
        Self {
            solver: SudokuSolver::new(),
        }
    }

    pub fn with_seed(seed: u64) -> Self {
        Self {
            solver: SudokuSolver::with_seed(seed),
        }
    }

    fn try_remove(&mut self, sudoku: &mut [usize], to_remove: &Vec<usize>) -> bool {
        let saved_values: Vec<usize> = to_remove.iter().map(|&idx| sudoku[idx]).collect();

        for &idx in to_remove {
            sudoku[idx] = 0;
        }

        if self.solver.is_valid_puzzle(sudoku) {
            true
        } else {
            for (&idx, val) in zip(to_remove, saved_values) {
                sudoku[idx] = val;
            }
            false
        }
    }

    pub fn generate_sudoku(&mut self) -> Vec<usize> {
        let mut question = self.solver.solve_random(&vec![0; 81]).unwrap();

        let mut to_remove: Vec<usize> = (0..81).collect();
        to_remove.shuffle(&mut self.solver.rng);

        let mut chunk_size = 15;

        while !to_remove.is_empty() {
            // Take `chunk` cells from the end to remove them.
            let chunk: Vec<usize> = to_remove.iter().rev().take(chunk_size).copied().collect();

            // Heuristics to try and remove multiple cells at once.
            if self.try_remove(&mut question, &chunk) || chunk_size == 1 {
                to_remove.truncate(to_remove.len() - chunk_size);

                if chunk_size == 1 {
                    if to_remove.len() >= 60 {
                        chunk_size = 8;
                    } else if to_remove.len() >= 40 {
                        chunk_size = 4;
                    }
                }
            } else {
                chunk_size /= 2;
                if chunk_size <= 2 {
                    chunk_size = 1;
                }
            }
        }
        question
    }

    pub fn generate_sudoku_with_empty(&mut self, min_empty: usize, max_empty: usize) -> Vec<usize> {
        loop {
            let sudoku = self.generate_sudoku();

            let empty_count = sudoku.iter().filter(|&&c| c == 0).count();
            if min_empty <= empty_count && empty_count <= max_empty {
                return sudoku;
            }
        }
    }
}
