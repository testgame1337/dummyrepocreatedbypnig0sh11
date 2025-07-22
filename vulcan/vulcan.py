#!/usr/bin/env python3
"""
Vulcan - A Python 3 tool for system analysis and security testing

This module provides functionality for scanning, analyzing, and testing systems
for security vulnerabilities and performance issues.
"""

import argparse
import concurrent.futures
import ipaddress
import json
import logging
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union


class VulcanScanner:
    """Main scanner class for Vulcan."""

    def __init__(self, target: str = None, port_range: Tuple[int, int] = (1, 1024),
                 timeout: float = 1.0, verbose: bool = False):
        """
        Initialize the Vulcan scanner.

        Args:
            target: Target IP address or hostname
            port_range: Tuple containing start and end port numbers
            timeout: Timeout for connection attempts in seconds
            verbose: Enable verbose output
        """
        self.target = target
        self.port_range = port_range
        self.timeout = timeout
        self.verbose = verbose
        self.results = {}
        
        # Configure logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("Vulcan")

    def resolve_host(self, hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address.

        Args:
            hostname: The hostname to resolve

        Returns:
            IP address as string or None if resolution fails
        """
        try:
            self.logger.debug(f"Resolving hostname: {hostname}")
            return socket.gethostbyname(hostname)
        except socket.gaierror as e:
            self.logger.error(f"Failed to resolve hostname {hostname}: {e}")
            return None

    def is_port_open(self, port: int) -> bool:
        """
        Check if a port is open on the target.

        Args:
            port: Port number to check

        Returns:
            True if port is open, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.target, port))
                is_open = result == 0
                if is_open and self.verbose:
                    self.logger.debug(f"Port {port} is open")
                return is_open
        except (socket.timeout, ConnectionRefusedError) as e:
            self.logger.debug(f"Error checking port {port}: {e}")
            return False

    def scan_port_range(self) -> Dict[int, bool]:
        """
        Scan a range of ports on the target.

        Returns:
            Dictionary mapping port numbers to boolean indicating if open
        """
        if not self.target:
            self.logger.error("No target specified for port scanning")
            return {}

        self.logger.info(f"Starting port scan on {self.target} "
                         f"(ports {self.port_range[0]}-{self.port_range[1]})")
        start_time = time.time()
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            port_futures = {
                executor.submit(self.is_port_open, port): port
                for port in range(self.port_range[0], self.port_range[1] + 1)
            }
            
            for future in concurrent.futures.as_completed(port_futures):
                port = port_futures[future]
                try:
                    is_open = future.result()
                    if is_open:
                        results[port] = True
                except Exception as e:
                    self.logger.error(f"Error scanning port {port}: {e}")
        
        scan_time = time.time() - start_time
        self.logger.info(f"Port scan completed in {scan_time:.2f} seconds")
        self.logger.info(f"Found {len(results)} open ports")
        
        return results

    def get_system_info(self) -> Dict[str, str]:
        """
        Get information about the current system.

        Returns:
            Dictionary containing system information
        """
        self.logger.info("Gathering system information")
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "python_version": sys.version,
        }
        return info

    def run_security_checks(self) -> Dict[str, Dict]:
        """
        Run basic security checks on the target system.

        Returns:
            Dictionary containing security check results
        """
        self.logger.info("Running security checks")
        results = {
            "open_ports": self.scan_port_range(),
            "system_info": self.get_system_info() if self.target == "localhost" else {},
        }
        return results

    def save_results(self, filename: str) -> None:
        """
        Save scan results to a JSON file.

        Args:
            filename: Name of the file to save results to
        """
        if not self.results:
            self.logger.warning("No results to save")
            return
            
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=4)
            self.logger.info(f"Results saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")

    def run(self) -> Dict:
        """
        Run the Vulcan scanner with configured settings.

        Returns:
            Dictionary containing all scan results
        """
        self.logger.info(f"Starting Vulcan scan on {self.target}")
        start_time = datetime.now()
        
        # Resolve hostname if needed
        if self.target and not self._is_ip_address(self.target):
            resolved_ip = self.resolve_host(self.target)
            if resolved_ip:
                self.logger.info(f"Resolved {self.target} to {resolved_ip}")
                self.target = resolved_ip
            else:
                self.logger.error(f"Could not resolve hostname: {self.target}")
                return {}
        
        # Run security checks
        security_results = self.run_security_checks()
        
        # Compile results
        self.results = {
            "scan_info": {
                "target": self.target,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
            },
            "security": security_results,
        }
        
        self.logger.info("Scan completed")
        return self.results

    def _is_ip_address(self, addr: str) -> bool:
        """
        Check if a string is a valid IP address.

        Args:
            addr: String to check

        Returns:
            True if string is a valid IP address, False otherwise
        """
        try:
            ipaddress.ip_address(addr)
            return True
        except ValueError:
            return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Vulcan - A Python 3 tool for system analysis and security testing"
    )
    parser.add_argument(
        "-t", "--target", 
        help="Target IP address or hostname (use 'localhost' for local system)"
    )
    parser.add_argument(
        "-p", "--ports", 
        help="Port range to scan (format: start-end)", 
        default="1-1024"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file for scan results"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose output"
    )
    parser.add_argument(
        "--timeout", 
        type=float, 
        default=1.0, 
        help="Timeout for connection attempts in seconds"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for Vulcan."""
    args = parse_arguments()
    
    # Parse port range
    try:
        start_port, end_port = map(int, args.ports.split('-'))
        port_range = (start_port, end_port)
    except ValueError:
        print(f"Invalid port range: {args.ports}. Format should be start-end.")
        sys.exit(1)
    
    # Create and run scanner
    scanner = VulcanScanner(
        target=args.target,
        port_range=port_range,
        timeout=args.timeout,
        verbose=args.verbose
    )
    
    results = scanner.run()
    
    # Save results if output file specified
    if args.output:
        scanner.save_results(args.output)
    else:
        # Print summary to console
        print("\nScan Results Summary:")
        print(f"Target: {args.target}")
        
        if "security" in results and "open_ports" in results["security"]:
            open_ports = results["security"]["open_ports"]
            print(f"Open ports: {', '.join(map(str, open_ports.keys())) if open_ports else 'None'}")
        
        print("\nUse --output to save detailed results to a file")


if __name__ == "__main__":
    main()