"""
Basic tests for NeuroEML email parser
"""
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_import_parser():
    """Test that the email parser module imports correctly"""
    from parsers.email_parser import EmailParser
    assert EmailParser is not None


def test_parser_initialization():
    """Test parser can be instantiated"""
    from parsers.email_parser import EmailParser
    parser = EmailParser()
    assert parser is not None


def test_import_analyzer():
    """Test that the main analyzer module imports correctly"""
    from models.analyzer import NeuroEMLAnalyzer
    assert NeuroEMLAnalyzer is not None
