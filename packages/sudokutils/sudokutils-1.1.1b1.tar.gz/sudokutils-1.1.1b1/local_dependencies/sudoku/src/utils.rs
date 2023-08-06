pub struct BitIter {
    n: usize,
}

impl Iterator for BitIter {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.n > 0 {
            let index = self.n.trailing_zeros();
            self.n ^= 1 << index;
            Some(2 << (index - 1))
        } else {
            None
        }
    }
}

pub trait IterBits {
    fn iter_bits(&self) -> BitIter;
}

impl IterBits for usize {
    fn iter_bits(&self) -> BitIter {
        BitIter { n: *self }
    }
}

pub fn string_to_grid(sudoku: &str) -> Result<Vec<usize>, String> {
    let maybe_numbers: Result<Vec<u32>, String> = sudoku
        .chars()
        .map(|c| if ". ".contains(c) { '0' } else { c })
        .map(|c| {
            c.to_digit(10)
                .ok_or_else(|| format!("Invalid character: {}", c))
        })
        .collect();

    match maybe_numbers {
        Ok(numbers) => {
            if numbers.len() == 81 {
                Ok(numbers.into_iter().map(|n| n as usize).collect())
            } else {
                Err("Not enough characters".to_string())
            }
        }
        Err(error) => Err(error),
    }
}

pub fn grid_to_string(grid: &[usize]) -> String {
    return String::from_utf8(grid.iter().map(|&c| c as u8 + 48).collect()).unwrap();
}
