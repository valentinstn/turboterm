use clap::{Arg, ArgAction, Command};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::HashMap;

// --- Internal CLI parameter representation ---

#[derive(Debug, Clone)]
enum ParamKind {
    Positional,
    Option { flag_names: Vec<String> },
}

struct CliParam {
    name: String,
    kind: ParamKind,
    help: String,
    type_annotation: Option<Py<PyAny>>,
    default_value: Option<Py<PyAny>>,
    is_bool_flag: bool,
    required: bool,
}

#[allow(dead_code)]
struct PyCliCommand {
    name: String,
    func: Py<PyAny>,
    doc: Option<String>,
    params: Vec<CliParam>,
}

static CLI_COMMAND_REGISTRY: std::sync::LazyLock<std::sync::Mutex<HashMap<String, PyCliCommand>>> =
    std::sync::LazyLock::new(|| std::sync::Mutex::new(HashMap::new()));

/// Register a command with pre-processed parameter metadata.
/// Called from the Python `@command()` decorator which handles signature inspection.
#[pyfunction]
#[pyo3(signature = (name, func, doc=None, params=vec![]))]
pub fn register_command(
    _py: Python,
    name: String,
    func: Py<PyAny>,
    doc: Option<String>,
    params: Vec<Bound<'_, PyDict>>,
) -> PyResult<()> {
    let mut cli_params = Vec::new();

    for param_dict in params {
        let param_name: String = param_dict
            .get_item("name")?
            .ok_or_else(|| PyValueError::new_err("param missing 'name'"))?
            .extract()?;
        let kind_str: String = param_dict
            .get_item("kind")?
            .ok_or_else(|| PyValueError::new_err("param missing 'kind'"))?
            .extract()?;
        let help: String = param_dict
            .get_item("help")?
            .map(|v| v.extract().unwrap_or_default())
            .unwrap_or_default();
        let required: bool = param_dict
            .get_item("required")?
            .map(|v| v.extract().unwrap_or(true))
            .unwrap_or(true);

        let type_ann = param_dict
            .get_item("type")?
            .filter(|v| !v.is_none())
            .map(|v| v.unbind());

        let default_val = param_dict.get_item("default")?.map(|v| v.unbind());

        let kind = if kind_str == "option" {
            let flags: Vec<String> = param_dict
                .get_item("flags")?
                .ok_or_else(|| PyValueError::new_err("option param missing 'flags'"))?
                .extract()?;
            ParamKind::Option { flag_names: flags }
        } else {
            ParamKind::Positional
        };

        let is_bool = if kind_str == "option" {
            param_dict
                .get_item("is_bool")?
                .map(|v| v.extract().unwrap_or(false))
                .unwrap_or(false)
        } else {
            false
        };

        cli_params.push(CliParam {
            name: param_name,
            kind,
            help,
            type_annotation: type_ann,
            default_value: default_val,
            is_bool_flag: is_bool,
            required,
        });
    }

    let command = PyCliCommand {
        name: name.clone(),
        func,
        doc,
        params: cli_params,
    };

    let mut registry = CLI_COMMAND_REGISTRY.lock().unwrap();
    registry.insert(name, command);
    Ok(())
}

/// Convert a string CLI value to a Python object using the type annotation as constructor.
fn convert_value(
    py: Python,
    val: &str,
    type_annotation: &Option<Py<PyAny>>,
) -> PyResult<Py<PyAny>> {
    if let Some(ty) = type_annotation {
        // Call the Python type: int("42"), float("3.14"), str("hello"), etc.
        ty.call1(py, (val,))
    } else {
        // No annotation — pass as string
        Ok(val.into_pyobject(py).unwrap().into_any().unbind())
    }
}

/// Snapshot of CliParam data needed for clap (no Py<PyAny> fields, all owned).
struct ClapParamInfo {
    name: String,
    kind: ParamKind,
    help: String,
    is_bool_flag: bool,
    required: bool,
}

struct ClapCommandInfo {
    name: String,
    doc: Option<String>,
    params: Vec<ClapParamInfo>,
}

fn build_clap_app(commands: &[ClapCommandInfo]) -> Command {
    let mut app = Command::new("app".to_string())
        .subcommand_required(true)
        .arg_required_else_help(true);

    for cmd in commands {
        let mut subcmd = Command::new(cmd.name.clone());
        if let Some(ref doc) = cmd.doc {
            subcmd = subcmd.about(doc.clone());
        }

        for param in &cmd.params {
            match &param.kind {
                ParamKind::Positional => {
                    let mut arg = Arg::new(param.name.clone()).required(param.required);
                    if !param.help.is_empty() {
                        arg = arg.help(param.help.clone());
                    }
                    subcmd = subcmd.arg(arg);
                }
                ParamKind::Option { flag_names } => {
                    let mut arg = Arg::new(param.name.clone());
                    if !param.help.is_empty() {
                        arg = arg.help(param.help.clone());
                    }
                    for flag in flag_names {
                        if let Some(long_name) = flag.strip_prefix("--") {
                            arg = arg.long(long_name.to_string());
                        } else if flag.starts_with('-') && flag.len() == 2 {
                            arg = arg.short(flag.chars().nth(1).unwrap());
                        }
                    }
                    if param.is_bool_flag {
                        arg = arg.action(ArgAction::SetTrue);
                    } else {
                        arg = arg.required(param.required);
                    }
                    subcmd = subcmd.arg(arg);
                }
            }
        }

        app = app.subcommand(subcmd);
    }

    app
}

#[pyfunction]
pub fn run_cli(py: Python, args: Vec<String>) -> PyResult<()> {
    // Phase 1: Snapshot clap-relevant data from registry (owned strings only)
    let clap_commands: Vec<ClapCommandInfo> = {
        let registry = CLI_COMMAND_REGISTRY.lock().unwrap();
        registry
            .iter()
            .map(|(name, cmd)| ClapCommandInfo {
                name: name.clone(),
                doc: cmd.doc.clone(),
                params: cmd
                    .params
                    .iter()
                    .map(|p| ClapParamInfo {
                        name: p.name.clone(),
                        kind: p.kind.clone(),
                        help: p.help.clone(),
                        is_bool_flag: p.is_bool_flag,
                        required: p.required,
                    })
                    .collect(),
            })
            .collect()
    }; // registry lock dropped here

    // Phase 2: Build clap command from owned data and parse
    let app = build_clap_app(&clap_commands);

    let full_args: Vec<&str> = std::iter::once("app")
        .chain(args.iter().map(|s| s.as_str()))
        .collect();

    let matches = match app.try_get_matches_from(full_args) {
        Ok(m) => m,
        Err(e) => match e.kind() {
            clap::error::ErrorKind::DisplayHelp | clap::error::ErrorKind::DisplayVersion => {
                print!("{}", e);
                return Ok(());
            }
            _ => return Err(PyValueError::new_err(e.to_string())),
        },
    };

    let (subcmd_name, subcmd_matches) = matches
        .subcommand()
        .ok_or_else(|| PyValueError::new_err("No subcommand provided"))?;

    // Phase 3: Re-lock registry for dispatch
    let registry = CLI_COMMAND_REGISTRY.lock().unwrap();
    let cmd = registry
        .get(subcmd_name)
        .ok_or_else(|| PyValueError::new_err(format!("Unknown command: {}", subcmd_name)))?;

    // Build kwargs from parsed arguments
    let kwargs = PyDict::new(py);

    for param in &cmd.params {
        match &param.kind {
            ParamKind::Positional => {
                if let Some(val) = subcmd_matches.get_one::<String>(param.name.as_str()) {
                    let converted = convert_value(py, val, &param.type_annotation)?;
                    kwargs.set_item(&param.name, converted)?;
                } else if let Some(ref default) = param.default_value {
                    kwargs.set_item(&param.name, default.bind(py))?;
                }
            }
            ParamKind::Option { .. } => {
                if param.is_bool_flag {
                    let val = subcmd_matches.get_flag(param.name.as_str());
                    kwargs.set_item(&param.name, val)?;
                } else if let Some(val) = subcmd_matches.get_one::<String>(param.name.as_str()) {
                    let converted = convert_value(py, val, &param.type_annotation)?;
                    kwargs.set_item(&param.name, converted)?;
                } else if let Some(ref default) = param.default_value {
                    kwargs.set_item(&param.name, default.bind(py))?;
                }
            }
        }
    }

    cmd.func.bind(py).call((), Some(&kwargs))?;

    Ok(())
}
