#!/usr/bin/env python3
"""
Test Runner for JSON-RPC Project

This script provides a comprehensive test runner with different test categories
and quality checks. It ensures that all tests pass and code quality standards
are met before allowing changes to be committed.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --quick            # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --coverage         # Run tests with detailed coverage
    python run_tests.py --quality          # Run code quality checks only
    python run_tests.py --all              # Run everything (tests + quality)
"""

import argparse
import subprocess
import sys
import os
import time
from pathlib import Path


class TestRunner:
    """Comprehensive test runner for the JSON-RPC project."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.failed_checks = []

    def run_command(self, command, description, check_return_code=True):
        """Run a command and handle output."""
        print(f"\n{'='*60}")
        print(f"🔍 {description}")
        print(f"{'='*60}")
        print(f"Command: {' '.join(command)}")
        print("-" * 60)

        start_time = time.time()
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=False,
                text=True,
                check=check_return_code,
            )
            elapsed = time.time() - start_time

            if result.returncode == 0:
                print(f"\n✅ {description} - PASSED ({elapsed:.2f}s)")
                return True
            else:
                print(f"\n❌ {description} - FAILED ({elapsed:.2f}s)")
                self.failed_checks.append(description)
                return False

        except subprocess.CalledProcessError as e:
            elapsed = time.time() - start_time
            print(f"\n❌ {description} - FAILED ({elapsed:.2f}s)")
            print(f"Error: {e}")
            self.failed_checks.append(description)
            return False
        except FileNotFoundError:
            print(f"\n⚠️  Command not found: {command[0]}")
            print(
                "Make sure all dependencies are installed with: uv sync --group test --group dev"
            )
            self.failed_checks.append(description)
            return False

    def install_dependencies(self):
        """Install test and dev dependencies."""
        print("📦 Installing dependencies...")
        commands = [
            (
                ["uv", "sync", "--group", "test", "--group", "dev"],
                "Installing test and dev dependencies",
            ),
        ]

        for command, description in commands:
            if not self.run_command(command, description):
                return False
        return True

    def run_unit_tests(self):
        """Run unit tests only."""
        return self.run_command(
            ["uv", "run", "pytest", "tests/", "-m", "not integration", "-v"], "Running Unit Tests"
        )

    def run_integration_tests(self):
        """Run integration tests only."""
        return self.run_command(
            ["uv", "run", "pytest", "tests/", "-m", "integration", "-v"],
            "Running Integration Tests",
        )

    def run_all_tests(self):
        """Run all tests."""
        return self.run_command(["uv", "run", "pytest", "tests/", "-v"], "Running All Tests")

    def run_tests_with_coverage(self):
        """Run tests with coverage analysis."""
        success = self.run_command(
            [
                "uv",
                "run",
                "pytest",
                "tests/",
                "--cov=src/jsonrpc_playground",
                "--cov-report=term-missing",
                "--cov-report=html",
                "-v",
            ],
            "Running Tests with Coverage Analysis",
        )

        if success:
            print("\n📊 Coverage report generated in 'htmlcov' directory")
            coverage_file = self.project_root / "htmlcov" / "index.html"
            if coverage_file.exists():
                print(
                    f"📄 Open {coverage_file} in your browser to view detailed coverage"
                )

        return success

    def run_code_quality_checks(self):
        """Run code quality and linting checks."""
        checks = [
            (["uv", "run", "black", "--check", "src/", "tests/"], "Code Formatting Check (Black)"),
            (
                ["uv", "run", "isort", "--check-only", "src/", "tests/"],
                "Import Sorting Check (isort)",
            ),
            (["uv", "run", "flake8", "src/", "tests/"], "Code Style Check (Flake8)"),
            (["uv", "run", "pylint", "src/jsonrpc_playground/"], "Code Quality Check (Pylint)"),
        ]

        all_passed = True
        for command, description in checks:
            if not self.run_command(command, description, check_return_code=False):
                all_passed = False

        return all_passed

    def run_syntax_check(self):
        """Run Python syntax compilation check."""
        python_files = []
        # Check source files
        src_files = list((self.project_root / "src").glob("**/*.py"))
        test_files = list((self.project_root / "tests").glob("**/*.py"))
        python_files.extend(src_files)
        python_files.extend(test_files)
        
        if not python_files:
            print("⚠️  No Python files found")
            return True

        file_args = [str(f) for f in python_files]
        return self.run_command(
            ["python", "-m", "py_compile"] + file_args,
            "Python Syntax Compilation Check",
        )

    def run_security_check(self):
        """Run security vulnerability check."""
        # This is optional and will be skipped if bandit is not available
        return self.run_command(
            [
                "uv",
                "run",
                "python",
                "-c",
                "print('Security check placeholder - install bandit for real security scanning')",
            ],
            "Security Check (placeholder)",
            check_return_code=False,
        )

    def check_test_files_exist(self):
        """Verify that test files exist and are properly structured."""
        required_test_files = [
            "tests/test_server.py",
            "tests/test_client.py", 
            "tests/test_main.py",
        ]

        missing_files = []
        for test_file in required_test_files:
            if not (self.project_root / test_file).exists():
                missing_files.append(test_file)

        if missing_files:
            print(f"❌ Missing test files: {', '.join(missing_files)}")
            self.failed_checks.append("Test File Existence Check")
            return False
        else:
            print("✅ All required test files exist")
            return True

    def print_summary(self):
        """Print test run summary."""
        print("\n" + "=" * 80)
        print("📋 TEST RUN SUMMARY")
        print("=" * 80)

        if not self.failed_checks:
            print("🎉 ALL CHECKS PASSED!")
            print("✨ Your code is ready for submission/deployment.")
            return True
        else:
            print(f"❌ {len(self.failed_checks)} CHECK(S) FAILED:")
            for i, check in enumerate(self.failed_checks, 1):
                print(f"   {i}. {check}")

            print("\n💡 TO FIX ISSUES:")
            print("   • Run 'uv run black .' to fix formatting")
            print("   • Run 'uv run isort .' to fix import sorting")
            print("   • Check the output above for specific error details")
            print(
                "   • Make sure all dependencies are installed: 'uv sync --group test --group dev'"
            )
            return False


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Comprehensive test runner for JSON-RPC project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                 # Run all tests
  python run_tests.py --quick         # Quick unit tests only
  python run_tests.py --integration   # Integration tests only  
  python run_tests.py --coverage      # Tests with coverage
  python run_tests.py --quality       # Code quality checks only
  python run_tests.py --all           # Everything (tests + quality)
  python run_tests.py --install-deps  # Install dependencies only
        """,
    )

    parser.add_argument(
        "--quick", action="store_true", help="Run only unit tests (fast)"
    )
    parser.add_argument(
        "--integration", action="store_true", help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage analysis"
    )
    parser.add_argument(
        "--quality", action="store_true", help="Run code quality checks only"
    )
    parser.add_argument(
        "--all", action="store_true", help="Run all tests and quality checks"
    )
    parser.add_argument(
        "--install-deps", action="store_true", help="Install dependencies only"
    )
    parser.add_argument(
        "--no-install", action="store_true", help="Skip dependency installation"
    )

    args = parser.parse_args()

    runner = TestRunner()

    print("🚀 JSON-RPC Project Test Runner")
    print(f"📁 Project: {runner.project_root}")

    # Install dependencies unless explicitly skipped
    if args.install_deps:
        success = runner.install_dependencies()
        return 0 if success else 1

    if not args.no_install:
        print("\n📦 Checking dependencies...")
        if not runner.install_dependencies():
            print("❌ Failed to install dependencies")
            return 1

    # Check test files exist
    if not runner.check_test_files_exist():
        return 1

    # Run syntax check first
    if not runner.run_syntax_check():
        print("❌ Syntax errors found. Fix them before running tests.")
        return 1

    # Determine what to run based on arguments
    success = True

    if args.quality:
        success = runner.run_code_quality_checks()
    elif args.quick:
        success = runner.run_unit_tests()
    elif args.integration:
        success = runner.run_integration_tests()
    elif args.coverage:
        success = runner.run_tests_with_coverage()
    elif args.all:
        success = runner.run_all_tests() and runner.run_code_quality_checks()
    else:
        # Default: run all tests
        success = runner.run_all_tests()

    # Print summary
    overall_success = success and runner.print_summary()

    if overall_success:
        print("\n🎯 All checks completed successfully!")
        return 0
    else:
        print("\n💥 Some checks failed. Please review and fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
