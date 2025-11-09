#!/usr/bin/env python3
"""
Test script specifically for BVCU file loading functionality

Note: These tests verify that BVCU files are correctly detected and loaded
into memory. However, the actual TTS synthesis uses pyttsx3/eSpeak and cannot
use BVCU data (proprietary format requiring Nuance Vocalizer SDK).
"""

import os
import sys
import tempfile
from pathlib import Path
from text_to_speech import BVCUTextToSpeech


def test_no_bvcu_files():
    """Test when no BVCU files are present"""
    print("\n" + "=" * 60)
    print("TEST 1: No BVCU files present")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        assert len(tts.voice_files) == 0, "Should find no voice files"
        assert tts.bvcu_data['voice_data'] is None, "Should have no voice data"
        assert tts.bvcu_data['dictionary'] is None, "Should have no dictionary"
        assert tts.bvcu_data['linguistic'] is None, "Should have no linguistic data"
        
        print("✓ TEST PASSED: Correctly handles absence of BVCU files")
        return True


def test_with_bvcu_files():
    """Test when BVCU files are present"""
    print("\n" + "=" * 60)
    print("TEST 2: BVCU files present")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create sample BVCU files
        (tmpdir_path / 'frf.bnx').write_bytes(b'BVCU voice data sample')
        (tmpdir_path / 'frf.dca').write_bytes(b'BVCU dictionary')
        (tmpdir_path / 'frf.ldi').write_bytes(b'BVCU linguistic')
        (tmpdir_path / 'frf.oso').write_bytes(b'BVCU orthographic')
        (tmpdir_path / 'frf.trz').write_bytes(b'BVCU transcription')
        (tmpdir_path / 'user.userdico').write_text('test=test', encoding='utf-8')
        
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Verify files were detected
        assert len(tts.voice_files) == 6, f"Should find 6 voice files, found {len(tts.voice_files)}"
        
        # Verify data was loaded
        assert tts.bvcu_data['voice_data'] is not None, "Should have voice data"
        assert len(tts.bvcu_data['voice_data']) > 0, "Voice data should be loaded"
        
        assert tts.bvcu_data['dictionary'] is not None, "Should have dictionary"
        assert len(tts.bvcu_data['dictionary']) > 0, "Dictionary should be loaded"
        
        assert tts.bvcu_data['linguistic'] is not None, "Should have linguistic data"
        assert len(tts.bvcu_data['linguistic']) > 0, "Linguistic data should be loaded"
        
        assert 'user_dictionary' in tts.bvcu_data['configuration'], "Should have user dictionary"
        assert tts.bvcu_data['configuration']['user_dictionary'] == 'test=test', "User dict content mismatch"
        
        assert 'frf.oso' in tts.bvcu_data['configuration'], "Should have orthographic config"
        assert 'frf.trz' in tts.bvcu_data['configuration'], "Should have transcription config"
        
        print("✓ TEST PASSED: Correctly loads BVCU files (detection only)")
        return True


def test_hd_voice_priority():
    """Test that HD voice data takes priority over standard voice data"""
    print("\n" + "=" * 60)
    print("TEST 3: HD voice data priority")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create both standard and HD voice files
        (tmpdir_path / 'frf.bnx').write_bytes(b'Standard voice')
        (tmpdir_path / 'frf_hd.bnx').write_bytes(b'High definition voice data')
        
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Verify HD voice data was used (it's larger)
        assert tts.bvcu_data['voice_data'] is not None, "Should have voice data"
        assert len(tts.bvcu_data['voice_data']) == 26, "Should use HD voice data (26 bytes)"
        
        print("✓ TEST PASSED: HD voice data takes priority")
        return True


def test_multiple_dictionaries():
    """Test that multiple dictionary files are combined"""
    print("\n" + "=" * 60)
    print("TEST 4: Multiple dictionary files")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create multiple dictionary files
        (tmpdir_path / 'frf.dca').write_bytes(b'Dict1')
        (tmpdir_path / 'frf_accent_restoration.dca').write_bytes(b'Dict2')
        
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Verify dictionaries were combined
        assert tts.bvcu_data['dictionary'] is not None, "Should have dictionary"
        assert len(tts.bvcu_data['dictionary']) == 10, "Should combine both dictionaries (10 bytes)"
        
        print("✓ TEST PASSED: Multiple dictionaries combined correctly")
        return True


def test_bvcu_file_extension():
    """Test that .bvcu files are detected and loaded"""
    print("\n" + "=" * 60)
    print("TEST 5: .bvcu file extension support")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create .bvcu files
        (tmpdir_path / 'frf.bvcu').write_bytes(b'BVCU voice data in .bvcu format')
        
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Verify .bvcu file was detected
        assert 'frf.bvcu' in tts.voice_files, "Should detect frf.bvcu file"
        assert len(tts.voice_files) == 1, f"Should find 1 voice file, found {len(tts.voice_files)}"
        
        # Verify .bvcu data was loaded
        assert tts.bvcu_data['voice_data'] is not None, "Should have voice data"
        assert len(tts.bvcu_data['voice_data']) == 31, "Voice data should be 31 bytes"
        
        print("✓ TEST PASSED: .bvcu files are properly detected and loaded")
        return True


def test_bvcu_hd_priority():
    """Test that HD .bvcu files take priority over standard .bvcu files"""
    print("\n" + "=" * 60)
    print("TEST 6: HD .bvcu file priority")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create both standard and HD .bvcu files
        (tmpdir_path / 'frf.bvcu').write_bytes(b'Standard BVCU')
        (tmpdir_path / 'frf_hd.bvcu').write_bytes(b'High definition BVCU voice data')
        
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Verify HD .bvcu was used (it's larger)
        assert tts.bvcu_data['voice_data'] is not None, "Should have voice data"
        assert len(tts.bvcu_data['voice_data']) == 31, "Should use HD .bvcu data (31 bytes)"
        
        print("✓ TEST PASSED: HD .bvcu files take priority")
        return True


def test_bvcu_and_bnx_coexistence():
    """Test that .bvcu and .bnx files can coexist, with larger file taking priority"""
    print("\n" + "=" * 60)
    print("TEST 7: .bvcu and .bnx coexistence")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create both .bvcu (smaller) and .bnx (larger) files
        (tmpdir_path / 'frf.bvcu').write_bytes(b'Small BVCU')
        (tmpdir_path / 'frf.bnx').write_bytes(b'Larger BNX voice data file')
        
        tts = BVCUTextToSpeech(tmpdir, 'fr')
        
        # Verify both were detected
        assert 'frf.bvcu' in tts.voice_files, "Should detect frf.bvcu"
        assert 'frf.bnx' in tts.voice_files, "Should detect frf.bnx"
        
        # Verify larger .bnx was used
        assert tts.bvcu_data['voice_data'] is not None, "Should have voice data"
        assert len(tts.bvcu_data['voice_data']) == 26, "Should use larger .bnx data (26 bytes)"
        
        print("✓ TEST PASSED: .bvcu and .bnx files coexist properly")
        return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("BVCU File Loading Test Suite")
    print("=" * 60)
    
    tests = [
        test_no_bvcu_files,
        test_with_bvcu_files,
        test_hd_voice_priority,
        test_multiple_dictionaries,
        test_bvcu_file_extension,
        test_bvcu_hd_priority,
        test_bvcu_and_bnx_coexistence,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ TEST FAILED: {test_func.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"Success rate: {passed / (passed + failed) * 100:.1f}%")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
