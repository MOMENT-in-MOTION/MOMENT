"""Exceptions for code generation and configuration."""


class CodeGeneratorError(Exception):
    """Base exception for code generation errors."""


class ConfigurationError(CodeGeneratorError):
    """Raised when API configuration is invalid or inconsistent."""
