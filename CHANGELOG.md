# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-29

### Added

- `pocforge check`: grades a PoC spec on 16 rules with blocking, major and minor severities.
- `pocforge report`: renders submission markdown with the proof grade attached.
- `pocforge scaffold`: emits a spec skeleton that satisfies the structural rules.
- `pocforge hash` / `pocforge verify`: tamper-evident evidence manifests with size and digest drift detection, plus unrecorded-file reporting.
- 50 skills across six phases (`frame`, `reproduce`, `minimize`, `oracle`, `verify`, `package`), each with steps, signals, patterns, pitfalls, done-when criteria and canonical references.
- `pocforge validate`: the corpus gate, enforced in CI.
- `pack.json` with a SHA-256 per rendered skill file.

### Fixed

- Manifest paths were recorded relative to the caller's working directory instead of the evidence root, which made `verify` unable to find its own files.
- A manifest stored inside the evidence directory was reported as an unrecorded file.
- `hash` rejected a directory argument instead of expanding it.
- `infer_root` could loop forever when files shared no common parent above the drive root.
