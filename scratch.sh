#!/bin/bash

# Find all directories that have a directory with the same name within it
find . -type d -exec sh -c '
for dir; do
  if [ -d "$dir/$dir" ]; then
    # Move all contents from child directory to parent directory
    mv "$dir/$dir"/* "$dir"
    # Remove the now-empty child directory
    rmdir "$dir/$dir"
  fi
done
' sh {} +
