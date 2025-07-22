#!/usr/bin/env python3
"""
Unit tests for the Vulcan module.
"""

import unittest
from unittest.mock import patch, MagicMock
import socket
from vulcan.vulcan import VulcanScanner


class TestVulcanScanner(unittest.TestCase):
    """Test cases for the VulcanScanner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scanner = VulcanScanner(target="localhost", port_range=(1, 100))

    def test_init(self):
        """Test scanner initialization."""
        self.assertEqual(self.scanner.target, "localhost")
        self.assertEqual(self.scanner.port_range, (1, 100))
        self.assertEqual(self.scanner.timeout, 1.0)
        self.assertFalse(self.scanner.verbose)
        self.assertEqual(self.scanner.results, {})

    @patch('socket.gethostbyname')
    def test_resolve_host_success(self, mock_gethostbyname):
        """Test successful hostname resolution."""
        mock_gethostbyname.return_value = "127.0.0.1"
        result = self.scanner.resolve_host("localhost")
        self.assertEqual(result, "127.0.0.1")
        mock_gethostbyname.assert_called_once_with("localhost")

    @patch('socket.gethostbyname')
    def test_resolve_host_failure(self, mock_gethostbyname):
        """Test failed hostname resolution."""
        mock_gethostbyname.side_effect = socket.gaierror("Name resolution error")
        result = self.scanner.resolve_host("nonexistent.domain")
        self.assertIsNone(result)

    @patch('socket.socket')
    def test_is_port_open_true(self, mock_socket):
        """Test port open detection."""
        # Configure the mock
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect_ex.return_value = 0
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        result = self.scanner.is_port_open(80)
        self.assertTrue(result)
        mock_socket_instance.connect_ex.assert_called_once_with(("localhost", 80))

    @patch('socket.socket')
    def test_is_port_open_false(self, mock_socket):
        """Test port closed detection."""
        # Configure the mock
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect_ex.return_value = 1
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        result = self.scanner.is_port_open(81)
        self.assertFalse(result)
        mock_socket_instance.connect_ex.assert_called_once_with(("localhost", 81))

    def test_is_ip_address(self):
        """Test IP address validation."""
        self.assertTrue(self.scanner._is_ip_address("127.0.0.1"))
        self.assertTrue(self.scanner._is_ip_address("192.168.1.1"))
        self.assertFalse(self.scanner._is_ip_address("localhost"))
        self.assertFalse(self.scanner._is_ip_address("not-an-ip"))

    @patch('vulcan.vulcan.VulcanScanner.scan_port_range')
    @patch('vulcan.vulcan.VulcanScanner.get_system_info')
    def test_run_security_checks(self, mock_get_system_info, mock_scan_port_range):
        """Test security checks execution."""
        mock_scan_port_range.return_value = {80: True, 443: True}
        mock_get_system_info.return_value = {"platform": "test"}
        
        results = self.scanner.run_security_checks()
        
        self.assertEqual(results["open_ports"], {80: True, 443: True})
        self.assertEqual(results["system_info"], {"platform": "test"})
        mock_scan_port_range.assert_called_once()
        mock_get_system_info.assert_called_once()


if __name__ == '__main__':
    unittest.main()