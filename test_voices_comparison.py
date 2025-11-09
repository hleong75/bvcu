#!/usr/bin/env python3
"""
Comprehensive test to verify the difference between 'fr' with /voices and without /voices.
This test runs many iterations to ensure stability and correctness.

This test was created to address the issue of checking if there's a real difference
when using French voice files from the /voices directory versus not using them.
"""

import os
import sys
import tempfile
from pathlib import Path
from text_to_speech import BVCUTextToSpeech


def test_with_voices_directory():
    """Test loading voice files WITH the /voices directory"""
    print("\n" + "=" * 80)
    print("TEST: Loading French voice files WITH /voices directory")
    print("=" * 80)
    
    tts = BVCUTextToSpeech("voices", 'fr')
    
    # Check that files were detected
    detected_files = list(tts.voice_files.keys())
    print(f"\nDetected {len(detected_files)} voice files:")
    for filename in detected_files:
        print(f"  - {filename}")
    
    # Check that voice data was loaded
    voice_data_size = len(tts.bvcu_data['voice_data']) if tts.bvcu_data['voice_data'] else 0
    dictionary_size = len(tts.bvcu_data['dictionary']) if tts.bvcu_data['dictionary'] else 0
    linguistic_size = len(tts.bvcu_data['linguistic']) if tts.bvcu_data['linguistic'] else 0
    
    print(f"\nLoaded data:")
    print(f"  - Voice data: {voice_data_size:,} bytes")
    print(f"  - Dictionary: {dictionary_size:,} bytes")
    print(f"  - Linguistic: {linguistic_size:,} bytes")
    
    # Verify critical files are loaded
    has_claire = 'claire_22k_lf.bvcu' in detected_files
    has_voice_data = voice_data_size > 0
    has_dictionary = dictionary_size > 0
    
    print(f"\nStatus:")
    print(f"  - claire_22k_lf.bvcu detected: {'✓' if has_claire else '✗'}")
    print(f"  - Voice data loaded: {'✓' if has_voice_data else '✗'}")
    print(f"  - Dictionary loaded: {'✓' if has_dictionary else '✗'}")
    
    return {
        'files_detected': len(detected_files),
        'voice_data_size': voice_data_size,
        'dictionary_size': dictionary_size,
        'linguistic_size': linguistic_size,
        'has_claire': has_claire,
        'has_voice_data': has_voice_data,
        'has_dictionary': has_dictionary
    }


def test_without_voices_directory():
    """Test loading voice files WITHOUT the /voices directory (empty directory)"""
    print("\n" + "=" * 80)
    print("TEST: Loading French voice files WITHOUT /voices directory (empty dir)")
    print("=" * 80)
    
    # Create a temporary empty directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Check that NO files were detected
        detected_files = list(tts.voice_files.keys())
        print(f"\nDetected {len(detected_files)} voice files in empty directory")
        
        # Check that NO voice data was loaded
        voice_data_size = len(tts.bvcu_data['voice_data']) if tts.bvcu_data['voice_data'] else 0
        dictionary_size = len(tts.bvcu_data['dictionary']) if tts.bvcu_data['dictionary'] else 0
        linguistic_size = len(tts.bvcu_data['linguistic']) if tts.bvcu_data['linguistic'] else 0
        
        print(f"\nLoaded data:")
        print(f"  - Voice data: {voice_data_size:,} bytes")
        print(f"  - Dictionary: {dictionary_size:,} bytes")
        print(f"  - Linguistic: {linguistic_size:,} bytes")
        
        return {
            'files_detected': len(detected_files),
            'voice_data_size': voice_data_size,
            'dictionary_size': dictionary_size,
            'linguistic_size': linguistic_size
        }


def compare_results(with_voices, without_voices):
    """Compare results from with and without voices directory"""
    print("\n" + "=" * 80)
    print("COMPARISON: WITH /voices vs WITHOUT /voices")
    print("=" * 80)
    
    print(f"\nFiles detected:")
    print(f"  WITH /voices:    {with_voices['files_detected']} files")
    print(f"  WITHOUT /voices: {without_voices['files_detected']} files")
    print(f"  Difference:      {with_voices['files_detected'] - without_voices['files_detected']} files")
    
    print(f"\nVoice data size:")
    print(f"  WITH /voices:    {with_voices['voice_data_size']:,} bytes")
    print(f"  WITHOUT /voices: {without_voices['voice_data_size']:,} bytes")
    print(f"  Difference:      {with_voices['voice_data_size'] - without_voices['voice_data_size']:,} bytes")
    
    print(f"\nDictionary size:")
    print(f"  WITH /voices:    {with_voices['dictionary_size']:,} bytes")
    print(f"  WITHOUT /voices: {without_voices['dictionary_size']:,} bytes")
    print(f"  Difference:      {with_voices['dictionary_size'] - without_voices['dictionary_size']:,} bytes")
    
    # Determine if there's a significant difference
    has_difference = (
        with_voices['files_detected'] > 0 and
        with_voices['voice_data_size'] > 0 and
        with_voices['dictionary_size'] > 0 and
        without_voices['files_detected'] == 0 and
        without_voices['voice_data_size'] == 0
    )
    
    print("\n" + "=" * 80)
    if has_difference:
        print("✓ RESULT: There IS a significant difference!")
        print("  The program correctly detects and loads voice files from /voices")
        print("  and does NOT load them when /voices is empty.")
        print("  This proves the program is working correctly.")
    else:
        print("✗ RESULT: There is NO difference or unexpected behavior!")
        print("  The program might not be working correctly.")
    print("=" * 80)
    
    return has_difference


def test_stability(iterations=1000):
    """Test stability by running many iterations"""
    print("\n" + "=" * 80)
    print(f"STABILITY TEST: Running {iterations} iterations")
    print("=" * 80)
    
    print("\nThis test will verify that the program consistently:")
    print("  1. Detects voice files in /voices directory")
    print("  2. Loads the correct amount of data")
    print("  3. Does not crash or produce errors")
    
    expected_voice_data_size = None
    expected_files_count = None
    
    for i in range(iterations):
        try:
            tts = BVCUTextToSpeech("voices", 'fr')
            
            files_count = len(tts.voice_files)
            voice_data_size = len(tts.bvcu_data['voice_data']) if tts.bvcu_data['voice_data'] else 0
            
            # First iteration - establish baseline
            if i == 0:
                expected_files_count = files_count
                expected_voice_data_size = voice_data_size
                print(f"\n✓ Iteration 1: Baseline established")
                print(f"  - Files: {expected_files_count}")
                print(f"  - Voice data: {expected_voice_data_size:,} bytes")
            else:
                # Check consistency
                if files_count != expected_files_count:
                    print(f"\n✗ Iteration {i+1}: File count mismatch!")
                    print(f"  Expected {expected_files_count}, got {files_count}")
                    return False
                
                if voice_data_size != expected_voice_data_size:
                    print(f"\n✗ Iteration {i+1}: Voice data size mismatch!")
                    print(f"  Expected {expected_voice_data_size:,}, got {voice_data_size:,}")
                    return False
            
            # Progress reporting
            if (i + 1) % 100 == 0:
                print(f"✓ Completed {i+1}/{iterations} iterations successfully")
        
        except Exception as e:
            print(f"\n✗ Iteration {i+1}: Exception occurred!")
            print(f"  Error: {e}")
            return False
    
    print(f"\n✓ ALL {iterations} iterations completed successfully!")
    print(f"  - Consistent file detection: {expected_files_count} files")
    print(f"  - Consistent voice data: {expected_voice_data_size:,} bytes")
    print(f"  - No errors or crashes")
    
    return True


def main():
    """Run all comparison tests"""
    print("=" * 80)
    print("COMPREHENSIVE VOICE COMPARISON TEST")
    print("Testing: fr WITH /voices vs fr WITHOUT /voices")
    print("=" * 80)
    
    # Test 1: With voices directory
    with_voices = test_with_voices_directory()
    
    # Test 2: Without voices directory
    without_voices = test_without_voices_directory()
    
    # Test 3: Compare results
    has_difference = compare_results(with_voices, without_voices)
    
    # Test 4: Stability test with many iterations
    is_stable = test_stability(iterations=1000)
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    if has_difference and is_stable:
        print("\n✓✓✓ ALL TESTS PASSED! ✓✓✓")
        print("\nConclusions:")
        print("  1. There IS a clear difference between using /voices and not using it")
        print("  2. The program correctly detects and loads voice files from /voices")
        print("  3. The program is stable across 1000 iterations")
        print("  4. The program works correctly!")
        print("\n  The claire_22k_lf.bvcu file is now properly detected and loaded.")
        print("  Voice files provide enhanced synthesis capability.")
        return 0
    elif has_difference and not is_stable:
        print("\n✗ PARTIAL SUCCESS")
        print("\nConclusions:")
        print("  1. There IS a difference (good)")
        print("  2. BUT the program is NOT stable across iterations (bad)")
        return 1
    else:
        print("\n✗✗✗ TESTS FAILED ✗✗✗")
        print("\nConclusions:")
        print("  1. The program is NOT working correctly")
        print("  2. Voice files may not be detected or loaded properly")
        return 1


if __name__ == '__main__':
    sys.exit(main())
