# ANSWERS.md

## 1. How to run

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
```

### Generate logs (optional)

```bash
python scripts/generate_logs.py
```

### Run analyzer

```bash
python analyzer.py data/sample.log
```

---

## 2. Stack choice

Python was chosen for its strong standard library support for text processing and rapid iteration.

The problem is primarily about **resilient parsing of inconsistent input**, not system architecture or UI. Python allows implementing flexible parsing logic with minimal overhead.

### Tradeoffs

- Node.js would introduce additional complexity for string parsing and file handling.
- Strong typing (TypeScript) is less useful here because the input data itself is unstructured and inconsistent.

---

## 3. One real edge case handled

### Edge Case

Logs containing:

- mixed formats (JSON + plain text)
- extra trailing fields
- missing or invalid status codes
- variable response time formats

### Location

`analyzer.py → parse_line()`

### Approach

Instead of relying on fixed positions, the parser:

- identifies paths via `/api` prefix
- extracts status codes using pattern matching
- scans tokens in reverse to locate response times
- attempts JSON parsing first before fallback

### Without this

The analyzer would:

- break when additional fields are appended
- misparse logs with shifted columns
- fail on mixed-format datasets

---

## 4. AI usage

AI was used for:

- exploring parsing strategies for mixed-format logs
- identifying potential edge cases
- improving robustness of input handling

### Modifications

Initial suggestions used positional parsing. This was replaced with a heuristic-based approach because:

- log formats are not stable
- schema evolution breaks fixed parsing
- robustness is more important than strict correctness

The final implementation reflects these adjustments.

---

## 5. Honest gap

### Current limitations

- Heuristic parsing may misidentify fields in highly corrupted logs
- No structured schema validation
- Limited output format (CLI only)

### Improvements with more time

- Introduce multiple parsing strategies with fallback layers
- Add confidence scoring for parsed fields
- Provide JSON output format
- Add test suite with diverse malformed datasets

---

## Summary

The tool focuses on **resilience under uncertain input conditions**, ensuring it:

- does not crash
- does not silently discard data
- surfaces malformed input explicitly

This mirrors real-world log processing systems where input consistency cannot be guaranteed.
