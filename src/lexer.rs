use lazy_static::lazy_static;
use std::collections::HashMap;

const ANSI_RESET: &str = "\x1b[0m";

lazy_static! {
    static ref STYLES: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();

        // Text attributes
        m.insert("b", "\x1b[1m");
        m.insert("bold", "\x1b[1m");
        m.insert("dim", "\x1b[2m");
        m.insert("i", "\x1b[3m");
        m.insert("italic", "\x1b[3m");
        m.insert("u", "\x1b[4m");
        m.insert("underline", "\x1b[4m");
        m.insert("blink", "\x1b[5m");
        m.insert("inverse", "\x1b[7m");
        m.insert("reverse", "\x1b[7m");
        m.insert("hidden", "\x1b[8m");
        m.insert("s", "\x1b[9m");
        m.insert("strike", "\x1b[9m");
        m.insert("strikethrough", "\x1b[9m");
        m.insert("overline", "\x1b[53m");

        // Standard foreground colors
        m.insert("black", "\x1b[30m");
        m.insert("red", "\x1b[31m");
        m.insert("green", "\x1b[32m");
        m.insert("yellow", "\x1b[33m");
        m.insert("blue", "\x1b[34m");
        m.insert("magenta", "\x1b[35m");
        m.insert("cyan", "\x1b[36m");
        m.insert("white", "\x1b[37m");

        // Bright foreground colors
        m.insert("bright_black", "\x1b[90m");
        m.insert("grey", "\x1b[90m");
        m.insert("gray", "\x1b[90m");
        m.insert("bright_red", "\x1b[91m");
        m.insert("bright_green", "\x1b[92m");
        m.insert("bright_yellow", "\x1b[93m");
        m.insert("bright_blue", "\x1b[94m");
        m.insert("bright_magenta", "\x1b[95m");
        m.insert("bright_cyan", "\x1b[96m");
        m.insert("bright_white", "\x1b[97m");

        // Standard background colors
        m.insert("on_black", "\x1b[40m");
        m.insert("on_red", "\x1b[41m");
        m.insert("on_green", "\x1b[42m");
        m.insert("on_yellow", "\x1b[43m");
        m.insert("on_blue", "\x1b[44m");
        m.insert("on_magenta", "\x1b[45m");
        m.insert("on_cyan", "\x1b[46m");
        m.insert("on_white", "\x1b[47m");

        // Bright background colors
        m.insert("on_bright_black", "\x1b[100m");
        m.insert("on_grey", "\x1b[100m");
        m.insert("on_gray", "\x1b[100m");
        m.insert("on_bright_red", "\x1b[101m");
        m.insert("on_bright_green", "\x1b[102m");
        m.insert("on_bright_yellow", "\x1b[103m");
        m.insert("on_bright_blue", "\x1b[104m");
        m.insert("on_bright_magenta", "\x1b[105m");
        m.insert("on_bright_cyan", "\x1b[106m");
        m.insert("on_bright_white", "\x1b[107m");

        m
    };
}

/// Resolve a single style token to its ANSI escape sequence.
/// Handles both static names (from the STYLES table) and dynamic parameterized
/// styles like `color(N)`, `on_color(N)`, `rgb(R,G,B)`, `on_rgb(R,G,B)`,
/// `#RRGGBB`, and `on_#RRGGBB`.
fn resolve_token(token: &str) -> Option<String> {
    // Static lookup first
    if let Some(&code) = STYLES.get(token) {
        return Some(code.to_string());
    }

    // color(N) — 256-color foreground
    if let Some(inner) = token
        .strip_prefix("color(")
        .and_then(|s| s.strip_suffix(')'))
    {
        if let Ok(n) = inner.trim().parse::<u8>() {
            return Some(format!("\x1b[38;5;{}m", n));
        }
    }

    // on_color(N) — 256-color background
    if let Some(inner) = token
        .strip_prefix("on_color(")
        .and_then(|s| s.strip_suffix(')'))
    {
        if let Ok(n) = inner.trim().parse::<u8>() {
            return Some(format!("\x1b[48;5;{}m", n));
        }
    }

    // rgb(R,G,B) — truecolor foreground
    if let Some(inner) = token.strip_prefix("rgb(").and_then(|s| s.strip_suffix(')')) {
        if let Some(code) = parse_rgb(inner, false) {
            return Some(code);
        }
    }

    // on_rgb(R,G,B) — truecolor background
    if let Some(inner) = token
        .strip_prefix("on_rgb(")
        .and_then(|s| s.strip_suffix(')'))
    {
        if let Some(code) = parse_rgb(inner, true) {
            return Some(code);
        }
    }

    // on_#RRGGBB — hex truecolor background (check before #RRGGBB)
    if let Some(hex) = token.strip_prefix("on_#") {
        if let Some(code) = parse_hex(hex, true) {
            return Some(code);
        }
    }

    // #RRGGBB — hex truecolor foreground
    if let Some(hex) = token.strip_prefix('#') {
        if let Some(code) = parse_hex(hex, false) {
            return Some(code);
        }
    }

    None
}

fn parse_rgb(inner: &str, background: bool) -> Option<String> {
    let parts: Vec<&str> = inner.split(',').collect();
    if parts.len() != 3 {
        return None;
    }
    let r = parts[0].trim().parse::<u8>().ok()?;
    let g = parts[1].trim().parse::<u8>().ok()?;
    let b = parts[2].trim().parse::<u8>().ok()?;
    let layer = if background { 48 } else { 38 };
    Some(format!("\x1b[{};2;{};{};{}m", layer, r, g, b))
}

fn parse_hex(hex: &str, background: bool) -> Option<String> {
    if hex.len() != 6 {
        return None;
    }
    let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
    let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
    let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
    let layer = if background { 48 } else { 38 };
    Some(format!("\x1b[{};2;{};{};{}m", layer, r, g, b))
}

/// Resolve all space-separated tokens in a compound tag and return the
/// concatenated ANSI codes. Returns None if any token is unrecognized.
fn resolve_compound(tag: &str) -> Option<String> {
    let mut codes = String::new();
    for token in tag.split_whitespace() {
        codes.push_str(&resolve_token(token)?);
    }
    Some(codes)
}

pub fn apply_styles(text: &str) -> String {
    let mut result = String::new();
    let mut style_stack: Vec<String> = Vec::new();
    let mut in_tag = false;
    let mut current_tag = String::new();

    let chars: Vec<char> = text.chars().collect();
    let mut i = 0;

    while i < chars.len() {
        match chars[i] {
            '[' => {
                if i + 1 < chars.len() {
                    let next_char = chars[i + 1];
                    if next_char.is_alphabetic() || next_char == '/' || next_char == '#' {
                        in_tag = true;
                        current_tag.clear();
                        i += 1;
                        continue;
                    }
                }
                result.push(chars[i]);
            }
            ']' if in_tag => {
                in_tag = false;
                if let Some(tag_name) = current_tag.strip_prefix('/') {
                    // Closing tag
                    if let Some(pos) = style_stack.iter().rposition(|s| s == tag_name) {
                        style_stack.truncate(pos);
                        result.push_str(ANSI_RESET);
                        // Reapply remaining styles
                        for style_entry in &style_stack {
                            if let Some(codes) = resolve_compound(style_entry) {
                                result.push_str(&codes);
                            }
                        }
                    } else {
                        result.push('[');
                        result.push_str(&current_tag);
                        result.push(']');
                    }
                } else {
                    // Opening tag
                    if let Some(codes) = resolve_compound(&current_tag) {
                        style_stack.push(current_tag.clone());
                        result.push_str(&codes);
                    } else {
                        result.push('[');
                        result.push_str(&current_tag);
                        result.push(']');
                    }
                }
                current_tag.clear();
            }
            _ if in_tag => {
                current_tag.push(chars[i]);
            }
            _ => {
                result.push(chars[i]);
            }
        }
        i += 1;
    }

    if !style_stack.is_empty() {
        result.push_str(ANSI_RESET);
    }

    result
}
