use pyo3::prelude::*;

#[pyclass]
#[allow(clippy::upper_case_acronyms)]
enum Difficulty {
    EASY,
    MEDIUM,
    HARD,
}

#[pyfunction]
fn generate_sudoku() -> Vec<usize> {
    let mut generator = sudoku::Generator::new();
    generator.generate_sudoku()
}

#[pyfunction]
fn generate_sudoku_with_difficulty(difficulty: &Difficulty) -> Vec<usize> {
    let mut generator = sudoku::Generator::new();
    match difficulty {
        Difficulty::EASY => generator.generate_sudoku_with_empty(0, 55),
        Difficulty::MEDIUM => generator.generate_sudoku_with_empty(56, 57),
        Difficulty::HARD => generator.generate_sudoku_with_empty(58, 81),
    }
}

#[pyfunction]
fn is_solved_sudoku(grid: Vec<usize>) -> bool {
    if grid.len() != 81 {
        return false;
    }
    if !grid.iter().all(|&n| (1..=9).contains(&n)) {
        return false;
    }
    let mut solver = sudoku::Solver::new();

    if solver.is_valid_puzzle(&grid) {
        return true;
    }
    false
}

#[pymodule]
fn sudokutils(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_sudoku, m)?)?;

    m.add_class::<Difficulty>()?;
    m.add_function(wrap_pyfunction!(generate_sudoku_with_difficulty, m)?)?;
    m.add_function(wrap_pyfunction!(is_solved_sudoku, m)?)?;
    Ok(())
}
