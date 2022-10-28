/// A small wrapper around a file path, designed to permit more appealing use of parsing and
/// execution functions (i.e., as struct methods)
pub struct Source {
    path: std::path::Path
}
