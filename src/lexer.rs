use std::collections::HashMap;
use lazy_static::lazy_static;

const ANSI_RESET: &str = "\x1b[0m";

// Define mappings for styles to ANSI codes
lazy_static! {
    static ref STYLES: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();
        m.insert("b", "\x1b[1m");    // Bold
        m.insert("u", "\x1b[4m");    // Underline
        m.insert("red", "\x1b[31m"); // Red foreground
        // Add more styles as needed
        m
    };
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
                // Check if it's a potential tag opener, not just a literal '['
                if i + 1 < chars.len() {
                    let next_char = chars[i+1];
                    if next_char.is_alphabetic() || next_char == '/' {
                        in_tag = true;
                        current_tag.clear();
                        i += 1; // Move past '['
                        continue;
                    }
                }
                result.push(chars[i]); // Not a tag, push literal '['
            }
            ']' if in_tag => {
                in_tag = false;
                if current_tag.starts_with('/') {
                    // Closing tag
                    let tag_name = &current_tag[1..];
                    if let Some(pos) = style_stack.iter().rposition(|s| s == tag_name) {
                        // Pop styles until the matching tag is found (inclusive)
                        for _ in pos..style_stack.len() {
                            style_stack.pop();
                        }
                        result.push_str(ANSI_RESET);
                        // Reapply remaining styles
                        for style_name in &style_stack {
                            if let Some(&code) = STYLES.get(style_name.as_str()) {
                                result.push_str(code);
                            }
                        }
                    } else {
                        // Mismatched closing tag, treat as literal
                        result.push('[');
                        result.push_str(&current_tag);
                        result.push(']');
                    }
                } else {
                    // Opening tag
                    if let Some(&code) = STYLES.get(current_tag.as_str()) {
                        style_stack.push(current_tag.clone());
                        result.push_str(code);
                    } else {
                        // Unrecognized opening tag, treat as literal
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

    // After processing all characters, if there are still active styles, reset them
    if !style_stack.is_empty() {
        result.push_str(ANSI_RESET);
    }

    result
}
