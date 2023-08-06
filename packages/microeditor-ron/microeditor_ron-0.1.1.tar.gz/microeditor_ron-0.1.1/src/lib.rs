pub mod global_transform;
pub mod parent;
pub mod transform;

use pyo3::prelude::*;

#[pymodule]
fn microeditor_ron(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(global_transform::global_transform, m)?)?;
    m.add_function(wrap_pyfunction!(transform::transform, m)?)?;
    m.add_function(wrap_pyfunction!(parent::parent, m)?)?;
    Ok(())
}
