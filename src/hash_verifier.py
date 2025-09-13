#!/usr/bin/env python3
"""
Hash Verification Engine for PASS // FAIL

This file contains the core logic for checking if hashes match common passwords.

How it works:
1. Takes a hash (encrypted password) as input
2. Tries different hash algorithms based on the hash length
3. Checks each word in the selected wordlists b                # Skip remaining wordlists for this algorithm if we found all hashes in this length group
                if found_in_group[hash_length] == len(hashes_in_group):
                    send_status_message(
                        "",
                        False,
                        "#0f0",
                        [
                            ("✅ Found all ", "#0f0"),
                            (str(len(hashes_in_group)), "#fff"),
                            (" hashes for ", "#0f0"),
                            (f"{hash_length}-char", "#ff0"),
                            (" length using ", "#0f0"),
                            (algorithm, "#0ff"),
                        ]
                    )
                    breakshing it
4. If the hashed word matches the input hash, we found the password!

Performance Optimizations:
- Early termination when ALL hashes in a list are found
- O(1) hash lookup using sets instead of O(n) list searches
- Cached hasher objects to avoid repeated object creation
- Duplicate password detection to skip already-tested combinations
- Smart algorithm ordering (most common first: MD5, SHA1, SHA256)
- Efficient file I/O with single-pass reading
- Per-algorithm group completion detection

This helps people understand if their passwords are too common and easily guessable.
"""

# Import the modules we need
import os
import hashlib
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Callable, Any

# This dictionary maps hash lengths to the algorithms that produce them
# For example: MD5 hashes are always 32 characters long
# Ordered by likelihood/popularity for better performance
HASH_ALGORITHMS_BY_LENGTH = {
    32:  ["md5", "md4", "md2"],                    # 128-bit hashes (32 hex chars) - MD5 most common
    40:  ["sha1", "ripemd160"],                    # 160-bit hashes (40 hex chars) - SHA1 most common
    56:  ["sha224"],                               # 224-bit hashes (56 hex chars)
    64:  ["sha256", "blake2s", "sm3"],             # 256-bit hashes (64 hex chars) - SHA256 most common
    96:  ["sha384"],                               # 384-bit hashes (96 hex chars)
    128: ["sha512", "blake2b", "whirlpool"]        # 512-bit hashes (128 hex chars) - SHA512 most common
}

# Find the wordlists folder (should be in the same directory as this file)
WORDLISTS_FOLDER = os.path.join(os.path.dirname(__file__), "wordlists")


def get_available_wordlists():
    """
    Finds all the wordlist files (.txt files) in the wordlists folder.
    
    Returns:
        list: Names of all .txt files found in the wordlists folder
    """
    # Check if the wordlists folder exists
    if not os.path.isdir(WORDLISTS_FOLDER):
        return []
    
    # Get all .txt files from the folder
    txt_files = []
    for filename in os.listdir(WORDLISTS_FOLDER):
        if filename.endswith(".txt"):
            txt_files.append(filename)
    
    return txt_files


def create_hash(word, hasher):
    """
    Creates a hash of a word using a pre-configured hasher object (for efficiency).
    
    Args:
        word (str): The word to hash (like "password123")
        hasher (hashlib object): Pre-configured hash object
    
    Returns:
        str: The hash as a string of hexadecimal characters
    """
    # Reset the hasher and update with the word
    hasher_copy = hasher.copy()
    hasher_copy.update(word.encode("utf-8"))
    return hasher_copy.hexdigest()


def verify_hash(hash_to_check, wordlist_names, gui_callback=None, progress_callback=None, stop_event=None):
    """
    The main function that tries to find what password created a given hash.
    
    Args:
        hash_to_check (str): The hash to verify, or path to a file with hashes
        wordlist_names (list): List of wordlist filenames to check against
        gui_callback (function, optional): Function to send status updates to the GUI
        progress_callback (function, optional): Function to update the progress bar
        stop_event (object, optional): Used to stop the verification early if needed
    
    Returns:
        tuple: (success, results_dictionary)
               success = True if any passwords were found
               results_dictionary = maps hashes to (password, algorithm) pairs
    """
    # Dictionary to store any passwords we find
    found_passwords = {}
    was_stopped_early = False

    def send_status_message(message, replace_last_line=False, text_color="#fff", colored_segments=None):
        """Helper function to send status updates to the GUI or console"""
        if gui_callback:
            try:
                gui_callback(message, replace_last_line, text_color, colored_segments)
            except TypeError:
                # Fallback if the GUI function expects fewer parameters
                gui_callback(message, replace_last_line)
        else:
            # If no GUI, just print to console
            if replace_last_line:
                print(f"\r{message}", end="", flush=True)
            else:
                print(message)

    # Check if the input is a file path or a single hash
    if isinstance(hash_to_check, str) and hash_to_check.endswith('.txt'):
        # It's a file - read all hashes from it
        try:
            with open(hash_to_check, "r") as file:
                hash_list = [line.strip() for line in file if line.strip()]
            send_status_message(f"Loaded {len(hash_list)} hashes from file: {hash_to_check}")
        except FileNotFoundError:
            send_status_message(f"Error: Could not find file: {hash_to_check}")
            return None
    else:
        # It's a single hash
        hash_list = [hash_to_check]

    # Convert all hashes to lowercase for consistent comparison and use sets for O(1) lookup
    hash_list = [hash_value.lower() for hash_value in hash_list]

    # Group hashes by their length (different lengths need different algorithms)
    # Use sets for O(1) lookup performance instead of lists
    hashes_by_length = defaultdict(set)
    for hash_value in hash_list:
        length = len(hash_value)
        hashes_by_length[length].add(hash_value)

    # Keep track of passwords we've already tested to avoid duplicates
    tested_passwords = set()
    
    # Track how many hashes we've found for each length group
    found_in_group = defaultdict(int)

    # Process each group of hashes (by length)
    for hash_length, hashes_in_group in hashes_by_length.items():
        
        # Check if we know what algorithms can produce this hash length
        if hash_length not in HASH_ALGORITHMS_BY_LENGTH:
            send_status_message(f"Unknown hash length: {hash_length} characters (hash: {hashes_in_group[0]})")
            continue

        # Get the possible algorithms for this hash length
        possible_algorithms = HASH_ALGORITHMS_BY_LENGTH[hash_length]
        send_status_message(
            "",
            False,
            "#fff",
            [
                (f"Testing {hash_length}-character hashes with algorithms: ", "#fff"),
                (", ".join(possible_algorithms), "#0ff"),
            ]
        )

        # Try each possible algorithm
        for algorithm in possible_algorithms:
            
            # Check if we should stop early
            if stop_event is not None and getattr(stop_event, "is_set", lambda: False)():
                was_stopped_early = True
                break
                
            # Check if this algorithm is available on this computer
            if algorithm not in hashlib.algorithms_available:
                send_status_message(
                    "",
                    False,
                    "#f00",
                    [
                        ("Algorithm ", "#f00"),
                        (algorithm, "#0ff"),
                        (" is not available on this system.", "#f00"),
                    ]
                )
                continue

            # Create hasher object once for efficiency (instead of creating new ones for each password)
            try:
                hasher = hashlib.new(algorithm)
            except Exception as e:
                send_status_message(
                    "",
                    False,
                    "#f00",
                    [
                        ("Failed to initialize ", "#f00"),
                        (algorithm, "#0ff"),
                        (" hasher: ", "#f00"),
                        (str(e), "#f00"),
                    ]
                )
                continue

            # Try each wordlist
            for wordlist_name in wordlist_names:
                
                # Check if we should stop early
                if stop_event is not None and getattr(stop_event, "is_set", lambda: False)():
                    was_stopped_early = True
                    break
                    
                # Build the full path to the wordlist file
                wordlist_path = os.path.join(WORDLISTS_FOLDER, wordlist_name)
                
                # Check if the wordlist file exists
                if not os.path.isfile(wordlist_path):
                    send_status_message(
                        "",
                        False,
                        "#f00",
                        [
                            ("Wordlist not found: ", "#f00"),
                            (wordlist_name, "#e6d9ff"),
                        ]
                    )
                    continue

                send_status_message(
                    "",
                    False,
                    "#fff",
                    [
                        ("Checking wordlist: ", "#fff"),
                        (wordlist_name, "#e6d9ff"),
                    ]
                )
                
                try:
                    # More efficient file processing - read in chunks and process line by line
                    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
                        # Read all lines at once for better I/O performance with smaller files
                        # For very large files, this could be modified to read in chunks
                        lines = file.readlines()
                        total_lines = len(lines)
                    
                    # Process each password
                    for line_number, line in enumerate(lines, 1):
                        
                        # Check if we should stop early
                        if stop_event is not None and getattr(stop_event, "is_set", lambda: False)():
                            was_stopped_early = True
                            break
                            
                        # Get the password from this line
                        password = line.strip()
                        if not password:
                            continue  # Skip empty lines
                        
                        # Skip passwords we've already tested (avoid duplicate work)
                        password_key = f"{password}:{algorithm}"
                        if password_key in tested_passwords:
                            continue
                        tested_passwords.add(password_key)
                        
                        # Hash this password with the current algorithm (using cached hasher)
                        password_hash = create_hash(password, hasher)
                        
                        # Check if this hash matches any of our target hashes (O(1) lookup with set)
                        if password_hash in hashes_in_group:
                            # We found a match!
                            found_passwords[password_hash] = (password, algorithm)
                            found_in_group[hash_length] += 1
                        
                        # Check if we've found all hashes - if so, we can stop early!
                        if len(found_passwords) == len(hash_list):
                            send_status_message(f"🎉 All {len(hash_list)} hashes found! Stopping early for efficiency.")
                            was_stopped_early = True
                            break
                        
                        # Update progress every 1000 passwords
                        if line_number % 1000 == 0:
                            send_status_message(
                                "",
                                True,  # replace_last_line=True
                                "#fff",
                                [
                                    (f"Checked {line_number:,} / {total_lines:,} passwords in ", "#fff"),
                                    (wordlist_name, "#e6d9ff"),
                                    (" using ", "#fff"),
                                    (algorithm, "#0ff"),
                                    ("...", "#fff"),
                                ]
                            )
                            
                            # Update the progress bar if we have a callback
                            if progress_callback:
                                progress_callback(line_number, total_lines)
                                    
                except Exception as error:
                    send_status_message(
                        "",
                        False,
                        "#f00",
                        [
                            ("Error reading ", "#f00"),
                            (wordlist_name, "#e6d9ff"),
                            (": ", "#f00"),
                            (str(error), "#f00"),
                        ]
                    )
                
                # If we found all hashes or stopped early, break out of wordlist loop
                if was_stopped_early:
                    break
                
                # Skip remaining wordlists for this algorithm if we found all hashes in this length group
                if found_in_group[hash_length] == len(hashes_in_group):
                    send_status_message(
                        "",
                        False,
                        "#0f0",
                        [
                            ("[ ✓ ] Found all ", "#0f0"),
                            (str(len(hashes_in_group)), "#fff"),
                            (" hashes for ", "#0f0"),
                            (f"{hash_length}-char", "#fff"),
                            (" length using ", "#0f0"),
                            (algorithm, "#0ff"),
                        ]
                    )
                    break
                    
            # If we found all hashes or stopped early, break out of algorithm loop too
            if was_stopped_early:
                break
                
            # Skip remaining algorithms if we found all hashes in this length group
            if found_in_group[hash_length] == len(hashes_in_group):
                break
                
        # Add a blank line for readability
        send_status_message("")
        
        # If we stopped early, break out of length loop too
        if was_stopped_early:
            break

    # Show results
    if found_passwords:
        for hash_value, (password, algorithm) in found_passwords.items():
            if gui_callback:
                # Send colorful results to GUI
                gui_callback(
                    "",
                    False,
                    "#0f0",
                    [
                        ("[ ! ] ", "#f00"),  # [ ! ] in red
                        ("Weak Password Found: ", "#fff"),
                        (password, "#f00"),  # Password in red
                    ]
                )
                gui_callback(
                    "",
                    False,
                    "#0f0",
                    [
                        ("(Hash: ", "#fff"),
                        (hash_value, "#ff0"),      # Hash in yellow
                        (", Algorithm: ", "#fff"),
                        (algorithm, "#0ff"),       # Algorithm in cyan
                        (")", "#fff"),
                    ]
                )
            else:
                # Simple console output
                print(f"[ ! ] Weak Password Found: {password}")
                print(f"(Hash: {hash_value}, Algorithm: {algorithm})")
    
    # Send final status message
    if not found_passwords:
        send_status_message("No matches were found.")
    else:
        if len(found_passwords) == len(hash_list):
            send_status_message(f"🎯 Perfect! All {len(found_passwords)} hash(es) successfully cracked!")
        else:
            send_status_message(f"Found {len(found_passwords)} out of {len(hash_list)} hash(es).")
    
    # Return results
    # Success means we found passwords AND either completed normally OR stopped early because we found everything
    verification_successful = bool(found_passwords and (not was_stopped_early or len(found_passwords) == len(hash_list)))
    return verification_successful, found_passwords