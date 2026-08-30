# Standardization configuration

Working directory: .standardization
Publication directory pattern: standards/v{version}
Revision assessment directory pattern: standards/revision-assessments
Versioning system: Git
Git command permissions: elevated-write-only
Release preservation: Preserve the current release in its resolved versioned directory; immutable Git release tags preserve superseded releases and their matching document metadata
Release storage: single-current-tagged-history
Version policy: standard-versioning
Initial version: 1
Version levels: three
Version rendering: Use major.minor.patch conceptually; omit trailing zero components, so 1.0.0 renders as 1, 1.1.0 as 1.1, and 1.0.1 remains 1.0.1; the version value itself has no v prefix
Version examples: from baseline 1: patch => 1.0.1, minor => 1.1, major => 2
Tag pattern: web-editor-revisions-v{version}
Source report integrations: Local repository paths and the GitHub repository mahendrimd/web-editor-revisions
Publication surfaces: Canonical release directories under standards/; current GitHub Pages site at https://mahendrimd.github.io/web-editor-revisions/, verified by site/build.py, site/verify.py, and .github/workflows/pages.yml
Notification targets: none

## Repository-specific notes

The standard-versioning policy governs publication-set releases. Embedded modelVersion, serializationProfile, and independently versioned mapping profiles continue to follow Section 19 of the standard.

Existing release identifiers normalize consistently: document metadata version 1, directory standards/v1, and tag web-editor-revisions-v1 all designate conceptual version 1.0.0 with canonical rendering 1.

The current canonical release directory is authoritative; the generated website derives from it. Superseded release directories are removed from the active tree after their immutable tags are verified. Historical website pages are not required.
