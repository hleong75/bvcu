#!/usr/bin/env python3
"""
Test script for BVCU Text-to-Speech Converter

This script tests all major functionality of the TTS program.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✓ TEST PASSED: {description}")
            return True
        else:
            print(f"✗ TEST FAILED: {description} (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ TEST FAILED: {description} (timeout)")
        return False
    except Exception as e:
        print(f"✗ TEST FAILED: {description} (error: {e})")
        return False


def main():
    """Run all tests"""
    print("BVCU Text-to-Speech Converter - Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Help message
    if run_command(
        ["python3", "text_to_speech.py", "-h"],
        "Display help message"
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 2: Simple French text to audio file
    output_file = "test_french.wav"
    if run_command(
        ["python3", "text_to_speech.py", 
         "-t", "Bonjour, ceci est un test de synthèse vocale",
         "-o", output_file],
        "French text to WAV file"
    ):
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"✓ Output file created: {output_file} ({size} bytes)")
            os.remove(output_file)
            tests_passed += 1
        else:
            print(f"✗ Output file not created: {output_file}")
            tests_failed += 1
    else:
        tests_failed += 1
    
    # Test 3: Read from file
    test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
    test_file.write("Ceci est un texte de test.\nIl contient plusieurs lignes.\nMerci!")
    test_file.close()
    
    output_file = "test_from_file.wav"
    if run_command(
        ["python3", "text_to_speech.py",
         "-f", test_file.name,
         "-o", output_file],
        "Read text from file"
    ):
        if os.path.exists(output_file):
            print(f"✓ Output file created from input file")
            os.remove(output_file)
            tests_passed += 1
        else:
            print(f"✗ Output file not created")
            tests_failed += 1
    else:
        tests_failed += 1
    
    os.remove(test_file.name)
    
    # Test 4: English text
    output_file = "test_english.wav"
    if run_command(
        ["python3", "text_to_speech.py",
         "-t", "This is an English test",
         "-l", "en",
         "-o", output_file],
        "English text synthesis"
    ):
        if os.path.exists(output_file):
            print(f"✓ English audio file created")
            os.remove(output_file)
            tests_passed += 1
        else:
            print(f"✗ Output file not created")
            tests_failed += 1
    else:
        tests_failed += 1
    
    # Test 5: Test with example.txt
    if os.path.exists("example.txt"):
        output_file = "test_example.wav"
        if run_command(
            ["python3", "text_to_speech.py",
             "-f", "example.txt",
             "-o", output_file],
            "Synthesize example.txt"
        ):
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"✓ Example file synthesized: {size} bytes")
                os.remove(output_file)
                tests_passed += 1
            else:
                print(f"✗ Output file not created")
                tests_failed += 1
        else:
            tests_failed += 1
    else:
        print("\n✗ example.txt not found, skipping test")
        tests_failed += 1
    
    # Test 6: Error handling - no input
    print(f"\n{'='*60}")
    print(f"TEST: Error handling - no input provided")
    print(f"{'='*60}")
    result = subprocess.run(
        ["python3", "text_to_speech.py"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("✓ Correctly rejected invalid input (no text or file)")
        tests_passed += 1
    else:
        print("✗ Should have failed with no input")
        tests_failed += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    print(f"Total tests: {tests_passed + tests_failed}")
    print(f"Success rate: {tests_passed / (tests_passed + tests_failed) * 100:.1f}%")
    print(f"{'='*60}")
    
    if tests_failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {tests_failed} TEST(S) FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
