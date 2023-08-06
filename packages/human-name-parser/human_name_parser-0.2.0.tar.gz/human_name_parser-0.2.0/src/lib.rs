use std::collections::HashMap;

use human_name::Name;
use pyo3::prelude::*;

#[pyfunction]
fn parse_name(name: String) -> PyResult<HashMap<String, Vec<Option<String>>>> {
    let mut result = HashMap::new();

    let n = Name::parse(name.as_str());

    if n.is_none() {
        return Ok(result);
    }

    let n = n.unwrap();

    result.insert(
        "given_name".to_string(),
        vec![n.given_name().map(str::to_string)],
    );
    result.insert(
        "generational_suffix".to_string(),
        vec![n.generational_suffix().map(str::to_string)],
    );
    result.insert(
        "honorific_prefix".to_string(),
        vec![n.honorific_prefix().map(str::to_string)],
    );
    result.insert(
        "honorific_suffix".to_string(),
        vec![n.honorific_suffix().map(str::to_string)],
    );
    result.insert(
        "middle_name".to_string(),
        vec![Some(n.middle_name().unwrap_or_default().to_string())],
    );
    result.insert("surname".to_string(), vec![Some(n.surname().to_string())]);
    result.insert(
        "middle_initials".to_string(),
        vec![n.middle_initials().map(str::to_string)],
    );

    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn human_name_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_name, m)?)?;
    Ok(())
}
