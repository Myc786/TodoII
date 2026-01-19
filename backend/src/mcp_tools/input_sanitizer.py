"""
Input Sanitizer for Todo Chatbot Extension

This module implements input sanitization to prevent various injection
attacks and ensure safe handling of user input.
"""

from typing import Dict, Any, Union, List
import html
import re
import logging


class InputSanitizer:
    """
    Sanitizes user inputs to prevent injection attacks and other security vulnerabilities.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        # Regex patterns for common injection attempts
        self.dangerous_patterns = {
            'sql_injection': [
                r"(?i)(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bDROP\b|\bUPDATE\b|\bCREATE\b|\bEXEC\b|\bEXECUTE\b)",
                r"(?i)(\bOR\b\s+1\s*=\s*1|\bAND\b\s+1\s*=\s*1)",
                r"--\s*.*$",
                r"/\*.*?\*/",
                r"'[^']*exec\b.*\('[^']*'|exec\b.*\('[^']*'"
            ],
            'xss_injection': [
                r"(?i)<script[^>]*>.*?</script>",
                r"(?i)<iframe[^>]*>.*?</iframe>",
                r"(?i)<img[^>]*onload\s*=|<img[^>]*onerror\s*=|<img[^>]*onclick\s*=",
                r"(?i)javascript:",
                r"(?i)vbscript:",
                r"(?i)on\w+\s*=",
                r"(?i)data:text/html",
                r"(?i)<svg[^>]*onload\s*="
            ],
            'command_injection': [
                r"(?i)\|\s*.*",
                r"(?i);\s*.*",
                r"(?i)`.*`",
                r"(?i)\$\(.*\)",
                r"(?i)%.*%",
                r"(?i)&\s*.*&",
            ],
            'prompt_injection': [
                r"(?i)Ignore the above instructions",
                r"(?i)Disregard previous commands",
                r"(?i)Forget all prior instructions",
                r"(?i)System:",
                r"(?i)Human:",
                r"(?i)Assistant:",
                r"(?i)You are now",
                r"(?i)Your new role is",
                r"(?i)Act as",
                r"(?i)Pretend you are",
                r"(?i)### Instruction:",
                r"(?i)\[INST\]",
                r"(?i)\[/INST\]",
                r"(?i)### Response:"
            ]
        }

        # Pre-compile regex patterns for performance
        self.compiled_patterns = {}
        for category, patterns in self.dangerous_patterns.items():
            self.compiled_patterns[category] = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in patterns]

    def sanitize_string(self, input_string: str, max_length: int = 1000) -> str:
        """
        Sanitize a string input.

        Args:
            input_string: Input string to sanitize
            max_length: Maximum allowed length (default 1000)

        Returns:
            Sanitized string
        """
        if input_string is None:
            return ""

        # Convert to string if not already
        if not isinstance(input_string, str):
            input_string = str(input_string)

        # Check for excessive length
        if len(input_string) > max_length:
            self.logger.warning(f"Input string exceeds maximum length of {max_length} characters")
            input_string = input_string[:max_length]

        # Remove null bytes which can be used in various exploits
        input_string = input_string.replace('\x00', '[NULL]')

        # HTML encode dangerous characters to prevent XSS
        input_string = html.escape(input_string)

        # Check for and filter dangerous patterns
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(input_string):
                    self.logger.warning(f"Dangerous {category} pattern detected in input: {input_string[:100]}...")
                    # Replace the pattern with a safe placeholder
                    input_string = pattern.sub(f"[{category.upper()}_FILTERED]", input_string)

        return input_string

    def sanitize_dict(self, input_dict: Dict[str, Any], max_depth: int = 3, max_length: int = 1000) -> Dict[str, Any]:
        """
        Recursively sanitize a dictionary.

        Args:
            input_dict: Dictionary to sanitize
            max_depth: Maximum recursion depth (default 3)
            max_length: Maximum length for string values (default 1000)

        Returns:
            Sanitized dictionary
        """
        if max_depth <= 0:
            self.logger.warning("Maximum sanitization depth reached")
            return input_dict

        sanitized_dict = {}
        for key, value in input_dict.items():
            # Sanitize the key
            if isinstance(key, str):
                safe_key = self.sanitize_string(key, max_length)
            else:
                safe_key = key

            # Sanitize the value
            sanitized_dict[safe_key] = self._sanitize_value(value, max_depth - 1, max_length)

        return sanitized_dict

    def sanitize_list(self, input_list: List[Any], max_depth: int = 3, max_length: int = 1000) -> List[Any]:
        """
        Recursively sanitize a list.

        Args:
            input_list: List to sanitize
            max_depth: Maximum recursion depth (default 3)
            max_length: Maximum length for string values (default 1000)

        Returns:
            Sanitized list
        """
        if max_depth <= 0:
            self.logger.warning("Maximum sanitization depth reached")
            return input_list

        sanitized_list = []
        for item in input_list:
            sanitized_list.append(self._sanitize_value(item, max_depth - 1, max_length))

        return sanitized_list

    def _sanitize_value(self, value: Any, max_depth: int, max_length: int) -> Any:
        """
        Internal helper to sanitize different value types.

        Args:
            value: Value to sanitize
            max_depth: Remaining recursion depth
            max_length: Maximum length for string values

        Returns:
            Sanitized value
        """
        if isinstance(value, str):
            return self.sanitize_string(value, max_length)
        elif isinstance(value, dict):
            return self.sanitize_dict(value, max_depth, max_length)
        elif isinstance(value, list):
            return self.sanitize_list(value, max_depth, max_length)
        else:
            # For other types (int, float, bool, None), return as is
            return value

    def validate_json_structure(self, data: Union[Dict[str, Any], List[Any]], max_depth: int = 5, max_elements: int = 100) -> bool:
        """
        Validate that JSON structure is reasonable and not too deep or large.

        Args:
            data: JSON data to validate
            max_depth: Maximum allowed nesting depth
            max_elements: Maximum allowed elements at any level

        Returns:
            True if structure is valid, False otherwise
        """
        def _validate_recursive(obj, current_depth=0):
            if current_depth > max_depth:
                self.logger.warning(f"JSON structure exceeds maximum depth of {max_depth}")
                return False

            if isinstance(obj, dict):
                if len(obj) > max_elements:
                    self.logger.warning(f"Dictionary has too many elements: {len(obj)} > {max_elements}")
                    return False
                return all(_validate_recursive(v, current_depth + 1) for v in obj.values())
            elif isinstance(obj, list):
                if len(obj) > max_elements:
                    self.logger.warning(f"List has too many elements: {len(obj)} > {max_elements}")
                    return False
                return all(_validate_recursive(item, current_depth + 1) for item in obj)
            else:
                return True

        return _validate_recursive(data)

    def strip_control_characters(self, text: str) -> str:
        """
        Strip control characters that could be used for injection.

        Args:
            text: Text to sanitize

        Returns:
            Text with control characters removed
        """
        # Remove control characters except common whitespace
        # Control characters have ASCII values 0-31 and 127
        return ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')

    def validate_and_sanitize_input(self, user_input: Union[str, Dict[str, Any], List[Any]],
                                  input_type: str = "natural_language",
                                  max_length: int = 10000) -> Union[str, Dict[str, Any], List[Any]]:
        """
        Validate and sanitize user input based on its expected type.

        Args:
            user_input: User input to validate and sanitize
            input_type: Expected type of input ('natural_language', 'json', 'command', etc.)
            max_length: Maximum allowed length for strings

        Returns:
            Sanitized input
        """
        try:
            if isinstance(user_input, str):
                # Check for prompt injection attempts first
                if self.detect_prompt_injection(user_input):
                    self.logger.warning(f"Prompt injection attempt detected: {user_input[:100]}...")

                # Strip control characters and sanitize
                user_input = self.strip_control_characters(user_input)
                return self.sanitize_string(user_input, max_length)
            elif isinstance(user_input, dict):
                # Validate JSON structure and sanitize
                if not self.validate_json_structure(user_input):
                    raise ValueError("Invalid JSON structure")
                return self.sanitize_dict(user_input)
            elif isinstance(user_input, list):
                # Validate JSON structure and sanitize
                if not self.validate_json_structure(user_input):
                    raise ValueError("Invalid JSON structure")
                return self.sanitize_list(user_input)
            else:
                # For other types, convert to string and sanitize
                return self.sanitize_string(str(user_input), max_length)

        except Exception as e:
            self.logger.error(f"Error sanitizing input: {str(e)}")
            # Return a safe default in case of error
            if isinstance(user_input, str):
                return self.sanitize_string("")
            elif isinstance(user_input, dict):
                return {}
            elif isinstance(user_input, list):
                return []
            else:
                return self.sanitize_string("")

    def detect_prompt_injection(self, text: str) -> bool:
        """
        Detect potential prompt injection attempts in the input.

        Args:
            text: Text to check for prompt injection

        Returns:
            True if prompt injection is detected, False otherwise
        """
        result = self.detect_prompt_injection_with_details(text)
        return result is not None

    def detect_prompt_injection_with_details(self, text: str) -> Optional[str]:
        """
        Detect potential prompt injection attempts in the input and return the detected pattern.

        Args:
            text: Text to check for prompt injection

        Returns:
            Detected pattern if prompt injection is detected, None otherwise
        """
        if not text or not isinstance(text, str):
            return None

        text_lower = text.lower()

        # Check for common prompt injection patterns
        injection_patterns = [
            # Instruction manipulation
            r"ignore (the )?(above|previous) (instructions|commands?)",
            r"disregard (previous|earlier) (instructions|commands?)",
            r"forget all (prior|previous) (instructions|commands?)",
            r"you are now (an ai|a(?:n)? )?evil",
            r"your new role is",
            r"act as",
            r"pretend you are",
            r"roleplay as",

            # Format manipulation
            r"### instruction:",
            r"### response:",
            r"\[INST\]",
            r"\[/INST\]",
            r"<s>",
            r"</s>",

            # System role impersonation
            r"(?<!\w)system(?!\w):",
            r"(?<!\w)human(?!\w):",
            r"(?<!\w)assistant(?!\w):",
            r"(?<!\w)user(?!\w):",
            r"(?<!\w)model(?!\w):",

            # Escape sequences
            r"new output format:",
            r"from now on",
            r"change your behavior",
            r"bypass security",
            r"security vulnerability",
            r"exploit",
            r"hack",
            r"break character",
            r"jailbreak",

            # Direct commands to ignore safety
            r"do not (follow|obey|listen to) safety",
            r"disable (safety|filter)",
            r"ignore (moderation|rules|guidelines)",
            r"stop (filtering|monitoring)",
            r"without (refusing|warning|mentioning)",
            r"don't (tell|inform|warn) anyone",
        ]

        for pattern in injection_patterns:
            if re.search(pattern, text_lower):
                self.logger.warning(f"Prompt injection pattern detected: {pattern}")
                return pattern

        return None


# Global instance of the input sanitizer
input_sanitizer = InputSanitizer()